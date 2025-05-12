import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import joypy

# # 创建示例数据
# np.random.seed(10)
# category_1 = np.random.uniform(0, 1, 30)  # 类别1的数据
# category_2 = np.random.uniform(0, 1, 30)  # 类别2的数据

# 读取 Excel 文件
from joypy import joyplot
from openpyxl import load_workbook

human_auto_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\auto_global_feature_human_all.xlsx'
human_auto_sheet_name = r'auto_global_feature_human_all'
human_bronze_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\bronze_global_feature_human_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
human_bronze_sheet_name = r'bronze_global_feature_human_all'
human_silver_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\silver_global_feature_human_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
human_silver_sheet_name = r'silver_global_feature_human_all'
human_gold_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\gold_global_feature_human_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
human_gold_sheet_name = r'gold_global_feature_human_all'

mouse_auto_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\auto_global_feature_mouse_all.xlsx'
mouse_auto_sheet_name = r'auto_global_feature_mouse_all'
mouse_bronze_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\bronze_global_feature_mouse_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
mouse_bronze_sheet_name = r'bronze_global_feature_mouse_all'
mouse_silver_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\silver_global_feature_mouse_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
mouse_silver_sheet_name = r'silver_global_feature_mosue_all'
mouse_gold_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\gold_global_feature_mouse_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
mouse_gold_sheet_name = r'gold_global_feature_mouse_all'

synthetic_auto_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\auto_global_feature_synthetic_all.xlsx'
synthetic_auto_sheet_name = r'auto_global_feature_synthetic'
synthetic_bronze_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\bronze_global_feature_synthetic_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
synthetic_bronze_sheet_name = r'bronze_global_feature_synthetic'
synthetic_silver_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\silver_global_feature_synthetic_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
synthetic_silver_sheet_name = r'silver_global_feature_synthetic'
synthetic_gold_file_path = r'D:\source\PythonProjects\Gold_Silver_Bronze\experiments\gold_global_feature_synthetic_all.xlsx'  # 将 'example.xlsx' 替换为你的 Excel 文件路径
synthetic_gold_sheet_name = r'gold_global_feature_synthetic'

branch_column = 'F'
tip_column = 'G'
length_column = 'L'
maxbranchorder_column = 'Q'
bif_column = 'E'

# exp2_file_path = r'C:\Users\penglab\Documents\金银铜\autoQC_数据生产流程.xlsx'
# exp2_sheet_name = "流程一"
# exp2_column = 'N'

removed_human_neuron_number = ['03764', '05578', '06019']
name_column = 'A'

def get_features(file_path, sheet_name, column, is_human=True):
    # 打开 Excel 文件
    wb = load_workbook(file_path)
    sheet = wb[sheet_name]
    data = []
    for i, cell in enumerate(sheet[column][1:]):
        if cell.value is not None and cell.value != '':
            if is_human:
                image_number = sheet[name_column][i + 1].value.split('_')[0]
                if image_number in removed_human_neuron_number:
                    continue
            data.append((float(cell.value)))
        else:
            break

    # column_data = [float(cell.value) for cell in sheet[column][1:]]
    print(data)
    return data

human_auto_branch_data = get_features(human_auto_file_path, human_auto_sheet_name, branch_column)
human_bronze_branch_data = get_features(human_bronze_file_path, human_bronze_sheet_name, branch_column)
human_silver_branch_data = get_features(human_silver_file_path, human_silver_sheet_name, branch_column)
human_gold_branch_data = get_features(human_gold_file_path, human_gold_sheet_name, branch_column)

human_auto_tip_data = get_features(human_auto_file_path, human_auto_sheet_name, tip_column)
human_bronze_tip_data = get_features(human_bronze_file_path, human_bronze_sheet_name, tip_column)
human_silver_tip_data = get_features(human_silver_file_path, human_silver_sheet_name, tip_column)
human_gold_tip_data = get_features(human_gold_file_path, human_gold_sheet_name, tip_column)

human_auto_length_data = get_features(human_auto_file_path, human_auto_sheet_name, length_column)
human_bronze_length_data = get_features(human_bronze_file_path, human_bronze_sheet_name, length_column)
human_silver_length_data = get_features(human_silver_file_path, human_silver_sheet_name, length_column)
human_gold_length_data = get_features(human_gold_file_path, human_gold_sheet_name, length_column)

human_auto_maxbranchorder_data = get_features(human_auto_file_path, human_auto_sheet_name, maxbranchorder_column)
human_bronze_maxbranchorder_data = get_features(human_bronze_file_path, human_bronze_sheet_name, maxbranchorder_column)
human_silver_maxbranchorder_data = get_features(human_silver_file_path, human_silver_sheet_name, maxbranchorder_column)
human_gold_maxbranchorder_data = get_features(human_gold_file_path, human_gold_sheet_name, maxbranchorder_column)

human_auto_bif_data = get_features(human_auto_file_path, human_auto_sheet_name, bif_column)
human_bronze_bif_data = get_features(human_bronze_file_path, human_bronze_sheet_name, bif_column)
human_silver_bif_data = get_features(human_silver_file_path, human_silver_sheet_name, bif_column)
human_gold_bif_data = get_features(human_gold_file_path, human_gold_sheet_name, bif_column)

mouse_auto_branch_data = get_features(mouse_auto_file_path, mouse_auto_sheet_name, branch_column, False)
mouse_bronze_branch_data = get_features(mouse_bronze_file_path, mouse_bronze_sheet_name, branch_column, False)
mouse_silver_branch_data = get_features(mouse_silver_file_path, mouse_silver_sheet_name, branch_column, False)
mouse_gold_branch_data = get_features(mouse_gold_file_path, mouse_gold_sheet_name, branch_column, False)

