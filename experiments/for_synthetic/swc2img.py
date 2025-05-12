import json
import os
import re
import random
import shutil

from skimage.draw import line_nd
from skimage import exposure
from v3dpy.loaders import PBD
import numpy


def generate_predict_skeleton(swc_path, save_path, zshape=32, yshape=32, xshape=32, radius=1.0):
    pbd = PBD()
    img = numpy.zeros((zshape, yshape, xshape), dtype=numpy.uint8)
    xl_idx, yl_idx, zl_idx = [], [], []
    # all_coor_list = read_swc(swc_path)
    # print(all_coor_list)
    tree = parse_swc(swc_path)

    # for seg_coor_list in all_coor_list:
    #     for i in range(len(seg_coor_list) - 1):
            # xi = seg_coor_list[i][0]
            # yi = seg_coor_list[i][1]
            # zi = seg_coor_list[i][2]
            # xj = seg_coor_list[i + 1][0]
            # yj = seg_coor_list[i + 1][1]
            # zj = seg_coor_list[i + 1][2]

            # '''cylinder mask'''
            # x_down = int(max(min(xi, xj) - radius, 0))
            # x_top = int(min(max(xi, xj) + radius, 32 - 1))
            # y_down = int(max(min(yi, yj) - radius, 0))
            # y_top = int(min(max(zi, zj) + radius, 32 - 1))
            # z_down = int(max(min(zi, zj) - radius, 0))
            # z_top = int(min(max(zi, zj) + radius, 32 - 1))
            # # Iterate through each point in the envelope and determine if it's within the cylinder
            # for k in range(z_down, z_top + 1):
            #     for q in range(y_down, y_top + 1):
            #         for p in range(x_down, x_top + 1):
            #             # Calculate the distance from the line segment using the point-to-line distance formula
            #             norms10 = (xi - p) ** 2 + (yi - q) ** 2 + (zi - k) ** 2
            #             norms21 = (xj - xi) ** 2 + (yj - yi) ** 2 + (zj - zi) ** 2
            #             dots1021 = (xi - p) * (xj - xi) + (yi - q) * (yj - yi) + (zi - k) * (zj - zi)
            #             dist = numpy.sqrt(norms10 - (dots1021 ** 2) / norms21 if norms21 else norms10)
            #             t1 = -dots1021 / norms21 if norms21 else 0
            #             if t1 < 0:
            #                 dist = numpy.sqrt(norms10)
            #             elif t1 > 1:
            #                 dist = numpy.sqrt((xj - p) ** 2 + (yj - q) ** 2 + (zj - k) ** 2)
            #             # Calculate the varying radius along the line segment if the radii are different
            #             if dist <= radius:
            #                 xl_idx.append(p)
            #                 yl_idx.append(q)
            #                 zl_idx.append(k)

            # lin = line_nd(list(seg_coor_list[i])[::-1], list(seg_coor_list[i + 1])[::-1], endpoint=True)
            # xl_idx.extend(list(lin[2]))
            # yl_idx.extend(list(lin[1]))
            # zl_idx.extend(list(lin[0]))

    for point in tree:
        if point[6] == -1:
            continue
        parent_point = tree[point[6] - 1]
        lin = line_nd(list(parent_point[2:5])[::-1], list(point[2:5])[::-1], endpoint=True)
        xl_idx.extend(list(lin[2]))
        yl_idx.extend(list(lin[1]))
        zl_idx.extend(list(lin[0]))

    # x_extra, y_extra, z_extra = [], [], []
    # for i in range(len(zl_idx)):
    #     coor = [xl_idx[i], yl_idx[i], zl_idx[i]]
    #     x_extra.append(coor[0])
    #     y_extra.append(coor[1])
    #     z_extra.append(coor[2] + 1)
    #
    #     x_extra.append(coor[0])
    #     y_extra.append(coor[1])
    #     z_extra.append(coor[2] - 1)
    #
    #     x_extra.append(coor[0] + 1)
    #     y_extra.append(coor[1])
    #     z_extra.append(coor[2])
    #
    #     x_extra.append(coor[0] - 1)
    #     y_extra.append(coor[1])
    #     z_extra.append(coor[2])
    #
    #     x_extra.append(coor[0])
    #     y_extra.append(coor[1] + 1)
    #     z_extra.append(coor[2])
    #
    #     x_extra.append(coor[0])
    #     y_extra.append(coor[1] - 1)
    #     z_extra.append(coor[2])
    #
    # xl_idx.extend(x_extra)
    # yl_idx.extend(y_extra)
    # zl_idx.extend(z_extra)

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

    # xl_list = list(xl_idxArray)
    # yl_list = list(yl_idxArray)
    # zl_list = list(zl_idxArray)
    # for i in range(len(xl_list) - 1):
    #     xi = xl_list[i]
    #     yi = yl_list[i]
    #     zi = zl_list[i]
    #
    #     xj = xl_list[i + 1]
    #     yj = yl_list[i + 1]
    #     zj = zl_list[i + 1]
    #
    #     '''cylinder mask'''
    #     x_down = int(max(min(xi, xj) - radius, 0))
    #     x_top = int(min(max(xi, xj) + radius, 32 - 1))
    #     y_down = int(max(min(yi, yj) - radius, 0))
    #     y_top = int(min(max(zi, zj) + radius, 32 - 1))
    #     z_down = int(max(min(zi, zj) - radius, 0))
    #     z_top = int(min(max(zi, zj) + radius, 32 - 1))
    #     # Iterate through each point in the envelope and determine if it's within the cylinder
    #     for k in range(z_down, z_top + 1):
    #         for q in range(y_down, y_top + 1):
    #             for p in range(x_down, x_top + 1):
    #                 # Calculate the distance from the line segment using the point-to-line distance formula
    #                 norms10 = (xi - p) ** 2 + (yi - q) ** 2 + (zi - k) ** 2
    #                 norms21 = (xj - xi) ** 2 + (yj - yi) ** 2 + (zj - zi) ** 2
    #                 dots1021 = (xi - p) * (xj - xi) + (yi - q) * (yj - yi) + (zi - k) * (zj - zi)
    #                 dist = numpy.sqrt(norms10 - (dots1021 ** 2) / norms21 if norms21 else norms10)
    #                 t1 = -dots1021 / norms21 if norms21 else 0
    #                 if t1 < 0:
    #                     dist = numpy.sqrt(norms10)
    #                 elif t1 > 1:
    #                     dist = numpy.sqrt((xj - p) ** 2 + (yj - q) ** 2 + (zj - k) ** 2)
    #                 # Calculate the varying radius along the line segment if the radii are different
    #                 if dist <= radius:
    #                     xn_idx.append(p)
    #                     yn_idx.append(q)
    #                     zn_idx.append(k)

    img[zn_idx, yn_idx, xn_idx] = 255

    img = numpy.expand_dims(img, axis=0)
    pbd.save(save_path, img)


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

