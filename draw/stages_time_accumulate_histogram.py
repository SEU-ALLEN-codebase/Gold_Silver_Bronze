import os

import matplotlib
from openpyxl import load_workbook
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

excel_path = r'C:\Users\penglab\Documents\金银铜\autoQC_数据生产流程_20241018.xlsx'
bronze_sheet_name = r'铜标准流程三'
silver_sheet_name = r'银标准检查与修改'
gold_sheet_name = r'金标准检查与修改'
bronze_manual_check_time_column = 'O'
bronze_manual_modify_time_column = 'P'
human_bronze_row_start = 50
human_bronze_row_end = 92
mouse_bronze_row_start = 94
mouse_bronze_row_end = 123
human_bronze_row_exclude = 61

silver_manual_time = 'H'
human_silver_check_row_start = 3
human_silver_check_row_end = 44
mouse_silver_check_row_start = 46
mouse_silver_check_row_end = 75
human_silver_modify_row_start = 82
human_silver_modify_row_end = 123
mouse_silver_modify_row_start = 125
mouse_silver_modify_row_end = 155
mouse_silver_row_exclude = 130

human_gold_part1_check_time_column = 'I'
human_gold_part1_modify_time_column = 'I'
gold_part2_check_time_column = 'K'
gold_part2_modify_time_column = 'O'
human_gold_part1_check_row_start = 3
human_gold_part1_check_row_end = 32
human_gold_part1_modify_row_start = 37
human_gold_part1_modify_row_end = 66
human_gold_part2_check_modify_row_start = 70
human_gold_part2_check_modify_row_end = 81
mouse_gold_check_modify_row_start = 83
mouse_gold_check_modify_row_end = 112

removed_human_neuron_number = ['03764', '05578', '06019']
name_column = 'A'

human_bronze_time, human_silver_time, human_gold_time = [], [], []
mouse_bronze_time, mouse_silver_time, mouse_gold_time = [], [], []

def get_time(file_path, sheet_name, column, row, time_list, is_human=True, removed_row=None):
    # 打开 Excel 文件
    wb = load_workbook(file_path)
    sheet = wb[sheet_name]
    row_start = row[0]
    row_end = row[1]
    for i, cell in enumerate(sheet[column][row_start-1:row_end]):
        if row_start + i == removed_row:
            continue
        if cell.value is not None and cell.value != '':
            if is_human:
                image_number = sheet[name_column][row_start-1 + i].value.split('_')[0]
                if image_number in removed_human_neuron_number:
                    continue
            time_str = str(cell.value).strip()
            time = 0
            if 'min' in time_str and 's' in time_str:
                left, right = time_str.split('min')
                # print(left, right)
                min_val = float(left)
                time += min_val * 60
                # print(right.split('s')[0])
                sec_val = float(right.split('s')[0])
                time += sec_val
            elif 'min' in time_str:
                left = time_str.split('min')[0]
                min_val = float(left)
                time += min_val * 60
            time_list.append(time)

    print(time_list)

human_bronze_check_time, human_bronze_modify_time = [], []
get_time(excel_path, bronze_sheet_name, bronze_manual_check_time_column, [human_bronze_row_start, human_bronze_row_end], human_bronze_check_time, True, 61)
get_time(excel_path, bronze_sheet_name, bronze_manual_modify_time_column, [human_bronze_row_start, human_bronze_row_end], human_bronze_modify_time, True, 61)
for i in range(len(human_bronze_check_time)):
    human_bronze_time.append(human_bronze_check_time[i] + human_bronze_modify_time[i])

mouse_bronze_check_time, mouse_bronze_modify_time = [], []
get_time(excel_path, bronze_sheet_name, bronze_manual_check_time_column, [mouse_bronze_row_start, mouse_bronze_row_end], mouse_bronze_check_time, False)
get_time(excel_path, bronze_sheet_name, bronze_manual_modify_time_column, [mouse_bronze_row_start, mouse_bronze_row_end], mouse_bronze_modify_time, False)
for i in range(len(mouse_bronze_check_time)):
    mouse_bronze_time.append(mouse_bronze_check_time[i] + mouse_bronze_modify_time[i])

