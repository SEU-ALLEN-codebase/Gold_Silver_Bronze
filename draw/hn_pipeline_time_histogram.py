import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 示例数据
data = {
    'Pipeline': ['Pipeline1', 'Pipeline2', 'Pipeline3'],
    'Inspect duration': [17.91, 5.23, 13.83],
    'Modify duration': [34.37, 13.2, 30.38],
}

# 创建DataFrame
df = pd.DataFrame(data)

# 设置柱的宽度和位置
bar_width = 0.2
index = np.arange(len(df['Pipeline']))

# 创建图形
fig, ax = plt.subplots(figsize=(10, 8))

# 绘制每个指标的柱状图
bar1 = ax.bar(index, df['Inspect duration'], bar_width, label='inspect')
bar2 = ax.bar(index + bar_width, df['Modify duration'], bar_width, label='modify')

# 设置标签和标题
# ax.set_xlabel('Pipeline')
ax.set_ylabel('Duration(min)', fontsize=17)
ax.set_title('Inspect and modify duration of three pipelines', fontsize=20, pad=20)
ax.set_xticks(index + bar_width/2)
ax.set_xticklabels(df['Pipeline'], fontsize=19)
# ax.legend()
# 设置纵坐标标签字体大小
plt.yticks(fontsize=15)
legend = ax.legend(loc='upper center', prop={'size': 14})  # 另一种方法，指定字体大小

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
