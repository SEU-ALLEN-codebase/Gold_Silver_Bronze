import os
import re
import random
import shutil
from multiprocessing import Pool, cpu_count
from v3dpy.loaders import PBD
import numpy

input_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\input_image_has_signal_origin_val_256'
target_image_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\sample\target_image_has_signal_origin_val_256'
swc_converted_img_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\swcNearbyImage'
target_image_whole_dir_path = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\synthetic_image\model_sample\human\targetImageWhole'


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

def process_file(swc_converted_img_name):
    pbd = PBD()
    # 获取patch
    swc_converted_img_path = os.path.join(swc_converted_img_dir_path, swc_converted_img_name)
    # remove_len = len('_swcConverted.v3dpbd')
    remove_len = len('.v3dpbd')
    dir_name = swc_converted_img_name[0:-remove_len]

    # if os.path.exists(os.path.join(input_image_dir_path, dir_name)):
    #     continue

    swc_converted_img = pbd.load(swc_converted_img_path)
    # if swc_converted_img.shape[1] % 2 == 0:
    #     continue
    z_center_img = get_z_center_img(swc_converted_img, 128)
    target_img = pbd.load(os.path.join(target_image_whole_dir_path, dir_name + '.v3dpbd'))
    target_z_center_img = get_z_center_img(target_img, 128)

    shape = z_center_img.shape
    patch_size = 256
    x_split_number = shape[3] // patch_size
    y_split_number = shape[2] // patch_size
    for i in range(x_split_number):
        for j in range(y_split_number):
            patch = z_center_img[:, :, j * patch_size:(j + 1) * patch_size, i * patch_size:(i + 1) * patch_size]
            patch_name = 'x_' + str(i) + '_y_' + str(j) + '.v3dpbd'
            input_image_sub_dir_path = os.path.join(input_image_dir_path, dir_name)
            input_image_patch_path = os.path.join(input_image_sub_dir_path, patch_name)
            if not os.path.exists(input_image_sub_dir_path):
                os.mkdir(os.path.join(input_image_dir_path, dir_name))
                os.mkdir(os.path.join(target_image_dir_path, dir_name))

            if os.path.exists(input_image_patch_path):
                # patch_count += 1
                continue

            signal_count = 0
            for z in range(patch.shape[1]):
                for y in range(patch.shape[2]):
                    for x in range(patch.shape[3]):
                        if patch[:, z, y, x] > 0:
                            signal_count += 1
            print(signal_count)
            if signal_count / (patch_size ** 3) > 0.0005:
                # patch_count += 1
                pbd.save(input_image_patch_path, patch)

                target_image_sub_dir_path = os.path.join(target_image_dir_path, dir_name)
                target_image_patch_path = os.path.join(target_image_sub_dir_path, patch_name)

                target_patch = target_z_center_img[:, :, j * patch_size:(j + 1) * patch_size,
                               i * patch_size:(i + 1) * patch_size]
                pbd.save(target_image_patch_path, target_patch)

if __name__ == '__main__':
    num_processes = cpu_count()
    print(f"Using {num_processes} processes...")
    file_names = [swc_converted_img_name for swc_converted_img_name in os.listdir(swc_converted_img_dir_path)]
    # 创建进程池并分配任务
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_file, file_names)

    # print('patch_count: ' + str(patch_count))