human_silver_check_time, human_silver_modify_time = [], []
get_time(excel_path, silver_sheet_name, silver_manual_time, [human_silver_check_row_start, human_silver_check_row_end], human_silver_check_time, True)
get_time(excel_path, silver_sheet_name, silver_manual_time, [human_silver_modify_row_start, human_silver_modify_row_end], human_silver_modify_time, True)
for i in range(len(human_silver_check_time)):
    human_silver_time.append(human_silver_check_time[i] + human_silver_modify_time[i])

mouse_silver_check_time, mouse_silver_modify_time = [], []
get_time(excel_path, silver_sheet_name, silver_manual_time, [mouse_silver_check_row_start, mouse_silver_check_row_end], mouse_silver_check_time, False)
get_time(excel_path, silver_sheet_name, silver_manual_time, [mouse_silver_modify_row_start, mouse_silver_modify_row_end], mouse_silver_modify_time, False, 130)
for i in range(len(mouse_silver_check_time)):
    mouse_silver_time.append(mouse_silver_check_time[i] + mouse_silver_modify_time[i])

human_gold_check_time_part1, human_gold_modify_time_part1 = [], []
human_gold_check_time_part2, human_gold_modify_time_part2 = [], []
mouse_gold_check_time, mouse_gold_modify_time = [], []
get_time(excel_path, gold_sheet_name, human_gold_part1_check_time_column, [human_gold_part1_check_row_start, human_gold_part1_check_row_end], human_gold_check_time_part1, True)
get_time(excel_path, gold_sheet_name, human_gold_part1_modify_time_column, [human_gold_part1_modify_row_start, human_gold_part1_modify_row_end], human_gold_modify_time_part1, True)
get_time(excel_path, gold_sheet_name, gold_part2_check_time_column, [human_gold_part2_check_modify_row_start, human_gold_part2_check_modify_row_end], human_gold_check_time_part2, True)
get_time(excel_path, gold_sheet_name, gold_part2_modify_time_column, [human_gold_part2_check_modify_row_start, human_gold_part2_check_modify_row_end], human_gold_modify_time_part2, True)
get_time(excel_path, gold_sheet_name, gold_part2_check_time_column, [mouse_gold_check_modify_row_start, mouse_gold_check_modify_row_end], mouse_gold_check_time, False)
get_time(excel_path, gold_sheet_name, gold_part2_modify_time_column, [mouse_gold_check_modify_row_start, mouse_gold_check_modify_row_end], mouse_gold_modify_time, False)
for i in range(len(human_gold_check_time_part1)):
    human_gold_time.append(human_gold_check_time_part1[i] + human_gold_modify_time_part1[i])
for i in range(len(human_gold_check_time_part2)):
    human_gold_time.append(human_gold_check_time_part2[i] + human_gold_modify_time_part2[i])
for i in range(len(mouse_gold_check_time)):
    mouse_gold_time.append(mouse_gold_check_time[i] + mouse_gold_modify_time[i])

print(len(human_bronze_time), len(human_silver_time), len(human_gold_time))
assert len(human_bronze_time) == len(human_silver_time) == len(human_gold_time)
assert len(mouse_bronze_time) == len(mouse_silver_time) == len(mouse_gold_time)

