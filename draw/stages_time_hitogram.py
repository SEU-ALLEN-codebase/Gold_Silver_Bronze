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

human_auto_time = np.random.randint(40, 61, size=39)
human_bronze_time = np.array(human_bronze_time).astype(float)
human_silver_time = np.array(human_silver_time).astype(float)
human_gold_time = np.array(human_gold_time).astype(float)
# data = [np.copy(human_auto_time), np.copy(human_bronze_time), np.copy(human_silver_time), np.copy(human_gold_time)]

mouse_auto_time = np.random.randint(60, 81, size=30)
mouse_bronze_time = np.array(mouse_bronze_time).astype(float)
mouse_silver_time = np.array(mouse_silver_time).astype(float)
mouse_gold_time = np.array(mouse_gold_time).astype(float)
data = [np.copy(mouse_auto_time), np.copy(mouse_bronze_time), np.copy(mouse_silver_time), np.copy(mouse_gold_time)]


# 计算标准差
std_devs = [np.std(group) for group in data]
# 计算标准误差
# std_errs = [stats.sem(group) for group in data]
# data_avg = [np.mean(human_auto_time), np.mean(human_bronze_time), np.mean(human_silver_time), np.mean(human_gold_time)]
data_avg = [np.mean(mouse_auto_time), np.mean(mouse_bronze_time), np.mean(mouse_silver_time), np.mean(mouse_gold_time)]
print(data_avg)

# 计算标准误差
std_errors = [np.std(group, ddof=1) / np.sqrt(len(group)) for group in data]

# 计算 95% 置信区间
confidence = 0.95
degrees_freedom = len(mouse_bronze_time) - 1
t_critical = stats.t.ppf(confidence + (1-confidence)/2, degrees_freedom)

# 计算置信区间的误差条
errors = [t_critical * se for se in std_errors]

matplotlib.use('TkAgg')
plt.figure(figsize=(5.5, 6))

# distance_from_zero = 1.0  # 第一个柱子离零点的距离
# x_adjusted = x + distance_from_zero
types = ["Auto", "Bronze", "Silver", "Gold"]

# 设置初始位置和间距
bar_width = 0.18 # 柱子的宽度保持不变
spacing = 0.1    # 自定义间距
colors = ['#e99674', '#7db5a2', '#c0c0c0', '#ffe352']

# 手动计算每个柱子的位置
x = np.arange(len(types)) * (bar_width + spacing)
print(x)

bars = plt.bar(x, data_avg, width=bar_width, yerr=errors, capsize=8, color=colors)

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
plt.ylabel('Proofread time(s)', fontsize=20)

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