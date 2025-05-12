import math
import os
import numpy as np
from skimage.draw.draw_nd import line_nd
from v3dpy.loaders import PBD

ori_swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\new_swc_sup'
apo_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\mouse\apo'
txt_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\mouse\txt'
swc_converted_img_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\new_swc_converted_image'
converted_swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\new_converted_swc'
skeleton_patch_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\new_skeleton_patch'
target_img_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\new_target_image'
target_whole_img_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\new_target_whole_image'

def generate_predict_skeleton(tree, save_path, zshape=32, yshape=32, xshape=32, radius=1.0):
    pbd = PBD()
    img = np.zeros((zshape, yshape, xshape), dtype=np.uint8)
    xl_idx, yl_idx, zl_idx = [], [], []
    # all_coor_list = read_swc(swc_path)
    # print(all_coor_list)

    for point in tree:
        if point[6] == -1:
            continue
        parent_point = tree[point[6] - 1]
        lin = line_nd(list(parent_point[2:5])[::-1], list(point[2:5])[::-1], endpoint=True)
        xl_idx.extend(list(lin[2]))
        yl_idx.extend(list(lin[1]))
        zl_idx.extend(list(lin[0]))

    xl_idxArray = np.array(xl_idx)
    yl_idxArray = np.array(yl_idx)
    zl_idxArray = np.array(zl_idx)

    xn_idx, yn_idx, zn_idx = [], [], []
    for (xi, yi, zi) in zip(xl_idxArray, yl_idxArray, zl_idxArray):
        if is_in_crop_box(xi, yi, zi, (zshape, yshape, xshape)):
            x_range = range(round(max(xi - radius, 0)), round(min(xi + radius, xshape - 1) + 1))
            y_range = range(round(max(yi - radius, 0)), round(min(yi + radius, yshape - 1) + 1))
            z_range = range(round(max(zi - radius, 0)), round(min(zi + radius, zshape - 1) + 1))
            for p in x_range:
                for q in y_range:
                    for k in z_range:
                        dist = np.sqrt((p - xi) ** 2 + (q - yi) ** 2 + (k - zi) ** 2)
                        if dist <= radius * 1.0:
                            xn_idx.append(p)
                            yn_idx.append(q)
                            zn_idx.append(k)
            xn_idx.append(xi)
            yn_idx.append(yi)
            zn_idx.append(zi)

    img[zn_idx, yn_idx, xn_idx] = 255

    img = np.expand_dims(img, axis=0)
    pbd.save(save_path, img)
    return img

def read_swc(swc_path):
    all_coor_list = []
    seg_coor_list = []
    with open(swc_path, "r") as file:
        for line in file:
            line = line.lstrip()
            if line[0] == "#":
                continue
            tokens = line.split(" ")
            x = round(float(tokens[2]))
            y = round(float(tokens[3]))
            z = round(float(tokens[4]))
            pn = int(tokens[6])
            seg_coor_list.append((x, y, z))
            if pn == -1:
                list_copy = seg_coor_list.copy()
                all_coor_list.append(list_copy)
                seg_coor_list.clear()
    return all_coor_list

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

def get_min_max_from_tree(tree):
    x_min, y_min, z_min = 100000, 100000, 100000
    x_max, y_max, z_max = 0, 0, 0
    for point in tree:
        x = point[2]
        y = point[3]
        z = point[4]
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        z_min = min(z_min, z)
        x_max = max(x_max, x)
        y_max = max(y_max, y)
        z_max = max(z_max, z)
    return x_min, y_min, z_min, x_max, y_max, z_max

