import os

import numpy
import v3dpy
from skimage.draw.draw_nd import line_nd
from v3dpy.loaders import PBD, Raw

def parse_swc(swc_file):
    tree = []
    with open(swc_file) as fp:
        for line in fp.readlines():
            line = line.strip()
            if not line: continue
            if line[0] == '#': continue
            idx, type_, x, y, z, r, p = line.split()[:7]
            idx = int(idx)
            type_ = int(type_)
            x = float(x)
            y = float(y)
            z = float(z)
            r = float(r)
            p = int(p)
            tree.append((idx, type_, x, y, z, r, p))

    return tree

def is_in_crop_box(x, y, z, cropsize):
    """
    cropsize must be in (z,y,x) order
    """
    if x < 0 or y < 0 or z < 0 or \
            x > cropsize[2] - 1 or \
            y > cropsize[1] - 1 or \
            z > cropsize[0] - 1:
        return False
    return True

def get_z_center_img(original_img, center_size=128):
    # (c, z, y, x)
    shape = original_img.shape
    if shape[1] < center_size:
        raise ValueError("error: z < center_size")
    half_size = (shape[1] - center_size) // 2
    if shape[1] % 2 == 0:
        z_center_img = original_img[:, half_size:shape[1] - half_size, :, :]
    else:
        z_center_img = original_img[:, half_size:shape[1] - 1 - half_size, :, :]
    return z_center_img, half_size

def swc_converted_2_vox_dict(swc_path, x_offset, y_offset, z_offset, xshape, yshape, zshape, z_center_image):
    dict = {}
    radius = 2
    xl_idx, yl_idx, zl_idx = [], [], []
    # all_coor_list = read_swc(swc_path)
    # print(all_coor_list)
    tree = parse_swc(swc_path)
    for i in range(len(tree)):
        idx, type_, x, y, z, r, p = tree[i]
        x += x_offset
        y += y_offset
        z += z_offset
        tree[i] = (idx, type_, x, y, z, r, p)
    for point in tree:
        if point[6] == -1:
            continue
        parent_point = tree[point[6] - 1]
        lin = line_nd(list(parent_point[2:5])[::-1], list(point[2:5])[::-1], endpoint=True)
        xl_idx.extend(list(lin[2]))
        yl_idx.extend(list(lin[1]))
        zl_idx.extend(list(lin[0]))

    xl_idxArray = numpy.array(xl_idx)
    yl_idxArray = numpy.array(yl_idx)
    zl_idxArray = numpy.array(zl_idx)

    xn_idx, yn_idx, zn_idx = [], [], []
    for (xi, yi, zi) in zip(xl_idxArray, yl_idxArray, zl_idxArray):
        if is_in_crop_box(xi, yi, zi, (zshape, yshape, xshape)):
            x_range = range(round(max(xi - radius, 0)), round(min(xi + radius, xshape - 1) + 1))
            y_range = range(round(max(yi - radius, 0)), round(min(yi + radius, yshape - 1) + 1))
            z_range = range(round(max(zi - radius, 0)), round(min(zi + radius, zshape - 1) + 1))
            for p in x_range:
                for q in y_range:
                    for k in z_range:
                        dist = numpy.sqrt((p - xi) ** 2 + (q - yi) ** 2 + (k - zi) ** 2)
                        if dist <= radius * 1.0:
                            xn_idx.append(p)
                            yn_idx.append(q)
                            zn_idx.append(k)
            xn_idx.append(xi)
            yn_idx.append(yi)
            zn_idx.append(zi)

    for i in range(len(xn_idx)):
        key = str(xn_idx[i]) + '_' + str(yn_idx[i]) + '_' + str(zn_idx[i])
        dict[key] = z_center_image[0][zn_idx[i]][yn_idx[i]][xn_idx[i]]

    return dict

def get_converted_swc(swc_path, xoffset, yoffset, zoffset, converted_swc_path):
    tree = parse_swc(swc_path)
    for i in range(len(tree)):
        idx, type_, x, y, z, r, p = tree[i]
        x_converted = x + xoffset
        y_converted = y + yoffset
        z_converted = z + zoffset
        tree[i] = (idx, type_, x_converted, y_converted, z_converted, r, p)
    write_swc(tree, converted_swc_path)

def write_swc(tree, swc_file, header=tuple()):
    if header is None:
        header = []
    with open(swc_file, 'w') as fp:
        for s in header:
            if not s.startswith("#"):
                s = "#" + s
            if not s.endswith("\n") or not s.endswith("\r"):
                s += "\n"
            fp.write(s)
        fp.write(f'##n type x y z r parent\n')
        for leaf in tree:
            idx, type_, x, y, z, r, p = leaf
            fp.write(f'{idx:d} {type_:d} {x:.5f} {y:.5f} {z:.5f} {r:.1f} {p:d}\n')