def get_imagenumber_2_v3dpbd_path(dir_path):
    dict = {}
    for dir in os.listdir(dir_path):
        if not dir.startswith("human_brain"):
            continue
        sub_dir_path = os.path.join(dir_path, dir)
        # 使用 os.walk 递归遍历文件夹及其子文件夹
        for root, dirs, files in os.walk(sub_dir_path):
            for file in files:
                if file.endswith('.v3dpbd'):
                    parts = file.split('_')
                    image_number = parts[0]
                    dict[image_number] = os.path.join(root, file)
    return dict

def get_image_number_2_maxRes(dir_path, res_dict=None):
    if res_dict == None:
        res_dict = {}
    for filename in os.listdir(dir_path):
        if not os.path.isdir(os.path.join(dir_path, filename)):
            continue
        image_number = filename.split('_')[0] + "_synthetic"

        resList = []
        for r in os.listdir(os.path.join(dir_path, filename)):
            resolutionPath = os.path.join(dir_path, filename, r)
            if not os.path.isdir(resolutionPath):
                continue
            y = int((r.split('x'))[1])
            ry = []
            ry.append(r)
            ry.append(y)
            resList.append(ry)
        if len(resList) < 2:
            continue
        resList.sort(key=lambda x: x[1], reverse=True)
        resolutions = [list[0] for list in resList]
        res_dict[image_number] = resolutions[0]
    return res_dict

