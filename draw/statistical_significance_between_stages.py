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

synthetic_auto_F1_column = 'J'
synthetic_bronze_F1_column = 'K'
synthetic_silver_F1_column = 'L'
synthetic_gold_F1_column = 'M'

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

human_auto_data, human_bronze_data, human_silver_data, human_gold_data, human_ground_data = get_metric(exp1_file_path, exp1_sheet_name, auto_precision_column, bronze_precision_column, silver_precision_column, is_human=True)
human_auto_recall_data, human_bronze_recall_data, human_silver_recall_data, human_gold_recall_data, human_ground_recall_data= get_metric(exp1_file_path, exp1_sheet_name, auto_recall_column, bronze_recall_column, silver_recall_column, is_human=True)

human_auto_data = np.array(human_auto_data).astype(float)
human_bronze_data = np.array(human_bronze_data).astype(float)
human_silver_data = np.array(human_silver_data).astype(float)
human_ground_data = np.array(human_ground_data).astype(float)

human_auto_recall_data = np.array(human_auto_recall_data).astype(float)
human_bronze_recall_data = np.array(human_bronze_recall_data).astype(float)
human_silver_recall_data = np.array(human_silver_recall_data).astype(float)
human_ground_recall_data = np.array(human_ground_recall_data).astype(float)

mouse_auto_data, mouse_bronze_data, mouse_silver_data, mouse_gold_data, mouse_ground_data = get_metric(mouse_all_file_path, mouse_7_sheet_name, auto_precision_column, bronze_precision_column, silver_precision_column, is_human=False)
mouse_auto_recall_data, mouse_bronze_recall_data, mouse_silver_recall_data, mouse_gold_recall_data, mouse_ground_recall_data= get_metric(mouse_all_file_path, mouse_7_sheet_name, auto_recall_column, bronze_recall_column, silver_recall_column, is_human=False)

mouse_auto_data = np.array(mouse_auto_data).astype(float)
mouse_bronze_data = np.array(mouse_bronze_data).astype(float)
mouse_silver_data = np.array(mouse_silver_data).astype(float)
mouse_ground_data = np.array(mouse_ground_data).astype(float)

mouse_auto_recall_data = np.array(mouse_auto_recall_data).astype(float)
mouse_bronze_recall_data = np.array(mouse_bronze_recall_data).astype(float)
mouse_silver_recall_data = np.array(mouse_silver_recall_data).astype(float)
mouse_ground_recall_data = np.array(mouse_ground_recall_data).astype(float)

synthetic_auto_data, synthetic_bronze_data, synthetic_silver_data, synthetic_gold_data, synthetic_ground_truth_data = get_metric(synthetic_15_file_path, synthetic_15_sheet_name, synthetic_auto_precision_column, synthetic_bronze_precision_column, synthetic_silver_precision_column, synthetic_gold_precision_column, False)
synthetic_auto_recall_data, synthetic_bronze_recall_data, synthetic_silver_recall_data, synthetic_gold_recall_data, synthetic_ground_truth_recall_data = get_metric(synthetic_15_file_path, synthetic_15_sheet_name, synthetic_auto_recall_column, synthetic_bronze_recall_column, synthetic_silver_recall_column, synthetic_gold_recall_column, False)
synthetic_auto_F1_data, synthetic_bronze_F1_data, synthetic_silver_F1_data, synthetic_gold_F1_data, synthetic_ground_truth_F1_data = get_metric(synthetic_15_file_path, synthetic_15_sheet_name, synthetic_auto_F1_column, synthetic_bronze_F1_column, synthetic_silver_F1_column, synthetic_gold_F1_column, False)

synthetic_auto_data = np.array(synthetic_auto_data).astype(float)
synthetic_bronze_data = np.array(synthetic_bronze_data).astype(float)
synthetic_silver_data = np.array(synthetic_silver_data).astype(float)
synthetic_gold_data = np.array(synthetic_gold_data).astype(float)
synthetic_ground_truth_data = np.array(synthetic_ground_truth_data).astype(float)

synthetic_auto_recall_data = np.array(synthetic_auto_recall_data).astype(float)
synthetic_bronze_recall_data = np.array(synthetic_bronze_recall_data).astype(float)
synthetic_silver_recall_data = np.array(synthetic_silver_recall_data).astype(float)
synthetic_gold_recall_data = np.array(synthetic_gold_recall_data).astype(float)
synthetic_ground_truth_recall_data = np.array(synthetic_ground_truth_recall_data).astype(float)

synthetic_auto_F1_data = np.array(synthetic_auto_F1_data).astype(float)
synthetic_bronze_F1_data = np.array(synthetic_bronze_F1_data).astype(float)
synthetic_silver_F1_data = np.array(synthetic_silver_F1_data).astype(float)
synthetic_gold_F1_data = np.array(synthetic_gold_F1_data).astype(float)
synthetic_ground_truth_F1_data = np.array(synthetic_ground_truth_F1_data).astype(float)

group1 = synthetic_bronze_F1_data
group2 = synthetic_silver_F1_data

mean1, mean2 = np.mean(group1), np.mean(group2)
std1, std2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
n1, n2 = len(group1), len(group2)

# 计算t统计量
t_stat = (mean1 - mean2) / np.sqrt((std1**2 / n1) + (std2**2 / n2))

# Welch's 自由度计算
df = ((std1**2 / n1) + (std2**2 / n2))**2 / (
    (std1**2 / n1)**2 / (n1 - 1) + (std2**2 / n2)**2 / (n2 - 1)
)

# 计算p值（双尾检验）
p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))

print(group1)
print(group2)
# 输出t统计量和p值
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")