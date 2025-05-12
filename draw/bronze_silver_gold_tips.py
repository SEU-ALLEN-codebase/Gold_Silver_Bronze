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

bronze_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\bronze_global_feature_human_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
bronze_sheet_name = r'bronze_global_feature_human_all'
silver_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\silver_global_feature_human_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
silver_sheet_name = r'silver_global_feature_human_all'
gold_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\gold_global_feature_human_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
gold_sheet_name = r'gold_global_feature_human_all'
tip_column = 'G'

# exp2_file_path = r'C:\Users\penglab\Documents\金银铜\autoQC_数据生产流程.xlsx'
# exp2_sheet_name = "流程一"
# exp2_column = 'N'

def get_tips(file_path, sheet_name, column):
    # 打开 Excel 文件
    wb = load_workbook(file_path)
    sheet = wb[sheet_name]
    data = []
    for cell in sheet[column][1:]:
        if cell.value is not None:
            data.append(float(cell.value))
    # column_data = [float(cell.value) for cell in sheet[column][1:]]
    print(data)
    return data

bronze_data = get_tips(bronze_file_path, bronze_sheet_name, tip_column)
silver_data = get_tips(silver_file_path, silver_sheet_name, tip_column)
gold_data = get_tips(gold_file_path, gold_sheet_name, tip_column)

# 生成DataFrame
df = pd.DataFrame({
    'value': np.concatenate([np.array(bronze_data), np.array(silver_data), np.array(gold_data)]),
    'category': ['Bronze standard'] * 42 + ['Silver standard'] * 42 + ['Gold standard'] * 42
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
# plt.title("Number of tips of the bronze standard, silver standard and gold standard", fontsize=18, pad=20)
plt.ylabel("Number of tips", fontsize=20)
plt.xlabel('')
plt.show()