def get_image_number_2_maxRes_and_imageName(dir_path, image_name_dict=None, res_dict=None):
    if res_dict == None:
        res_dict = {}
    if image_name_dict == None:
        image_name_dict = {}
    for filename in os.listdir(dir_path):
        if not os.path.isdir(os.path.join(dir_path, filename)):
            continue
        image_number = filename.split('_')[0]
        image_name_dict[image_number] = filename
        res_dict[image_number] = filename
        resList = []
        for r in os.listdir(os.path.join(dir_path, filename)):
            resolutionPath = os.path.join(dir_path, filename, r)
            if not os.path.isdir(resolutionPath):
                continue
            y = int((r.split('x'))[1])
            ry = []
            ry.append(r)
            ry.append(y)
            resList.append(ry)
        if len(resList) < 2:
            continue
        resList.sort(key=lambda x: x[1], reverse=True)
        resolutions = [list[0] for list in resList]
        res_dict[image_number] = resolutions[0]
    return res_dict, image_name_dict

def get_random_swc_files(directory, num_files):
    # 获取文件夹中所有的文件（不包括子文件夹中的文件）
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # 随机选择指定数量的文件
    if len(all_files) < num_files:
        raise ValueError(f"文件夹中的文件少于 {num_files} 个")

    random_files = random.sample(all_files, num_files)

    return random_files

def add_prefix(root, prefix):
    for file in os.listdir(root):
        if file.endswith(".v3dpbd"):
            continue
        file_path = os.path.join(root, file)
        os.rename(file_path, file_path + prefix)

def get_swc_removed_image(swc_path, target_image_path, swc_removed_image_path, xshape, yshape, zshape):
    radius = 3
    xl_idx, yl_idx, zl_idx = [], [], []
    # all_coor_list = read_swc(swc_path)
    # print(all_coor_list)
    tree = parse_swc(swc_path)
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
    pbd = PBD()
    target_image = pbd.load(target_image_path)
    for (xi, yi, zi) in zip(xn_idx, yn_idx, zn_idx):
        target_image[0][zi][yi][xi] = 0
    pbd.save(swc_removed_image_path, target_image)

def get_swc_nearby_image(swc_path, target_image_path, swc_nearby_image_path, xshape, yshape, zshape):
    radius = 15
    xl_idx, yl_idx, zl_idx = [], [], []
    # all_coor_list = read_swc(swc_path)
    # print(all_coor_list)
    tree = parse_swc(swc_path)
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
    pbd = PBD()
    target_image = pbd.load(target_image_path)
    img = numpy.zeros((zshape, yshape, xshape), dtype=numpy.uint8)

    img[zn_idx, yn_idx, xn_idx] = target_image[0][zn_idx, yn_idx, xn_idx]
    img = numpy.expand_dims(img, axis=0)
    pbd.save(swc_nearby_image_path, img)

