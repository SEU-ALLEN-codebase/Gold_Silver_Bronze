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

auto_column = 'H'
bronze_column = 'I'
silver_column = 'J'

# exp2_file_path = r'C:\Users\penglab\Documents\金银铜\autoQC_数据生产流程.xlsx'
# exp2_sheet_name = "流程一"
# exp2_column = 'N'

def get_F1(file_path, sheet_name, auto_column, bronze_column, silver_column):
    # 打开 Excel 文件
    wb = load_workbook(file_path)
    sheet = wb[sheet_name]
    auto_data = []
    for cell in sheet[auto_column][1:]:
        if cell.value is not None:
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
    return auto_data, bronze_data, silver_data

auto_data, bronze_data, silver_data = get_F1(exp1_file_path, exp1_sheet_name, auto_column, bronze_column, silver_column)

# 生成DataFrame
df = pd.DataFrame({
    'value': np.concatenate([np.array(auto_data), np.array(bronze_data), np.array(silver_data)]),
    'category': ['Auto reconstruction'] * 42 + ['Bronze standard'] * 42 + ['Silver standard'] * 42
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
# plt.title("F1 of the auto reconstruction, bronze standard and silver standard", fontsize=18, pad=20)
plt.ylabel("F1", fontsize=20)
plt.xlabel('')
plt.show()