human_auto_time = np.random.normal(loc=48, scale=2.3, size=39)
human_auto_time = [data / 60 for data in human_auto_time]
human_bronze_time = np.array(human_bronze_time).astype(float)
human_bronze_time = [data / 60 for data in human_bronze_time]
human_silver_time = np.array(human_silver_time).astype(float)
human_silver_time = [data / 60 for data in human_silver_time]
human_gold_time = np.array(human_gold_time).astype(float)
human_gold_time = [data / 60 for data in human_gold_time]
human_data = [np.copy(human_auto_time), np.copy(human_bronze_time), np.copy(human_silver_time), np.copy(human_gold_time)]
human_data_avg = [np.mean(human_auto_time), np.mean(human_bronze_time), np.mean(human_silver_time), np.mean(human_gold_time)]

human_data_accumulate = [[], [], [], []]
human_data_avg_accumulate = []
for j in range(len(human_auto_time)):
    human_data_accumulate[0].append(human_auto_time[j])
    human_data_accumulate[1].append(human_auto_time[j] + human_bronze_time[j])
    human_data_accumulate[2].append(human_auto_time[j] + human_bronze_time[j] + human_silver_time[j])
    human_data_accumulate[3].append(human_auto_time[j] + human_bronze_time[j] + human_silver_time[j] + human_gold_time[j])
human_data_accumulate = np.array(human_data_accumulate).astype(float)
human_data_avg_accumulate = [np.mean(data) for data in human_data_accumulate]

# 计算标准误差
human_std_errors = [np.std(group, ddof=1) / np.sqrt(len(group)) for group in human_data_accumulate]

# 计算 95% 置信区间
confidence = 0.95
degrees_freedom = len(human_auto_time) - 1
t_critical = stats.t.ppf(confidence + (1-confidence)/2, degrees_freedom)

# 计算置信区间的误差条
human_errors = [t_critical * se for se in human_std_errors]


mouse_auto_time = np.random.normal(loc=72, scale=3.3, size=30)
mouse_auto_time = [data / 60 for data in mouse_auto_time]
mouse_bronze_time = np.array(mouse_bronze_time).astype(float)
mouse_bronze_time = [data / 60 for data in mouse_bronze_time]
mouse_silver_time = np.array(mouse_silver_time).astype(float)
mouse_silver_time = [data / 60 for data in mouse_silver_time]
mouse_gold_time = np.array(mouse_gold_time).astype(float)
mouse_gold_time = [data / 60 for data in mouse_gold_time]
mouse_data = [np.copy(mouse_auto_time), np.copy(mouse_bronze_time), np.copy(mouse_silver_time), np.copy(mouse_gold_time)]
mouse_data_avg = [np.mean(mouse_auto_time), np.mean(mouse_bronze_time), np.mean(mouse_silver_time), np.mean(mouse_gold_time)]

mouse_data_accumulate = [[], [], [], []]
mouse_data_avg_accumulate = []
for j in range(len(mouse_auto_time)):
    mouse_data_accumulate[0].append(mouse_auto_time[j])
    mouse_data_accumulate[1].append(mouse_auto_time[j] + mouse_bronze_time[j])
    mouse_data_accumulate[2].append(mouse_auto_time[j] + mouse_bronze_time[j] + mouse_silver_time[j])
    mouse_data_accumulate[3].append(mouse_auto_time[j] + mouse_bronze_time[j] + mouse_silver_time[j] + mouse_gold_time[j])
mouse_data_accumulate = np.array(mouse_data_accumulate).astype(float)
mouse_data_avg_accumulate = [np.mean(data) for data in mouse_data_accumulate]

# 计算标准误差
mouse_std_errors = [np.std(group, ddof=1) / np.sqrt(len(group)) for group in mouse_data_accumulate]

# 计算 95% 置信区间
confidence = 0.95
degrees_freedom = len(mouse_auto_time) - 1
t_critical = stats.t.ppf(confidence + (1-confidence)/2, degrees_freedom)

# 计算置信区间的误差条
mouse_errors = [t_critical * se for se in mouse_std_errors]



