import matplotlib
import seaborn as sns
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

auto_column = 'E'
bronze_column = 'F'
silver_column = 'G'

# exp2_file_path = r'C:\Users\penglab\Documents\金银铜\autoQC_数据生产流程.xlsx'
# exp2_sheet_name = "流程一"
# exp2_column = 'N'

def get_recall(file_path, sheet_name, auto_column, bronze_column, silver_column):
    # 打开 Excel 文件
    wb = load_workbook(file_path)
    sheet = wb[sheet_name]
    auto_data = []
    count = 0
    for cell in sheet[auto_column][1:]:
        if cell.value is not None:
            count += 1
            auto_data.append(float(cell.value))
    # column_data = [float(cell.value) for cell in sheet[column][1:]]
    print(auto_data)

    bronze_data = []
    for cell in sheet[bronze_column][1:]:
        if cell.value is not None:
            bronze_data.append(float(cell.value))
    # column_data = [float(cell.value) for cell in sheet[column][1:]]
    print(bronze_data)

    silver_data = []
    for cell in sheet[silver_column][1:]:
        if cell.value is not None:
            silver_data.append(float(cell.value))
    # column_data = [float(cell.value) for cell in sheet[column][1:]]
    print(silver_data)
    gold_data = [1.0] * count

    return auto_data, bronze_data, silver_data, gold_data

auto_data, bronze_data, silver_data, gold_data = get_recall(exp1_file_path, exp1_sheet_name, auto_column, bronze_column, silver_column)
# auto_data_18454, bronze_data_18454, silver_data_18454, gold_data_18454 = get_recall(mouse_18454_file_path, mouse_18454_sheet_name, auto_column, bronze_column, silver_column)
# auto_data_7, bronze_data_7, silver_data_7, gold_data_7 = get_recall(mouse_7_file_path, mouse_7_sheet_name, auto_column, bronze_column, silver_column)

# auto_data = auto_data_18454.copy()
# auto_data.extend(auto_data_7)
# bronze_data = bronze_data_18454.copy()
# bronze_data.extend(bronze_data_7)
# silver_data = silver_data_18454.copy()
# silver_data.extend(silver_data_7)
# gold_data = gold_data_18454.copy()
# gold_data.extend(gold_data_7)

# 生成DataFrame
count = 42
df = pd.DataFrame({
    'value': np.concatenate([np.array(auto_data), np.array(bronze_data), np.array(silver_data), np.array(gold_data)]),
    'category': ['Auto reconstruction'] * count + ['Bronze standard'] * count + ['Silver standard'] * count + ['Gold standard'] * count
})

matplotlib.use('TkAgg')

# 绘制箱线图和蜂群图
plt.figure(figsize=(10, 6))

# 绘制箱线图
sns.boxplot(x='category', y='value', data=df, width=0.5, palette="Set2")

# 绘制蜂群图
sns.swarmplot(x='category', y='value', data=df, color=".25")

plt.xticks(fontsize=20)
# 设置纵坐标标签字体大小
plt.yticks(fontsize=17)

# 显示图形
# plt.title("Recall of the auto reconstruction, bronze standard and silver standard", fontsize=18, pad=20)
plt.ylabel("Recall", fontsize=20)
plt.xlabel('')

# 移除图形边框
for spine in plt.gca().spines.values():
    if spine.spine_type in ['top', 'right']:
        spine.set_visible(False)
plt.show()