mouse_auto_tip_data = get_features(mouse_auto_file_path, mouse_auto_sheet_name, tip_column, False)
mouse_bronze_tip_data = get_features(mouse_bronze_file_path, mouse_bronze_sheet_name, tip_column, False)
mouse_silver_tip_data = get_features(mouse_silver_file_path, mouse_silver_sheet_name, tip_column, False)
mouse_gold_tip_data = get_features(mouse_gold_file_path, mouse_gold_sheet_name, tip_column, False)

mouse_auto_length_data = get_features(mouse_auto_file_path, mouse_auto_sheet_name, length_column, False)
mouse_bronze_length_data = get_features(mouse_bronze_file_path, mouse_bronze_sheet_name, length_column, False)
mouse_silver_length_data = get_features(mouse_silver_file_path, mouse_silver_sheet_name, length_column, False)
mouse_gold_length_data = get_features(mouse_gold_file_path, mouse_gold_sheet_name, length_column, False)

mouse_auto_bif_data = get_features(mouse_auto_file_path, mouse_auto_sheet_name, bif_column, False)
mouse_bronze_bif_data = get_features(mouse_bronze_file_path, mouse_bronze_sheet_name, bif_column, False)
mouse_silver_bif_data = get_features(mouse_silver_file_path, mouse_silver_sheet_name, bif_column, False)
mouse_gold_bif_data = get_features(mouse_gold_file_path, mouse_gold_sheet_name, bif_column, False)

mouse_auto_maxbranchorder_data = get_features(mouse_auto_file_path, mouse_auto_sheet_name, maxbranchorder_column, False)
mouse_bronze_maxbranchorder_data = get_features(mouse_bronze_file_path, mouse_bronze_sheet_name, maxbranchorder_column, False)
mouse_silver_maxbranchorder_data = get_features(mouse_silver_file_path, mouse_silver_sheet_name, maxbranchorder_column, False)
mouse_gold_maxbranchorder_data = get_features(mouse_gold_file_path, mouse_gold_sheet_name, maxbranchorder_column, False)

synthetic_auto_tip_data = get_features(synthetic_auto_file_path, synthetic_auto_sheet_name, tip_column)
synthetic_bronze_tip_data = get_features(synthetic_bronze_file_path, synthetic_bronze_sheet_name, tip_column)
synthetic_silver_tip_data = get_features(synthetic_silver_file_path, synthetic_silver_sheet_name, tip_column)
synthetic_gold_tip_data = get_features(synthetic_gold_file_path, synthetic_gold_sheet_name, tip_column)

synthetic_auto_length_data = get_features(synthetic_auto_file_path, synthetic_auto_sheet_name, length_column)
synthetic_bronze_length_data = get_features(synthetic_bronze_file_path, synthetic_bronze_sheet_name, length_column)
synthetic_silver_length_data = get_features(synthetic_silver_file_path, synthetic_silver_sheet_name, length_column)
synthetic_gold_length_data = get_features(synthetic_gold_file_path, synthetic_gold_sheet_name, length_column)

synthetic_auto_maxbranchorder_data = get_features(synthetic_auto_file_path, synthetic_auto_sheet_name, maxbranchorder_column)
synthetic_bronze_maxbranchorder_data = get_features(synthetic_bronze_file_path, synthetic_bronze_sheet_name, maxbranchorder_column)
synthetic_silver_maxbranchorder_data = get_features(synthetic_silver_file_path, synthetic_silver_sheet_name, maxbranchorder_column)
synthetic_gold_maxbranchorder_data = get_features(synthetic_gold_file_path, synthetic_gold_sheet_name, maxbranchorder_column)

human_neuron_count = 39
mouse_neuron_count = 30
synthetic_neuron_count = 15

data = {
    "Auto": [data / 1000 for data in synthetic_auto_length_data],
    "Bronze": [data / 1000 for data in synthetic_bronze_length_data],
    "Silver": [data / 1000 for data in synthetic_silver_length_data],
    "Gold": [data / 1000 for data in synthetic_gold_length_data],
}

df = pd.DataFrame(data)

# df = pd.DataFrame({
#     'value': np.concatenate([data["Auto"], data["Bronze"], data["Silver"], data["Gold"]]),
#     'group': ['Auto'] * len(human_auto_tip_data) + ['Bronze'] * len(human_bronze_tip_data) + ['Silver'] * len(human_silver_tip_data) + ['Gold'] * len(human_gold_tip_data)
# })

# # 设置背景没有网格
# sns.set(style="white")  # 使用没有网格的背景
# 定义颜色
# colors = ['#96cac0', '#f6f5bc', '#c2bed5', '#8aafc9']
colors = ['#989898', '#e4bd95', '#70b092', '#e17477']

matplotlib.use('TkAgg')

fig, axes = joyplot(
    data=[df[col].values for col in df.columns],
    labels=list(df.columns),
    fade=True,
    alpha=0.7,
    fill=True,
    ylabelsize=23,
    figsize=(9, 4),
    color=colors,
    linecolor="black",
    x_range=[-2.5, 15.5],
)

plt.xticks(fontsize=23)

# for ax in axes:
#     ax.set_xlabel('')  # 设置 x 轴标签

# # 移除图形边框
# for spine in plt.gca().spines.values():
#     if spine.spine_type in ['top', 'right']:
#         spine.set_visible(False)

# 显示图形
# plt.title("Number of branches of the bronze standard, silver standard and gold standard", fontsize=18, pad=20)
# plt.ylabel("Difference in number of bifurcations", fontsize=23)

# plt.tight_layout()
plt.show()