if __name__ == '__main__':
    # 匹配模式
    # pattern = r"\d+_\d+_\d+"
    # root_dir_path = r'D:\data\2024_07_14\sample\missing'
    # for dirpath, dirnames, filenames in os.walk(root_dir_path):
    #     for dirname in dirnames:
    #         full_dir_path = os.path.join(dirpath, dirname)
    #         match = re.search(pattern, dirname)
    #         if match:
    #             generate_predict_skeleton(full_dir_path)

    swc_dir_path = r'Z:\SEU-ALLEN\Projects\Human_Neurons\Different_versions_human_dendrite_reconstructed\humanNeuron_manual\humanNeuron_all_swc_manual_Vaa3D&CAR_latestVersion\all_swc_sorted\swc'
    swc_converted_img_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\swcConvertedImage'
    target_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\targetImageWhole_sup2'
    image_v3dpbd_dir_path = r'Z:\SEU-ALLEN\Projects\Human_Neurons\all_human_cells\all_human_cells_v3dpbd'
    image_terafly_dir_path = r'Z:\SEU-ALLEN\Users\zhy\Human_Neuron_terafly'
    image_terafly_add_dir_path = r'Z:\SEU-ALLEN\Projects\Human_Neurons\all_human_cells_terafly_add\terafly'
    swc_removed_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\swcRemovedImage'
    swc_nearby_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\swcNearbyImage'
    res_dict_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\res_dict.json'

    # res_dict, image_name_dict = get_image_number_2_maxRes_and_imageName(image_terafly_dir_path)
    # res_dict, image_name_dict = get_image_number_2_maxRes_and_imageName(image_terafly_add_dir_path, image_name_dict, res_dict)

    # with open(res_dict_path, 'w') as json_file:
        # json.dump(res_dict, json_file)
    with open(res_dict_path, 'r') as json_file:
        res_dict = json.load(json_file)

    # v3dimg_dict = get_imagenumber_2_v3dpbd_path(image_v3dpbd_dir_path)
    # tobe_selected_swc_list = get_random_swc_files(swc_dir_path, 800)
    #
    # count = 0
    # for swc_path in tobe_selected_swc_list:
    #     swc_name = os.path.basename(swc_path)
    #     image_number = swc_name.split('_')[0]
    #     if not image_number in res_dict:
    #         continue
    #     res_parts = res_dict[image_number].split('x')
    #     zshape = int(res_parts[2][:-1])
    #     yshape = int(res_parts[0][4:])
    #     xshape = int(res_parts[1])
    #     if zshape < 128 or xshape != 512 or yshape != 512:
    #         continue
    #     tree = parse_swc(swc_path)
    #     if tree[0][0] != 1:
    #         continue
    #
    #     save_path = os.path.join(swc_converted_img_dir_path, image_name_dict[image_number] + "_swcConverted.v3dpbd")
    #     generate_predict_skeleton(swc_path, save_path, zshape, yshape, xshape, 2.0)
    #
    #     target_src_path = v3dimg_dict[image_number]
    #     target_des_path = os.path.join(target_image_dir_path, image_name_dict[image_number] + ".v3dpbd")
    #     # 复制文件
    #     shutil.copy(target_src_path, target_des_path)
    #
    #     count += 1
    #     if count >= 200:
    #         break

    # swc_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\swc\10793_P040_T01_-_S005_1dAFTsur_MTG_stamp_2024_01_12_14_51.ano.eswc'
    # save_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\image\10793_P040_T01_-_S005_1dAFTsur_MTG.L_R0613_OMZ_20230712_YW_synthetic.v3dpbd'
    # generate_predict_skeleton(swc_path, save_path, 197, 1430, 978)

    # root_dir_path = r'C:\Users\penglab\Desktop\2024_07_22_17_17_40'
    # data_pre_augment(root_dir_path)

    human_bronze_swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\human\swc_bronze_standard'
    human_silver_swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\human\swc_silver_standard'
    human_gold_swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\human\swc_gold_standard'
    human_bronze_skeleton_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\human\skeleton_bronze'
    human_silver_skeleton_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\human\skeleton_silver'
    human_gold_skeleton_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\human\skeleton_gold'
    synthetic_bronze_swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\synthetic\swc_bronze_standard'
    synthetic_silver_swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\synthetic\swc_silver_standard'
    synthetic_gold_swc_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\synthetic\swc_gold_standard'
    synthetic_bronze_skeleton_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\synthetic\skeleton_bronze'
    synthetic_silver_skeleton_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\synthetic\skeleton_silver'
    synthetic_gold_skeleton_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\synthetic\skeleton_gold'

    human_image_origin_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\human\image_origin'
    synthetic_image_origin_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\for_M3D\synthetic\image_origin'
    synthetic_terafly_img_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\synthetic_human_image_addsoma_terafly'

    res_dict = get_image_number_2_maxRes(synthetic_terafly_img_dir_path, res_dict)

    human_v3dpbd_name_dict = {}
    for img in os.listdir(human_image_origin_dir_path):
        if img.endswith('v3dpbd'):
            img_path = os.path.join(human_image_origin_dir_path, img)
            image_name = img.split('_')[0]
            human_v3dpbd_name_dict[image_name] = img[:-len(".v3dpbd")]

    synthetic_v3dpbd_name_dict = {}
    for img in os.listdir(synthetic_image_origin_dir_path):
        if img.endswith('v3dpbd'):
            img_path = os.path.join(synthetic_image_origin_dir_path, img)
            image_name = img.split('_')[0] + "_synthetic"
            synthetic_v3dpbd_name_dict[image_name] = img[:-len(".v3dpbd")]

    for bronze_swc_name, silver_swc_name, gold_swc_name in zip(os.listdir(human_bronze_swc_dir_path), os.listdir(human_silver_swc_dir_path), os.listdir(human_gold_swc_dir_path)):
        image_number = bronze_swc_name.split('_')[0]
        if not image_number in res_dict:
            continue
        res_parts = res_dict[image_number].split('x')
        zshape = int(res_parts[2][:-1])
        yshape = int(res_parts[0][4:])
        xshape = int(res_parts[1])
        # if zshape < 128 or xshape != 512 or yshape != 512:
        #     continue
        bronze_swc_path = os.path.join(human_bronze_swc_dir_path, bronze_swc_name)
        silver_swc_path = os.path.join(human_silver_swc_dir_path, silver_swc_name)
        gold_swc_path = os.path.join(human_gold_swc_dir_path, gold_swc_name)

        bronze_tree = parse_swc(bronze_swc_path)
        silver_tree = parse_swc(silver_swc_path)
        gold_tree = parse_swc(gold_swc_path)

        bronze_save_path = os.path.join(human_bronze_skeleton_dir_path, human_v3dpbd_name_dict[image_number] + "_skeleton.v3dpbd")
        silver_save_path = os.path.join(human_silver_skeleton_dir_path,
                                        human_v3dpbd_name_dict[image_number] + "_skeleton.v3dpbd")
        gold_save_path = os.path.join(human_gold_skeleton_dir_path,
                                        human_v3dpbd_name_dict[image_number] + "_skeleton.v3dpbd")

        if os.path.exists(bronze_save_path):
            continue

        generate_predict_skeleton(bronze_swc_path, bronze_save_path, zshape, yshape, xshape, 1.5)
        generate_predict_skeleton(silver_swc_path, silver_save_path, zshape, yshape, xshape, 1.5)
        generate_predict_skeleton(gold_swc_path, gold_save_path, zshape, yshape, xshape, 1.5)

    # for bronze_swc_name, silver_swc_name, gold_swc_name in zip(os.listdir(synthetic_bronze_swc_dir_path), os.listdir(synthetic_silver_swc_dir_path), os.listdir(synthetic_gold_swc_dir_path)):
    #     image_number = bronze_swc_name.split('_')[0] + "_synthetic"
    #     if not image_number in res_dict:
    #         continue
    #     res_parts = res_dict[image_number].split('x')
    #     zshape = int(res_parts[2][:-1])
    #     yshape = int(res_parts[0][4:])
    #     xshape = int(res_parts[1])
    #     # if zshape < 128 or xshape != 512 or yshape != 512:
    #     #     continue
    #     bronze_swc_path = os.path.join(synthetic_bronze_swc_dir_path, bronze_swc_name)
    #     silver_swc_path = os.path.join(synthetic_silver_swc_dir_path, silver_swc_name)
    #     gold_swc_path = os.path.join(synthetic_gold_swc_dir_path, gold_swc_name)
    #
    #     bronze_tree = parse_swc(bronze_swc_path)
    #     silver_tree = parse_swc(silver_swc_path)
    #     gold_tree = parse_swc(gold_swc_path)
    #
    #     bronze_save_path = os.path.join(synthetic_bronze_skeleton_dir_path, synthetic_v3dpbd_name_dict[image_number] + "_skeleton.v3dpbd")
    #     silver_save_path = os.path.join(synthetic_silver_skeleton_dir_path,
    #                                     synthetic_v3dpbd_name_dict[image_number] + "_skeleton.v3dpbd")
    #     gold_save_path = os.path.join(synthetic_gold_skeleton_dir_path,
    #                                     synthetic_v3dpbd_name_dict[image_number] + "_skeleton.v3dpbd")
    #
    #     generate_predict_skeleton(bronze_swc_path, bronze_save_path, zshape, yshape, xshape, 1.5)
    #     generate_predict_skeleton(silver_swc_path, silver_save_path, zshape, yshape, xshape, 1.5)
    #     generate_predict_skeleton(gold_swc_path, gold_save_path, zshape, yshape, xshape, 1.5)

    # for target_image in os.listdir(target_image_dir_path):
    #     image_name = target_image.split("_")[0]
    #     res_parts = res_dict[image_name].split('x')
    #     zshape = int(res_parts[2][:-1])
    #     yshape = int(res_parts[0][4:])
    #     xshape = int(res_parts[1])
    #     target_image_path = os.path.join(target_image_dir_path, target_image)
    #     swc_path = swc_dict[image_name]
    #     swc_nearby_image_path = os.path.join(swc_nearby_image_dir_path, v3dpbd_name_dict[image_name])
    #     get_swc_nearby_image(swc_path, target_image_path, swc_nearby_image_path, xshape, yshape, zshape)