import matplotlib
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# # 创建示例数据
# np.random.seed(10)
# category_1 = np.random.uniform(0, 1, 30)  # 类别1的数据
# category_2 = np.random.uniform(0, 1, 30)  # 类别2的数据

# 读取 Excel 文件
from openpyxl import load_workbook

exp1_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\eval_human_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
exp1_sheet_name = 'Sheet1'       # 将 'Sheet1' 替换为你的工作表名称
mouse_18454_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\mouse_18454_eval.xlsx'
mouse_7_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\7_mouse_eval.xlsx'
mouse_18454_sheet_name = 'mouse_18454_eval'
mouse_7_sheet_name = '7_mouse_eval'
mouse_all_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\eval_mouse_all.xlsx'
synthetic_15_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\15_synthetic_eval.xlsx'
synthetic_15_sheet_name = '15_synthetic_eval'

name_column = 'A'
auto_precision_column = 'B'
bronze_precision_column = 'C'
silver_precision_column = 'D'

auto_recall_column = 'E'
bronze_recall_column = 'F'
silver_recall_column = 'G'

synthetic_auto_precision_column = 'B'
synthetic_bronze_precision_column = 'C'
synthetic_silver_precision_column = 'D'
synthetic_gold_precision_column = 'E'

synthetic_auto_recall_column = 'F'
synthetic_bronze_recall_column = 'G'
synthetic_silver_recall_column = 'H'
synthetic_gold_recall_column = 'I'

removed_human_neuron_number = ['03764', '05578', '06019']
# exp2_file_path = r'C:\Users\penglab\Documents\金银铜\autoQC_数据生产流程.xlsx'
# exp2_sheet_name = "流程一"
# exp2_column = 'N'

def get_metric(file_path, sheet_name, auto_column, bronze_column, silver_column, gold_column=None, is_human=True):
    # 打开 Excel 文件
    wb = load_workbook(file_path)
    sheet = wb[sheet_name]
    auto_data = []
    count = 0
    for i, cell in enumerate(sheet[auto_column][1:]):
        if sheet[name_column][i + 1].value is not None and sheet[name_column][i + 1].value != '':
            if is_human:
                image_number = sheet[name_column][i + 1].value.split('_')[0]
                if image_number in removed_human_neuron_number:
                    continue
            count += 1
            auto_data.append(float(cell.value))
        else:
            break
    # column_data = [float(cell.value) for cell in sheet[column][1:]]
    print(auto_data)

    bronze_data = []
    for i, cell in enumerate(sheet[bronze_column][1:]):
        if sheet[name_column][i + 1].value is not None and sheet[name_column][i + 1].value != '':
            if is_human:
                image_number = sheet[name_column][i + 1].value.split('_')[0]
                if image_number in removed_human_neuron_number:
                    continue
            bronze_data.append(float(cell.value))
        else:
            break
    # column_data = [float(cell.value) for cell in sheet[column][1:]]
    print(bronze_data)

    silver_data = []
    for i, cell in enumerate(sheet[silver_column][1:]):
        if sheet[name_column][i + 1].value is not None and sheet[name_column][i + 1].value != '':
            if is_human:
                image_number = sheet[name_column][i + 1].value.split('_')[0]
                if image_number in removed_human_neuron_number:
                    continue
            silver_data.append(float(cell.value))
        else:
            break
    # column_data = [float(cell.value) for cell in sheet[column][1:]]
    print(silver_data)

    gold_data = []
    if gold_column is not None:
        for i, cell in enumerate(sheet[gold_column][1:]):
            if sheet[name_column][i + 1].value is not None and sheet[name_column][i + 1].value != '':
                if is_human:
                    image_number = sheet[name_column][i + 1].value.split('_')[0]
                    if image_number in removed_human_neuron_number:
                        continue
                gold_data.append(float(cell.value))
            else:
                break
    # column_data = [float(cell.value) for cell in sheet[column][1:]]
    print(gold_data)

    ground_truth_data = [1.0] * count

    if gold_column is not None:
        return auto_data, bronze_data, silver_data, gold_data, ground_truth_data
    else:
        return auto_data, bronze_data, silver_data, ground_truth_data

auto_data, bronze_data, silver_data, gold_data = get_metric(mouse_all_file_path, mouse_7_sheet_name, auto_recall_column, bronze_recall_column, silver_recall_column, is_human=False)

assert len(auto_data) == len(bronze_data) == len(silver_data) == len(gold_data)

auto_data = [data * 100 for data in auto_data]
bronze_data = [data * 100 for data in bronze_data]
silver_data = [data * 100 for data in silver_data]
gold_data = [data * 100 for data in gold_data]

auto_data = np.array(auto_data).astype(float)
bronze_data = np.array(bronze_data).astype(float)
silver_data = np.array(silver_data).astype(float)
gold_data = np.array(gold_data).astype(float)
data = [np.copy(auto_data), np.copy(bronze_data), np.copy(silver_data), np.copy(gold_data)]
# 计算标准差
std_devs = [np.std(group) for group in data]
# 计算标准误差
# std_errs = [stats.sem(group) for group in data]
data_avg = [np.mean(auto_data), np.mean(bronze_data), np.mean(silver_data), np.mean(gold_data)]
print(data_avg)

# 计算标准误差
std_errors = [np.std(group, ddof=1) / np.sqrt(len(group)) for group in data]

# 计算 95% 置信区间
confidence = 0.95
degrees_freedom = len(auto_data) - 1
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
# colors = ['#e99674', '#7db5a2', '#c0c0c0', '#ffe352']
colors = ['#96cac0', '#f6f5bc', '#c2bed5', '#8aafc9']
# colors = ['#989898', '#e4bd95', '#70b092', '#e17477']
# 手动计算每个柱子的位置
x = np.arange(len(types)) * (bar_width + spacing)
print(x)

bars = plt.bar(x, data_avg, width=bar_width, yerr=errors, capsize=8, color=colors)

# # 设置自定义的 x 轴刻度
# x_ticks = np.arange(0, 61, 5)  # 定义刻度位置
# # x_labels =   # 定义刻度标签
plt.xticks(x, types, fontsize=20)
plt.yticks(fontsize=20)

plt.ylim(0, 100)

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
plt.ylabel('Recall(%)', fontsize=20)

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