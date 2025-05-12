import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain

from matplotlib.ticker import ScalarFormatter, FuncFormatter


def process_file(file_path):
    angles_collection = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()
        file_name = ''
        for i in range(0, len(lines)):
            if lines[i] == "":
                continue
            if "swc" in lines[i]:
                file_name = lines[i].strip()  # 文件名
                continue
            angles_line = lines[i].strip()  # 第二行是数字
            # 将数字转换为列表，如果没有数字则为一个空列表
            angles = list(map(float, angles_line.split()))
            # 收集到字典中
            angles_collection[file_name] = angles

    return angles_collection

BBP_file_path = 'D:\source\C++Projects\AngleDetector\output\BBP_Defined_Swc.txt'  # 替换为你的文件路径
human_file_path = 'D:\source\C++Projects\AngleDetector\output\human_neuron_swc.txt'
BBP_angles = process_file(BBP_file_path)
human_angles = process_file(human_file_path)
merged_angles = {**BBP_angles, **human_angles}
# 使用 itertools.chain
BBP_list = list(chain.from_iterable(BBP_angles.values()))
human_list = list(chain.from_iterable(human_angles.values()))
merged_list = list(chain.from_iterable(merged_angles.values()))

BBP_lt_90_list = [degree for degree in BBP_list if degree <= 90]
human_lt_90_list = [degree for degree in human_list if degree <= 90]
print(len(BBP_lt_90_list) / len(BBP_list))
print(len(human_lt_90_list) / len(human_list))
print(len(BBP_list))
print(len(human_list))
z_mouse = (len(BBP_lt_90_list) / len(BBP_list) - 0.91) / ((0.91 * (1 - 0.91) / len(BBP_list)) ** 0.5)
z_human = (len(human_lt_90_list) / len(human_list) - 0.97) / ((0.97 * (1 - 0.97) / len(human_list)) ** 0.5)
print(z_mouse)
print(z_human)

# # 打印结果
# for file_name, angles in BBP_angles.items():
#     print(f"filename: {file_name}, angles: {angles}")

# matplotlib.use('TkAgg')
# plt.figure(figsize=(10, 8))
#
# # 定义角度范围和组
# bins = np.arange(0, 190, 10)  # 0-180 度，每 10 度为一组
# x_set = np.arange(0, 181, 30)
#
# # 计算每组的数量
# counts, _ = np.histogram(BBP_list, bins=bins)
#
# # 绘制柱状图
# plt.bar(bins[:-1], counts, width=10, align='edge', edgecolor='white', color=(121/255, 182/255, 163/255))
#
# # 在每个柱子上方显示数量
# for i, count in enumerate(counts):
#     plt.text(bins[i] + 6, count, str(count), ha='center', va='bottom', rotation=60, fontsize=20)
#
# plt.xticks(np.arange(0, 181, 30), fontsize=28)
# plt.xlim(0, 185)  # 根据需要调整范围
# plt.yticks(fontsize=28)
#
# # 自定义 y 轴格式，显示为 0.01 倍并保留一位小数
# def format_y_axis(x, pos):
#     return f"{x * 0.0001:.1f}"
#
# # plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y_axis))
# # 设置 y 轴以科学计数法显示
# # plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
# # 添加标签和标题
# plt.xlabel('Angle', fontsize=28)
# plt.ylabel('Number of branching pairs', fontsize=28)
#
# # 移除图形边框
# for spine in plt.gca().spines.values():
#     if spine.spine_type in ['top', 'right']:
#         spine.set_visible(False)
#
# # 显示图形
# # plt.grid(axis='y')
# plt.tight_layout()
# plt.show()
