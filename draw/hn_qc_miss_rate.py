import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# miss_rate = FN / (FN + TP)

Multifurcation_FN = 2
Multifurcation_TP = 663
Loop_FN = 0
Loop_TP = 89
Angle_Error_TP = 58
Angle_Error_FN = 9
Overlapping_Branch_TP = 252
Overlapping_Branch_FN = 35
Floating_Branch_TP = 42
Floating_Branch_FN = 0
Missing_TP = 539 + 232
Missing_FN = 157 + 64
Crossing_Direction_Error_TP = 147
Crossing_Direction_Error_FN = 17

Multifurcation_MissRate = (Multifurcation_FN / (Multifurcation_TP + Multifurcation_FN)) * 100
Loop_MissRate = (Loop_FN / (Loop_TP + Loop_FN)) * 100
Angle_Error_MissRate = (Angle_Error_FN / (Angle_Error_TP + Angle_Error_FN)) * 100
Overlapping_Branch_MissRate = (Overlapping_Branch_FN / (Overlapping_Branch_TP + Overlapping_Branch_FN)) * 100
Floating_Branch_MissRate = (Floating_Branch_FN / (Floating_Branch_TP + Floating_Branch_FN)) * 100
Missing_MissRate = (Missing_FN / (Missing_TP + Missing_FN)) * 100
Crossing_Direction_Error_MissRate = (Crossing_Direction_Error_FN / (Crossing_Direction_Error_TP + Crossing_Direction_Error_FN)) * 100

# 错误类型和对应的precision
error_types = ['Multifurcation', 'Loop', 'Angle Error', 'Overlapping Branches', 'Isolated Branch', 'Missing', 'Crossing Direction Error']
miss_rates = [Multifurcation_MissRate, Loop_MissRate, Angle_Error_MissRate, Overlapping_Branch_MissRate, Floating_Branch_MissRate, Missing_MissRate, Crossing_Direction_Error_MissRate]
percentages = [round(p, 1) for p in miss_rates]

print(percentages)

matplotlib.use('TkAgg')
# 创建柱状图
plt.figure(figsize=(10, 10))

# 设置初始位置和间距
bar_width = 0.6  # 柱子的宽度保持不变
spacing = 0.2    # 自定义间距

# 手动计算每个柱子的位置
x = np.arange(len(error_types)) * (bar_width + spacing)

bars = plt.bar(x, percentages, width=bar_width, color=(128/255, 128/255, 128/255))

# 在每个柱子上显示百分比
for bar, percentage in zip(bars, percentages):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f'{percentage:.1f}',
             ha='center', color='black', fontsize=26)

# 添加标题和标签
# plt.title('Automatic QC inspect miss rate of different types of errors', fontsize=22, pad=35)
# plt.xlabel('error type')
plt.ylabel('Omission rate(%)', fontsize=27)
# 设置横坐标标签倾斜 45 度
plt.xticks(x, error_types, rotation=45, fontsize=25, ha='right')
# 设置纵坐标标签字体大小
plt.yticks(fontsize=26)

# 调整布局以确保标签显示不被截断
plt.tight_layout()

# 移除图形边框
for spine in plt.gca().spines.values():
    if spine.spine_type in ['top', 'right']:
        spine.set_visible(False)

# 保存为 SVG 格式
plt.savefig(r'C:\Users\penglab\Documents\金银铜\figure_svg\hn_omission_rate.svg', format='svg')

# 显示图表
plt.show()

