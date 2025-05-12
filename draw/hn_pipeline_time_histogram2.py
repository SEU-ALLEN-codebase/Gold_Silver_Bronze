import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 示例数据
from scipy.stats import stats

data = {
    'types': ['Check', 'Modify'],
    'pipeline1': [17.91, 34.37],
    'pipeline2': [5.64, 13.2],
    'pipeline3': [14.03, 31.38]
}

# 创建DataFrame
df = pd.DataFrame(data)

pipeline1_time_groups = [
    np.array([25 * 60 + 13, 15 * 60 + 25, 7 * 60 + 20, 8 * 60 + 22, 15 * 60, 31 * 60, 23 * 60,
     12 * 60, 5 * 60 + 46, 7 * 60 + 26, 25 * 60 + 30, 27 * 60 + 2]).astype(float),
    np.array([21 * 60 + 20, 15 * 60 + 37, 18 * 60, 25 * 60 + 35, 27 * 60, 25 * 60, 35 * 60,
     29 * 60, 27 * 60 + 52, 19 * 60 + 47, 65 * 60 + 3, 103 * 60 + 13]).astype(float)
]
for i in range(len(pipeline1_time_groups)):
    pipeline1_time_groups[i] /= 60.0

pipeline2_time_groups = [
    np.array([17.58 + 5 * 60 + 12, 23.115 + 3 * 60 + 24, 35.798 + 2 * 60 + 5, 39.048 + 3 * 60 + 32, 20.165 + 5 * 60,
     33.035 + 7 * 60 + 20, 46.096 + 7 * 60 + 55, 25.958 + 4 * 60 + 22, 28.681 + 3 * 60 + 22, 14.756 + 2 * 60 + 47,
     12.084 + 8 * 60, 6.511	+ 9 * 60 + 12]).astype(float),
    np.array([8 * 60 + 7, 3 * 60 + 51, 8 * 60 + 31, 10 * 60 + 56, 11 * 60, 13 * 60, 7 * 60, 8 * 60, 9 * 60 + 41,
     5 * 60 + 57, 13 * 60 + 25, 58 * 60 + 58]).astype(float)
]
for i in range(len(pipeline2_time_groups)):
    pipeline2_time_groups[i] /= 60.0

pipeline3_time_groups = [
    np.array([17.58 + 14 * 60 + 21, 23.115 + 11 * 60 + 10, 35.798 + 5 * 60 + 18, 39.048 + 7 * 60 + 11, 20.165 + 12 * 60,
     33.035 + 22 * 60, 46.096 + 23 * 60, 25.958 + 11 * 60, 28.681 + 5 * 60 + 1, 14.756 + 7 * 60 + 9,
     12.084 + 22 * 60 + 11, 6.511 + 23 * 60 + 7]).astype(float),
    np.array([20 * 60 + 21, 14 * 60 + 7, 16 * 60 + 12, 22 * 60 + 35, 23 * 60, 24 * 60, 32 * 60,
     21 * 60, 25 * 60 + 2, 13 * 60 + 47, 63 * 60 + 35, 101 * 60 + 5]).astype(float)
]
for i in range(len(pipeline3_time_groups)):
    pipeline3_time_groups[i] /= 60.0

# 计算标准差
pipe1_std_devs = [np.std(group) for group in pipeline1_time_groups]
# 计算标准差
pipe2_std_devs = [np.std(group) for group in pipeline2_time_groups]
# 计算标准差
pipe3_std_devs = [np.std(group) for group in pipeline3_time_groups]

# 计算标准误差
pipe1_std_errs = [stats.sem(group) for group in pipeline1_time_groups]
# 计算标准误差
pipe2_std_errs= [stats.sem(group) for group in pipeline2_time_groups]
# 计算标准误差
pipe3_std_errs = [stats.sem(group) for group in pipeline3_time_groups]

matplotlib.use('TkAgg')

# 设置初始位置和间距
bar_width = 0.15  # 柱子的宽度保持不变
spacing = 0.5   # 自定义间距

# 手动计算每个柱子的位置
x = np.arange(len(df['types'])) * (bar_width + spacing)

# index = np.arange(len(df['types']))
# index[0] += offset

# 创建图形
fig, ax = plt.subplots(figsize=(10, 8))

# 绘制每个指标的柱状图
bar1 = ax.bar(x, df['pipeline1'], bar_width, yerr=pipe1_std_errs, capsize=5, label='pipeline1', color=(115/255, 181/255, 162/255))
bar2 = ax.bar(x + bar_width, df['pipeline2'], bar_width, yerr=pipe2_std_errs, capsize=5, label='pipeline2', color=(233/255, 150/255, 116/255))
bar3 = ax.bar(x + bar_width * 2, df['pipeline3'], bar_width, yerr=pipe3_std_errs, capsize=5, label='pipeline3', color=(148/255, 163/255, 194/255))

# 设置标签和标题
# ax.set_xlabel('Pipeline')
ax.set_ylabel('Check and modify time(min)', fontsize=24)
# ax.set_title('Inspect and modify duration of three pipelines', fontsize=20, pad=20)
ax.set_xticks(x + bar_width)
ax.set_xticklabels(df['types'], fontsize=26)
# ax.set_xticks([0, 1, 2])
ax.set_xlim([-0.25, 1.6])
# ax.set_ylim([0, 60])

# ax.legend()
# 设置纵坐标标签字体大小
plt.yticks(fontsize=17)
legend = ax.legend(loc='upper right', prop={'size': 20})  # 另一种方法，指定字体大小

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