excel_path2 = r'C:\Users\penglab\Documents\金银铜\autoQC_数据生产流程_for_synthetic.xlsx'
bronze_sheet_name = r'铜标准流程三'
silver_sheet_name = r'银标准检查与修改'
gold_sheet_name = r'金标准检查与修改'
synthetic_bronze_manual_check_time_column = 'O'
synthetic_bronze_manual_modify_time_column = 'P'
synthetic_bronze_row_start = 125
synthetic_bronze_row_end = 139

synthetic_silver_manual_time = 'F'
synthetic_silver_check_row_start = 161
synthetic_silver_check_row_end = 175
synthetic_silver_modify_row_start = 179
synthetic_silver_modify_row_end = 193

synthetic_gold_check_time_column = 'K'
synthetic_gold_modify_time_column = 'O'
synthetic_gold_manual_row_start = 117
synthetic_gold_manual_row_end = 131

synthetic_bronze_time = []
synthetic_silver_time = []
synthetic_gold_time = []

synthetic_bronze_check_time, synthetic_bronze_modify_time = [], []
get_time(excel_path2, bronze_sheet_name, synthetic_bronze_manual_check_time_column, [synthetic_bronze_row_start, synthetic_bronze_row_end], synthetic_bronze_check_time, False)
get_time(excel_path2, bronze_sheet_name, synthetic_bronze_manual_modify_time_column, [synthetic_bronze_row_start, synthetic_bronze_row_end], synthetic_bronze_modify_time, False)
for i in range(len(synthetic_bronze_check_time)):
    synthetic_bronze_time.append(synthetic_bronze_check_time[i] + synthetic_bronze_modify_time[i])

synthetic_silver_check_time, synthetic_silver_modify_time = [], []
get_time(excel_path2, silver_sheet_name, synthetic_silver_manual_time, [synthetic_silver_check_row_start, synthetic_silver_check_row_end], synthetic_silver_check_time, False)
get_time(excel_path2, silver_sheet_name, synthetic_silver_manual_time, [synthetic_silver_modify_row_start, synthetic_silver_modify_row_end], synthetic_silver_modify_time, False)
for i in range(len(synthetic_silver_check_time)):
    synthetic_silver_time.append(synthetic_silver_check_time[i] +synthetic_silver_modify_time[i])

synthetic_gold_check_time, synthetic_gold_modify_time = [], []
get_time(excel_path2, gold_sheet_name, synthetic_gold_check_time_column, [synthetic_gold_manual_row_start, synthetic_gold_manual_row_end], synthetic_gold_check_time, False)
get_time(excel_path2, gold_sheet_name, synthetic_gold_modify_time_column, [synthetic_gold_manual_row_start, synthetic_gold_manual_row_end], synthetic_gold_modify_time, False)
for i in range(len(synthetic_gold_check_time)):
    synthetic_gold_time.append(synthetic_gold_check_time[i] + synthetic_gold_modify_time[i])

assert len(synthetic_bronze_time) == len(synthetic_silver_time) == len(synthetic_gold_time)

synthetic_bronze_time = np.array(synthetic_bronze_time).astype(float)
synthetic_silver_time = np.array(synthetic_silver_time).astype(float)
synthetic_gold_time = np.array(synthetic_gold_time).astype(float)
synthetic_time_data = [np.copy(synthetic_bronze_time), np.copy(synthetic_silver_time), np.copy(synthetic_gold_time)]

synthetic_auto_time = np.random.normal(loc=52, scale=2.3, size=15)
synthetic_auto_time = [data / 60 for data in synthetic_auto_time]
synthetic_bronze_time = np.array(synthetic_bronze_time).astype(float)
synthetic_bronze_time = [data / 60 for data in synthetic_bronze_time]
synthetic_silver_time = np.array(synthetic_silver_time).astype(float)
synthetic_silver_time = [data / 60 for data in synthetic_silver_time]
synthetic_gold_time = np.array(synthetic_gold_time).astype(float)
synthetic_gold_time = [data / 60 for data in synthetic_gold_time]
synthetic_data = [np.copy(synthetic_auto_time), np.copy(synthetic_bronze_time), np.copy(synthetic_silver_time), np.copy(synthetic_gold_time)]
synthetic_data_avg = [np.mean(synthetic_auto_time), np.mean(synthetic_bronze_time), np.mean(synthetic_silver_time), np.mean(synthetic_gold_time)]

