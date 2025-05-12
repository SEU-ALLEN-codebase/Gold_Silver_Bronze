import os
import random

import numpy as np
import v3dpy
from skimage.draw.draw_nd import line_nd
from v3dpy.loaders import PBD
from v3dpy.loaders import Raw

pbd = PBD()
raw = Raw()

final_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_image'
swc_skeleton_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\new_target_image'
synthetic_addsoma_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_image_addsoma'
synthetic_addsoma_image_v3dpbd_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_image_addsoma_v3dpbd'

predict_image_dict = {}
image_name_dict = {}
for predict_image_name in os.listdir(swc_skeleton_image_dir_path):
    path = os.path.join(swc_skeleton_image_dir_path, predict_image_name)
    image_number = predict_image_name.split("_")[0]
    predict_image_dict[image_number] = path
    image_name_dict[image_number] = predict_image_name

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

def swc_converted_2_vox_dict(swc_path, x_offset, y_offset, z_offset, xshape, yshape, zshape, image):
    dict1 = {}
    dict2 = {}
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

    for i in range(len(xl_idxArray)):
        xi = xl_idxArray[i]
        yi = yl_idxArray[i]
        zi = zl_idxArray[i]
        if is_in_crop_box(xi, yi, zi, (zshape, yshape, xshape)):
            key = str(xl_idxArray[i]) + '_' + str(yl_idxArray[i]) + '_' + str(zl_idxArray[i])
            dict1[key] = image[0][zl_idxArray[i]][yl_idxArray[i]][xl_idxArray[i]]

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
        dict2[key] = image[0][zn_idx[i]][yn_idx[i]][xn_idx[i]]

    return dict1, dict2

def adjust_swc_vox(swc_coor_dict1, swc_coor_dict2, synthetic_addsoma_image):
    for key, value in swc_coor_dict2.items():
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        synthetic_addsoma_image[0][z][y][x] = min(255, value + 10)

    for key, value in swc_coor_dict1.items():
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        synthetic_addsoma_image[0][z][y][x] = min(255, value + 10)

def merge(swc_coor_dict1, swc_coor_dict2, background_image):
    # 设置比例 (例如 50% 的键)
    ratio_2 = 0.2

    for key, value in swc_coor_dict2.items():
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        background_image[0][z][y][x] = min(255, value + 10)


    # 计算要选取的键的数量
    num_keys_2 = int(len(swc_coor_dict2) * ratio_2)

    # 随机选择对应数量的键
    random_keys_2 = random.sample(swc_coor_dict2.keys(), num_keys_2)

    for key in random_keys_2:
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        background_image[0][z][y][x] = 0

    for key, value in swc_coor_dict1.items():
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        background_image[0][z][y][x] = max(5, value - 5)
        print(background_image[0][z][y][x])

    ratio_1 = 0.1
    # 计算要选取的键的数量
    num_keys_1 = int(len(swc_coor_dict1) * ratio_1)

    # 随机选择对应数量的键
    random_keys_1 = random.sample(swc_coor_dict1.keys(), num_keys_1)

    for key in random_keys_1:
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        background_image[0][z][y][x] = 0

    return background_image


swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\new_converted_swc'
# swc_name = r'06871_P040_T01_-_S014_-_MTG_stamp_2024_02_28_15_14.ano.eswc'
# image_number = swc_name.split("_")[0]
# swc_path = os.path.join(swc_dir_path, swc_name)
swc_dict = {}
for swc_name in os.listdir(swc_dir_path):
    swc_path = os.path.join(swc_dir_path, swc_name)
    image_number = swc_name.split("_")[0]
    swc_dict[image_number] = swc_path

# swc_skeleton_image_name = image_name_dict[image_number]
# swc_skeleton_image_path = os.path.join(swc_skeleton_image_dir_path, swc_skeleton_image_name)
# swc_skeleton_image = pbd.load(swc_skeleton_image_path)
# background_image_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\targetImageBackground\13883_P073_T01_(2)_S002_1dAFTsur_pLV.L_R0460_RJ_20240417_RJ.v3draw'
# background_image = raw.load(background_image_path)
#
# final_image_name = swc_skeleton_image_name[0:-len('.v3dpbd')] + '_synthetic.v3draw'
# final_image_path = os.path.join(final_image_dir_path, final_image_name)
#
# pbd.save(final_image_path, background_image)
# background_image = pbd.load(final_image_path)
# background_image_shape = background_image.shape
# swc_skeleton_shape = swc_skeleton_image.shape
#
# if background_image_shape[1] < swc_skeleton_shape[1]:
#     background_image = np.pad(background_image, ((0, 0), (0, 1), (0, 0), (0, 0)), mode='constant', constant_values=0)
# if background_image_shape[2] < swc_skeleton_shape[2]:
#     background_image = np.pad(background_image, ((0, 0), (0, 0), (0, 1), (0, 0)), mode='constant', constant_values=0)
# if background_image_shape[3] < swc_skeleton_shape[3]:
#     background_image = np.pad(background_image, ((0, 0), (0, 0), (0, 0), (0, 1)), mode='constant', constant_values=0)
#
# # background_image[0, 0:40, :, :] = background_image[0, 40:80, :, :]
# background_image[0, -120:-60, 400:650, 0:600] = background_image[0, 0:60, 400:650, 0:600]
# background_image[0, -60:, 400:650, 0:600] = background_image[0, 0:60, 400:650, 0:600]

# synthetic_addsoma_image_name = r'06871_P040_T01_-_S014_-_MTG.L_R0919_RJ_20230712_YW_synthetic.v3draw'
for synthetic_addsoma_image_name in os.listdir(synthetic_addsoma_image_dir_path):
    # if '09567' not in synthetic_addsoma_image_name:
    #     continue
    synthetic_addsoma_image_path = os.path.join(synthetic_addsoma_image_dir_path, synthetic_addsoma_image_name)
    synthetic_addsoma_image = raw.load(synthetic_addsoma_image_path)
    synthetic_addsoma_image_v3dpbd_path = os.path.join(synthetic_addsoma_image_v3dpbd_dir_path, synthetic_addsoma_image_name[0:-len('.v3draw')] + '.v3dpbd')
    pbd.save(synthetic_addsoma_image_v3dpbd_path, synthetic_addsoma_image)
    synthetic_addsoma_image = pbd.load(synthetic_addsoma_image_v3dpbd_path)
    shape = synthetic_addsoma_image.shape
    swc_path = swc_dict[synthetic_addsoma_image_name.split("_")[0]]

    swc_coor_dict1, swc_coor_dict2 = swc_converted_2_vox_dict(swc_path, 0, 0, 0, shape[3], shape[2], shape[1], synthetic_addsoma_image)
    adjust_swc_vox(swc_coor_dict1, swc_coor_dict2, synthetic_addsoma_image)
    # swc_coor_dict1, swc_coor_dict2 = swc_converted_2_vox_dict(swc_path, 0, 0, 0, swc_skeleton_shape[3], swc_skeleton_shape[2], swc_skeleton_shape[1], swc_skeleton_image)
    # background_image = merge(swc_coor_dict1, swc_coor_dict2, background_image)
    # raw.save(final_image_path, background_image)

    raw.save(synthetic_addsoma_image_path, synthetic_addsoma_image)