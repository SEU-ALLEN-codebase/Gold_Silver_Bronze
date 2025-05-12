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

auto_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\auto_global_feature_mouse_all.xlsx'
auto_sheet_name = r'auto_global_feature_mouse_all'
bronze_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\bronze_global_feature_mouse_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
bronze_sheet_name = r'bronze_global_feature_mouse_all'
silver_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\silver_global_feature_mouse_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
silver_sheet_name = r'silver_global_feature_mouse_all'
gold_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\gold_global_feature_mouse_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
gold_sheet_name = r'gold_global_feature_mouse_all'
length_column = 'L'

# exp2_file_path = r'C:\Users\penglab\Documents\金银铜\autoQC_数据生产流程.xlsx'
# exp2_sheet_name = "流程一"
# exp2_column = 'N'

def get_length(file_path, sheet_name, column):
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

bronze_data = get_length(bronze_file_path, bronze_sheet_name, length_column)
silver_data = get_length(silver_file_path, silver_sheet_name, length_column)
gold_data = get_length(gold_file_path, gold_sheet_name, length_column)

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
# plt.title("Length of the bronze standard, silver standard and gold standard", fontsize=18, pad=20)
plt.ylabel("Length(μm)", fontsize=20)
plt.xlabel('')
plt.show()
