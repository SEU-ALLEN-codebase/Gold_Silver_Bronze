import matplotlib
from openpyxl import load_workbook
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

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

matplotlib.use('TkAgg')

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

    return auto_data, bronze_data, silver_data, gold_data, ground_truth_data

auto_data, bronze_data, silver_data, gold_data, ground_truth_data = get_metric(synthetic_15_file_path, synthetic_15_sheet_name, synthetic_auto_precision_column, synthetic_bronze_precision_column, synthetic_silver_precision_column, synthetic_gold_precision_column, False)
auto_recall_data, bronze_recall_data, silver_recall_data, gold_recall_data, ground_truth_recall_data = get_metric(synthetic_15_file_path, synthetic_15_sheet_name, synthetic_auto_recall_column, synthetic_bronze_recall_column, synthetic_silver_recall_column, synthetic_gold_recall_column, False)

stages = ['Auto', 'Bronze', 'Silver', 'Gold']

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

assert len(auto_data) == len(bronze_data) == len(silver_data) == len(gold_data)

auto_recall_data = [data * 100 for data in auto_recall_data]
bronze_recall_data = [data * 100 for data in bronze_recall_data]
silver_recall_data = [data * 100 for data in silver_recall_data]
gold_recall_data = [data * 100 for data in gold_recall_data]

auto_recall_data = np.array(auto_recall_data).astype(float)
bronze_recall_data = np.array(bronze_recall_data).astype(float)
silver_recall_data = np.array(silver_recall_data).astype(float)
gold_recall_data = np.array(gold_recall_data).astype(float)
data_recall = [np.copy(auto_recall_data), np.copy(bronze_recall_data), np.copy(silver_recall_data), np.copy(gold_recall_data)]
# 计算标准差
std_devs_recall = [np.std(group) for group in data_recall]
# 计算标准误差
# std_errs = [stats.sem(group) for group in data]
data_avg_recall = [np.mean(auto_recall_data), np.mean(bronze_recall_data), np.mean(silver_recall_data), np.mean(gold_recall_data)]
print(data_avg_recall)

# 计算标准误差
std_errors_recall = [np.std(group, ddof=1) / np.sqrt(len(group)) for group in data_recall]

# 计算 95% 置信区间
confidence = 0.95
degrees_freedom = len(auto_recall_data) - 1
t_critical = stats.t.ppf(confidence + (1-confidence)/2, degrees_freedom)

# 计算置信区间的误差条
errors_recall = [t_critical * se for se in std_errors_recall]

plt.figure(figsize=(8, 8))

colors = ['#e99674', '#7db5a2', '#c0c0c0', '#ffe352']

plt.plot(data_avg, data_avg_recall, linestyle='-', color='black', linewidth=2)

for i in range(len(data_avg)):
    plt.scatter(data_avg[i], data_avg_recall[i], color=colors[i], edgecolor='black', s=150, marker='o')

# for i, stage in enumerate(stages):
#     plt.text(data_avg[i], data_avg_recall[i], stage, fontsize=12, ha='right')

mouse_auto_data, mouse_bronze_data, mouse_silver_data, mouse_gold_data, mouse_ground_data = get_metric(mouse_all_file_path, mouse_7_sheet_name, auto_precision_column, bronze_precision_column, silver_precision_column, is_human=False)
mouse_auto_recall_data, mouse_bronze_recall_data, mouse_silver_recall_data, mouse_gold_recall_data, mouse_ground_recall_data= get_metric(mouse_all_file_path, mouse_7_sheet_name, auto_recall_column, bronze_recall_column, silver_recall_column, is_human=False)

assert len(mouse_auto_data) == len(mouse_bronze_data) == len(mouse_silver_data) == len(mouse_ground_data)

mouse_auto_data = [data * 100 for data in mouse_auto_data]
mouse_bronze_data = [data * 100 for data in mouse_bronze_data]
mouse_silver_data = [data * 100 for data in mouse_silver_data]
mouse_ground_data = [data * 100 for data in mouse_ground_data]

mouse_auto_data = np.array(mouse_auto_data).astype(float)
mouse_bronze_data = np.array(mouse_bronze_data).astype(float)
mouse_silver_data = np.array(mouse_silver_data).astype(float)
mouse_ground_data = np.array(mouse_ground_data).astype(float)
mouse_data = [np.copy(mouse_auto_data), np.copy(mouse_bronze_data), np.copy(mouse_silver_data), np.copy(mouse_ground_data)]
mouse_data_avg = [np.mean(mouse_auto_data), np.mean(mouse_bronze_data), np.mean(mouse_silver_data), np.mean(mouse_ground_data)]
print(mouse_data_avg)

assert len(mouse_auto_recall_data) == len(mouse_bronze_recall_data) == len(mouse_silver_recall_data) == len(mouse_ground_recall_data)

mouse_auto_recall_data = [data * 100 for data in mouse_auto_recall_data]
mouse_bronze_recall_data = [data * 100 for data in mouse_bronze_recall_data]
mouse_silver_recall_data = [data * 100 for data in mouse_silver_recall_data]
mouse_ground_recall_data = [data * 100 for data in mouse_ground_recall_data]

mouse_auto_recall_data = np.array(mouse_auto_recall_data).astype(float)
mouse_bronze_recall_data = np.array(mouse_bronze_recall_data).astype(float)
mouse_silver_recall_data = np.array(mouse_silver_recall_data).astype(float)
mouse_ground_recall_data = np.array(mouse_ground_recall_data).astype(float)
mouse_data_recall = [np.copy(mouse_auto_recall_data), np.copy(mouse_bronze_recall_data), np.copy(mouse_silver_recall_data), np.copy(mouse_ground_recall_data)]

mouse_data_avg_recall = [np.mean(mouse_auto_recall_data), np.mean(mouse_bronze_recall_data), np.mean(mouse_silver_recall_data), np.mean(mouse_ground_recall_data)]
print(mouse_data_avg_recall)

colors = ['#e99674', '#7db5a2', '#c0c0c0', '#ffe352']

# plt.plot(mouse_data_avg, mouse_data_avg_recall, linestyle='--', color='black', linewidth=2)
#
# for i in range(len(mouse_data_avg)):
#     plt.scatter(mouse_data_avg[i], mouse_data_avg_recall[i], color=colors[i], edgecolor='black', s=150, marker='o')

plt.xlabel('Average precision(%)', fontsize=22)
plt.ylabel('Average recall(%)', fontsize=22)

plt.xticks(fontsize=21)
plt.yticks(fontsize=21)
# plt.xlim(88, 102)
plt.xlim(70, 100)
plt.ylim(top=100)

# plt.legend()
plt.tight_layout()

# 移除图形边框
for spine in plt.gca().spines.values():
    if spine.spine_type in ['top', 'right']:
        spine.set_visible(False)

# plt.grid(True)
plt.show()