def get_swc_skeleton_img_converted_swc(swc_path, converted_swc_path, skeleton_img_path, target_whole_img, target_img_path):
    pbd = PBD()

    tree = parse_swc(swc_path)
    swc_name = os.path.basename(swc_path)[0:-len('.ano.eswc.attachment.eswc')]

    x_min, y_min, z_min, x_max, y_max, z_max = get_min_max_from_tree(tree)
    x_start = int(x_min) - 30
    y_start = int(y_min) - 30
    z_start = int(z_min) - 30
    if x_start < 0:
        x_start = 0
    if y_start < 0:
        y_start = 0
    if z_start < 0:
        z_start = 0

    x_interval = math.ceil(x_max - x_start)
    y_interval = math.ceil(y_max - y_start)
    z_interval = math.ceil(z_max - z_start)
    if (x_interval + 1) % 128 == 0:
        x_shape = x_interval + 1
    else:
        x_shape = ((x_interval + 1) // 128 + 1) * 128
    if (y_interval + 1) % 128 == 0:
        y_shape = y_interval + 1
    else:
        y_shape = ((y_interval + 1) // 128 + 1) * 128
    if (z_interval + 1) % 128 == 0:
        z_shape = z_interval + 1
    else:
        z_shape = ((z_interval + 1) // 128 + 1) * 128

    x_shape = x_interval + 1 + 30
    y_shape = y_interval + 1 + 30
    z_shape = z_interval + 1 + 30

    target_whole_img_shape = target_whole_img.shape
    if(x_start + x_shape - 1 > target_whole_img_shape[3]):
        x_shape = x_interval + 1
    if(y_start + y_shape - 1 > target_whole_img_shape[2]):
        y_shape = y_interval + 1
    if(z_start + z_shape - 1 > target_whole_img_shape[1]):
        z_shape = z_interval + 1

    # 生成converted_swc
    for i in range(len(tree)):
        idx, type_, x, y, z, r, p = tree[i]
        x_converted = x - x_start
        y_converted = y - y_start
        z_converted = z - z_start
        tree[i] = (idx, type_, x_converted, y_converted, z_converted, r, p)
    write_swc(tree, converted_swc_path)

    # 生成swc_skeleton_img
    skeleton_img = generate_predict_skeleton(tree, skeleton_img_path, z_shape, y_shape, x_shape, 2)

    target_img = target_whole_img[:, z_start:z_start + z_shape, y_start:y_start + y_shape, x_start:x_start + x_shape]
    pbd.save(target_img_path, target_img)

    # x_patch_size = x_shape // 128
    # y_patch_size = y_shape // 128
    # z_patch_size = z_shape // 128

    # for i in range(x_patch_size):
    #     for j in range(y_patch_size):
    #         for p in range(z_patch_size):
    #             patch = skeleton_img[:, 128 * p:128 * (p + 1), j * 128:(j + 1) * 128, i * 128:(i + 1) * 128]
    #             patch_name = 'x_' + str(i) + '_y_' + str(j) + '_z_' + str(p) + '.v3dpbd'
    #             patch_dir_path = os.path.join(skeleton_patch_dir_path, patch_dir_name)
    #             patch_path = os.path.join(patch_dir_path, patch_name)
    #             if not os.path.exists(patch_dir_path):
    #                 os.mkdir(patch_dir_path)
    #             pbd.save(patch_path, patch)

def generate_txt(center_2_xyz_dict, txt_path):
    with open(txt_path, "w") as file:
        for key, value in center_2_xyz_dict.items():
            file.write(key + ' ' + value + '\n')

def get_apo_point_list(apo_point_dict):
    apo_point_list = []
    n = 1
    for key in apo_point_dict.keys():
        parts = key.split('_')
        x = parts[0]
        y = parts[1]
        z = parts[2]
        apo_point_list.append((n, "", "", "", z, x, y, 100, 100, 100))
        n += 1
    return apo_point_list


v3dpbd_name_dict = {}
for img in os.listdir(target_whole_img_dir_path):
    if img.endswith('v3dpbd'):
        img_path = os.path.join(target_whole_img_dir_path, img)
        image_name = img.split('_')[0]
        v3dpbd_name_dict[image_name] = img

pbd = PBD()
for swc in os.listdir(ori_swc_dir_path):
    swc_path = os.path.join(ori_swc_dir_path, swc)
    converted_swc_path = os.path.join(converted_swc_dir_path, swc)
    skeleton_img_name = swc[0:-len('.ano.eswc')] + '.v3dpbd'
    image_number = swc.split("_")[0]
    # patch_dir_name = swc[0:-len('.ano.eswc')]
    skeleton_img_path = os.path.join(swc_converted_img_dir_path, v3dpbd_name_dict[image_number])
    target_img_path = os.path.join(target_img_dir_path, v3dpbd_name_dict[image_number])
    target_whole_img_path = os.path.join(target_whole_img_dir_path, v3dpbd_name_dict[image_number])
    target_whole_img = pbd.load(target_whole_img_path)
    get_swc_skeleton_img_converted_swc(swc_path, converted_swc_path, skeleton_img_path, target_whole_img, target_img_path)