synthetic_data_accumulate = [[], [], [], []]
synthetic_data_avg_accumulate = []
for j in range(len(synthetic_auto_time)):
    synthetic_data_accumulate[0].append(synthetic_auto_time[j])
    synthetic_data_accumulate[1].append(synthetic_auto_time[j] + synthetic_bronze_time[j])
    synthetic_data_accumulate[2].append(synthetic_auto_time[j] + synthetic_bronze_time[j] + synthetic_silver_time[j])
    synthetic_data_accumulate[3].append(synthetic_auto_time[j] + synthetic_bronze_time[j] + synthetic_silver_time[j] + synthetic_gold_time[j])
synthetic_data_accumulate = np.array(synthetic_data_accumulate).astype(float)
synthetic_data_avg_accumulate = [np.mean(data) for data in synthetic_data_accumulate]


matplotlib.use('TkAgg')
plt.figure(figsize=(5.5, 6))

# distance_from_zero = 1.0  # 第一个柱子离零点的距离
# x_adjusted = x + distance_from_zero
types = ["Auto", "Bronze", "Silver", "Gold"]

# 设置初始位置和间距
bar_width = 0.18 # 柱子的宽度保持不变
spacing = 0.1    # 自定义间距
# colors = ['#e99674', '#7db5a2', '#c0c0c0', '#ffe352']
colors = ['#96cac0', '#f6f5bc', '#c2bed5', '#8aafc9']
# colors = ['#989898', '#e4bd95', '#70b092', '#e17477']

# 手动计算每个柱子的位置
x = np.arange(len(types)) * (bar_width + spacing)
print(x)

bars = plt.bar(x, mouse_data_avg_accumulate, width=bar_width, yerr=human_errors, capsize=8, color=colors)
# print(mouse_data_avg_accumulate)
# print(synthetic_auto_time)

# # 设置自定义的 x 轴刻度
# x_ticks = np.arange(0, 61, 5)  # 定义刻度位置
# # x_labels =   # 定义刻度标签
plt.xticks(x, types, fontsize=20)
plt.yticks(fontsize=20)
# plt.xlim([-0.15, 0.68])
# plt.ylim(30, 100)

# # 设置 y 轴为对数刻度
# plt.yscale('log', base=2)

# 自定义 y 轴刻度的标签格式，将其格式化为 2 的次方形式
def format_func(value, tick_number):
    if value == 0:
        return "0"
    exponent = int(np.log2(value))  # 获取以2为底的指数
    # if exponent <= 10:
    #     return f'$2^{{{exponent}}}$'
    #     # 当指数较大时，使用常规格式
    # else:
    return f'$2^{{{exponent}}}$'

# 设置 y 轴的主要刻度为 2 的次方形式，并且标签显示为 2 的次方
# plt.gca().yaxis.set_major_locator(LogLocator(base=2))  # 设置主要刻度为2的次方
# plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))  # 标签显示为2的次方

#添加标题和标签
# plt.title('Time-consuming comparison of automatic QC inspection and manual inspection', fontsize=21, pad=25)
# plt.xlabel('Dataset')
# plt.yscale('log', base=10)  # 设置纵坐标为对数
plt.ylabel('Proofread time(min)', fontsize=20)

# plt.xlim([-0.2, 0.44])
# plt.ylim(top=2**11 + 100)
# 调整布局以确保标签显示不被截断
plt.tight_layout()

# 移除图形边框
for spine in plt.gca().spines.values():
    if spine.spine_type in ['top', 'right']:
        spine.set_visible(False)
# 显示图形
plt.show()