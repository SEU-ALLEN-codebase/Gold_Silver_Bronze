import os
import numpy as np
import v3dpy
from skimage.draw.draw_nd import line_nd
from v3dpy.loaders import PBD
from v3dpy.loaders import Raw

pbd = PBD()
raw = Raw()

# final_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_image'
synthetic_image_v3dpbd_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_image_v3dpbd'
synthetic_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_image'
synthetic_image_addsoma_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_image_addsoma'
swc_skeleton_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\new_target_image'

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
    radius = 1.5
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

def merge(swc_coor_dict1, swc_coor_dict2, background_image):
    for key, value in swc_coor_dict2.items():
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        background_image[0][z][y][x] = min(255, value + 5)

    for key, value in swc_coor_dict1.items():
        parts = key.split('_')
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        background_image[0][z][y][x] = min(255, value + 12)
    return background_image

def get_root_coor(tree):
    for swc_node in tree:
        p = swc_node[-1]
        if p == -1:
            return swc_node[2], swc_node[3], swc_node[4]

def add_soma(swc_path, swc_skeleton_image, synthetic_image):
    tree = parse_swc(swc_path)
    root_coor = get_root_coor(tree)
    radius = 18
    xi, yi, zi = root_coor
    xi, yi, zi = int(xi), int(yi), int(zi)
    xn_idx, yn_idx, zn_idx = [], [], []
    x_range = range(round(max(xi - radius, 0)), round(min(xi + radius, 1000 - 1) + 1))
    y_range = range(round(max(yi - radius, 0)), round(min(yi + radius, 1000 - 1) + 1))
    z_range = range(round(max(zi - radius, 0)), round(min(zi + radius, 250 - 1) + 1))
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
        synthetic_image[0][z][y][x] = swc_skeleton_image[0][z][y][x]
    return synthetic_image

swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\new_converted_swc'
swc_name = r'10440_P041_T01_-_S015_-_TL.R_R0613_RJ_20230713_YW.ano.eswc'
image_number = swc_name.split("_")[0]
swc_path = os.path.join(swc_dir_path, swc_name)

swc_skeleton_image_name = image_name_dict[image_number]
swc_skeleton_image_path = os.path.join(swc_skeleton_image_dir_path, swc_skeleton_image_name)
swc_skeleton_image = pbd.load(swc_skeleton_image_path)
# background_image_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\targetImageBackground\13883_P073_T01_(2)_S002_1dAFTsur_pLV.L_R0460_RJ_20240417_RJ.v3draw'
# background_image = raw.load(background_image_path)

# final_image_name = swc_skeleton_image_name[0:-len('.v3dpbd')] + '_synthetic.v3draw'
# final_image_path = os.path.join(final_image_dir_path, final_image_name)

synthetic_image_name = r'10440_P041_T01_-_S015_-_TL.R_R0613_RJ_20230713_YW_synthetic.v3draw'
synthetic_image_path = os.path.join(synthetic_image_dir_path, synthetic_image_name)
synthetic_image = raw.load(synthetic_image_path)
synthetic_image_v3dpbd_path = os.path.join(synthetic_image_v3dpbd_dir_path, synthetic_image_name[0:-len('.v3draw')] + '.v3dpbd')
pbd.save(synthetic_image_v3dpbd_path, synthetic_image)
synthetic_image = pbd.load(synthetic_image_v3dpbd_path)

synthetic_addsoma_image = add_soma(swc_path, swc_skeleton_image, synthetic_image)

synthetic_addsoma_image_path = os.path.join(synthetic_image_addsoma_dir_path, synthetic_image_name)
raw.save(synthetic_addsoma_image_path, synthetic_addsoma_image)
