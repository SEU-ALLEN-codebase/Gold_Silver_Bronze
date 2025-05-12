import os
import numpy as np
from skimage.draw.draw_nd import line_nd
from v3dpy.loaders import PBD, Raw

target_image_dir_path = r'Z:\SEU-ALLEN\Projects\Human_Neurons\all_human_cells\all_human_cells_v3draw_8bit\human_brain_data_v3draw_13778_14203\AtlasVolume'
converted_swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\convertedSwc'
target_image_background_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\targetImageBackground'

def get_root_coor(tree):
    for swc_node in tree:
        p = swc_node[-1]
        if p == -1:
            return swc_node[2], swc_node[3], swc_node[4]

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
    radius = 7
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

    print(xl_idxArray)
    print(yl_idxArray)
    print(zl_idxArray)
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

    print(dict1)
    return dict1


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
    return z_center_img

def get_target_image_background(swc_coor_dict, target_image_z_center, root_coor):
    xi, yi, zi = root_coor
    xi, yi, zi = int(xi), int(yi), int(zi)
    radius = 40
    xn_idx, yn_idx, zn_idx = [], [], []
    x_range = range(round(max(xi - radius, 0)), round(min(xi + radius, 512 - 1) + 1))
    y_range = range(round(max(yi - radius, 0)), round(min(yi + radius, 512 - 1) + 1))
    z_range = range(round(max(zi - radius, 0)), round(min(zi + radius, 128 - 1) + 1))
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

    for (x, y, z) in zip(xn_idx, yn_idx, zn_idx):
        target_image_z_center[0][z][y][x] = 20

    for key, value in swc_coor_dict.items():
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        print(target_image_z_center[0][z][y][x])
        target_image_z_center[0][z][y][x] = 0
    return target_image_z_center


pbd = PBD()

# target_z_center_image_dict = {}
# image_name_dict = {}
# for target_z_center_image_name in os.listdir(target_image_z_center_dir_path):
#     path = os.path.join(target_image_z_center_dir_path, target_z_center_image_name)
#     image_number = target_z_center_image_name.split("_")[0]
#     target_z_center_image_dict[image_number] = path
#     image_name_dict[image_number] = target_z_center_image_name

# for converted_swc_name in os.listdir(converted_swc_dir_path):
#     swc_path = os.path.join(converted_swc_dir_path, converted_swc_name)
#     image_number = converted_swc_name.split("_")[0]
#     target_z_center_image = pbd.load(target_z_center_image_dict[image_number])
#     swc_coor_dict = swc_converted_2_vox_dict(swc_path, 0, 0, 0, 512, 512, 128, target_z_center_image)
#     tree = parse_swc(swc_path)
#     root_coor = get_root_coor(tree)
#
#     target_image_background = get_target_image_background(swc_coor_dict, target_z_center_image, root_coor)
#
#     save_name = image_name_dict[image_number]
#     save_path = os.path.join(target_image_background_dir_path, save_name)
#     pbd.save(save_path, target_image_background)

def get_target_image_background_v2(target_image_whole, x_start, y_start, z_start):
    # print(type(target_image_whole))
    return target_image_whole[:, z_start:z_start + 154, y_start:y_start + 814, x_start:x_start + 690]

raw = Raw()

for target_image_whole_name in os.listdir(target_image_dir_path):
    if target_image_whole_name == r'13883_P073_T01_(2)_S002_1dAFTsur_pLV.L_R0460_RJ_20240417_RJ.v3draw':
        target_image_whole_path = os.path.join(target_image_dir_path, target_image_whole_name)
        target_image_whole = raw.load(target_image_whole_path)

        x_start = 0
        y_start = 630
        z_start = 0
        target_image_background = get_target_image_background_v2(target_image_whole, x_start, y_start, z_start)

        save_name = target_image_whole_name
        save_path = os.path.join(target_image_background_dir_path, save_name)
        raw.save(save_path, target_image_background)
        break

