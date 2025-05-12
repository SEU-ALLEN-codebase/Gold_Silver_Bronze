import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 示例数据
# data = {
#     'error_types': ['Multifurcation', 'Loop', 'Angle Error', 'Overlapping Branch',
#                'Floating Branch', 'Missing', 'Missing Branch', 'Over-tracing', 'Internal Error among Branches'],
#     'pipeline1': [2, 0, 1, 0, 0, 293, 79, 14, 45],
#     'pipeline2': [2, 0, 1, 0, 0, 224, 0, 0, 0],
#     'pipeline3': [2, 0, 1, 0, 0, 311, 79, 14, 45]
# }

data = {
    'error_types': ['Missing', 'Missing Branch', 'Internal Error among Branches', 'Over-tracing',
                    'Multifurcation', 'Angle Error', 'Loop', 'Overlapping Branch', 'Floating Branch'],
    'pipeline1': [293, 79, 45, 14, 2, 1, 0, 0, 0],
    'pipeline2': [224, 0, 0, 0, 2, 1, 0, 0, 0],
    'pipeline3': [311, 79, 45, 14, 2, 1, 0, 0, 0]
}

matplotlib.use('TkAgg')

# 创建DataFrame
df = pd.DataFrame(data)

# 设置柱的宽度和位置
bar_width = 0.8
# offset = 0.5
index = np.arange(len(df['error_types']))
# index[0] += offset
index *= 3
# for i in range(len(index)):
#     index[i] = float(index[i])
#     index[i] *= 2.2

# 创建图形
fig, ax = plt.subplots(figsize=(15, 10))

# 绘制每个指标的柱状图
bar1 = ax.bar(index, df['pipeline1'], bar_width, label='pipeline1', color=(115/255, 181/255, 162/255))
bar2 = ax.bar(index + bar_width, df['pipeline2'], bar_width, label='pipeline2', color=(233/255, 150/255, 116/255))
bar3 = ax.bar(index + bar_width * 2, df['pipeline3'], bar_width, label='pipeline3', color=(148/255, 163/255, 194/255))

# 在柱子上显示百分比
for bar, number in zip(bar1, df['pipeline1']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3, number,
             ha='center', color='black', fontsize=17)

# 在柱子上显示百分比
for bar, number in zip(bar2, df['pipeline2']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3, number,
             ha='center', color='black', fontsize=17)

# 在柱子上显示百分比
for bar, number in zip(bar3, df['pipeline3']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3, number,
             ha='center', color='black', fontsize=17)

# 设置标签和标题
# ax.set_xlabel('Pipeline')
ax.set_ylabel('Number of corrected errors', fontsize=26)
# ax.set_title('Number of different types of corrected errors of three pipelines', fontsize=26, pad=20)
ax.set_xticks(index + bar_width)
ax.set_xticklabels(df['error_types'], fontsize=27, rotation=45, ha='right')
# ax.set_xticks([0, 1, 2])
# ax.set_xlim([-0.24, 1.48])
ax.set_xlim([-0.9, 26.5])

# ax.legend()
# 设置纵坐标标签字体大小
plt.yticks(fontsize=24)
legend = ax.legend(loc='upper right', prop={'size': 23})  # 另一种方法，指定字体大小

# 或者可以使用 subplots_adjust 手动调整布局
# plt.subplots_adjust(top=0.85)

# 调整布局以确保标签显示不被截断
plt.tight_layout()

# 移除图形边框
for spine in plt.gca().spines.values():
    if spine.spine_type in ['top', 'right']:
        spine.set_visible(False)

# 显示图形
plt.show()