def get_target_image_whole(target_image_whole_path, dir_path, shape):
    pbd = PBD()
    shape_parts = shape.split("_")
    target_image_whole = numpy.zeros((1, int(shape_parts[2]), int(shape_parts[1]), int(shape_parts[0])), dtype=numpy.uint8)
    print(dir_path)
    for patch_name in os.listdir(dir_path):
        patch = pbd.load(os.path.join(dir_path, patch_name))
        patch_name = patch_name[0:-len('.v3dpbd')]
        parts = patch_name.split('_')
        x_index = int(parts[1])
        y_index = int(parts[3])
        z_index = int(parts[5])
        target_image_whole[0, z_index * 128:(z_index + 1) * 128, y_index * 128:(y_index + 1) * 128, x_index * 128:(x_index + 1) * 128] = patch
    pbd.save(target_image_whole_path, target_image_whole)

def get_final_image(dir_path, swc_dict, z_center_image):
    pbd = PBD()
    for patch_name in os.listdir(dir_path):
        patch = pbd.load(os.path.join(dir_path, patch_name))
        patch_name = patch_name[0:-len('.v3dpbd')]
        parts = patch_name.split('_')
        x_index = int(parts[1])
        y_index = int(parts[3])
        z_center_image[0, :, y_index * 128:(y_index+1)*128, x_index * 128:(x_index+1)*128] = patch
    z_zenter_image_before = numpy.copy(z_center_image)

    for key, value in swc_dict.items():
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        z_center_image[0][z][y][x] = value

    return z_zenter_image_before, z_center_image

def convert_v3draw_2_v3dpbd(v3draw_path):
    raw = Raw()
    pbd = PBD()
    img = raw.load(v3draw_path)
    v3dpbd_path = v3draw_path[0:-len('.v3draw')] + '.v3dpbd'
    pbd.save(v3dpbd_path, img)
    os.remove(v3draw_path)

def rename(v3dpbd_dir_path, txt_path):
    dict = {}
    with open(txt_path) as file:
        for line in file.readlines():
            line = line.strip()
            parts = line.split(' ')
            dict[parts[0]] = parts[1]
    for file_name in os.listdir(v3dpbd_dir_path):
        old_name = file_name[0:-len('.v3dpbd')]
        if not old_name in dict.keys():
           continue
        new_name = dict[old_name]
        old_file_path = os.path.join(v3dpbd_dir_path, file_name)
        new_file_path = os.path.join(v3dpbd_dir_path, new_name + '.v3dpbd')
        os.rename(old_file_path, new_file_path)

# for predict_dir_name in os.listdir(predict_image_dir_path):
#     pbd = PBD()
#     image_name = predict_dir_name.split('_')[0]
#     target_whole_img = pbd.load(target_whole_dict[image_name])
#     z_center_img, half_size = get_z_center_img(target_whole_img)
#
#     converted_swc_path = os.path.join(converted_swc_dir_path, swc_name_dict[image_name])
#     get_converted_swc(swc_dict[image_name], 0, 0, -half_size, converted_swc_path)
#     swc_coor_dict = swc_converted_2_vox_dict(swc_dict[image_name], 0, 0, -half_size, 512, 512, 128, z_center_img)
#     z_zenter_image_before, z_center_image = get_final_image(os.path.join(predict_image_dir_path, predict_dir_name), swc_coor_dict, z_center_img)
#
#     before_path = os.path.join(final_img_before_dir_path, v3dpbd_name_dict[image_name])
#     pbd.save(before_path, z_zenter_image_before)
#     after_path = os.path.join(final_img_after_dir_path, v3dpbd_name_dict[image_name])
#     pbd.save(after_path, z_center_image)

target_image_patch_root_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\mouse\targetImagePatch'
txt_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\mouse\txt'
target_image_whole_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\mouse\targetImageWhole'
txt_shape_info_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\mouse\apo_coor_instruction.txt'
# for root, dirs, files in os.walk(target_image_patch_dir_path):
#     for file in files:
#         file_path = os.path.join(root, file)
#         convert_v3draw_2_v3dpbd(file_path)
# for target_image in os.listdir(target_image_patch_dir_path):
#     txt_path = os.path.join(txt_dir_path, target_image + '.txt')
#     rename(os.path.join(target_image_patch_dir_path, target_image), txt_path)

shape_dict = {}
with open(txt_shape_info_path) as file:
    for line in file.readlines():
        line = line.strip()
        parts = line.split(" ")
        shape_dict[parts[0]] = parts[1]

for target_image in os.listdir(target_image_patch_root_path):
    target_image_patch_dir_path = os.path.join(target_image_patch_root_path, target_image)
    target_image_whole_path = os.path.join(target_image_whole_dir_path, target_image + '.v3dpbd')
    get_target_image_whole(target_image_whole_path, target_image_patch_dir_path, shape_dict[target_image])
