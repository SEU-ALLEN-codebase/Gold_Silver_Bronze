import math
import os
import numpy as np
from skimage.draw.draw_nd import line_nd
from v3dpy.loaders import PBD

predict_img_after_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\merge9\after'
converted_swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\convertedSwc'
predict_skeleton_img_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\sup_skeleton_image'

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

def swc_converted_2_vox_dict(swc_path, x_offset, y_offset, z_offset, xshape, yshape, zshape, predict_image):
    dict1 = {}
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

    xl_idxArray = np.array(xl_idx)
    yl_idxArray = np.array(yl_idx)
    zl_idxArray = np.array(zl_idx)

    # for i in range(len(xl_idxArray)):
    #     xi = xl_idxArray[i]
    #     yi = yl_idxArray[i]
    #     zi = zl_idxArray[i]
    #     if is_in_crop_box(xi, yi, zi, (zshape, yshape, xshape)):
    #         key = str(xl_idxArray[i]) + '_' + str(yl_idxArray[i]) + '_' + str(zl_idxArray[i])
    #         dict1[key] = predict_image[0][zl_idxArray[i]][yl_idxArray[i]][xl_idxArray[i]]

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

    for i in range(len(xn_idx)):
        key = str(xn_idx[i]) + '_' + str(yn_idx[i]) + '_' + str(zn_idx[i])
        dict1[key] = predict_image[0][zn_idx[i]][yn_idx[i]][xn_idx[i]]

    return dict1

def get_predict_skeleton_image(dict1):
    img = np.zeros((1, 128, 512, 512), dtype=np.uint8)
    # for patch_name in os.listdir(dir_path):
    #     patch = pbd.load(os.path.join(dir_path, patch_name))
    #     patch_name = patch_name[0:-len('.v3dpbd')]
    #     parts = patch_name.split('_')
    #     x_index = int(parts[1])
    #     y_index = int(parts[3])
    #     img[0, :, y_index * 128:(y_index+1)*128, x_index * 128:(x_index+1)*128] = patch
    # img_before = numpy.copy(img)

    for key, value in dict1.items():
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        img[0][z][y][x] = value
        # img[0][z][y][x] = value
    # for key, value in swc_dict2.items():
    #     parts = key.split('_')
    #     x = int(parts[0])
    #     y = int(parts[1])
    #     z = int(parts[2])
    #     img[0][z][y][x] = value

    return img

pbd = PBD()

predict_image_dict = {}
image_name_dict = {}
for predict_image_name in os.listdir(predict_img_after_dir_path):
    path = os.path.join(predict_img_after_dir_path, predict_image_name)
    image_number = predict_image_name.split("_")[0]
    predict_image_dict[image_number] = path
    image_name_dict[image_number] = predict_image_name

for converted_swc_name in os.listdir(converted_swc_dir_path):
    swc_path = os.path.join(converted_swc_dir_path, converted_swc_name)
    image_number = converted_swc_name.split("_")[0]
    predict_image = pbd.load(predict_image_dict[image_number])
    swc_coor_dict = swc_converted_2_vox_dict(swc_path, 0, 0, 0, 512, 512, 128, predict_image)
    swc_skeleton_img = get_predict_skeleton_image(swc_coor_dict)
    save_name = image_name_dict[image_number]
    save_path = os.path.join(predict_skeleton_img_dir_path, save_name)
    pbd.save(save_path, swc_skeleton_img)
