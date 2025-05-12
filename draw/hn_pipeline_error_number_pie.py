import matplotlib
import matplotlib.pyplot as plt

# 数据

pipe13_labels = ['Multifurcation', 'Angle Error', 'Missing', 'Missing Branch', 'Over-tracing', 'Internal Error among Branches']
error_types = ['Multifurcation', 'Loop', 'Angle Error', 'Overlapping Branch', 'Floating Branch', 'Missing', 'Crossing Direction Error']
pipe2_labels = ['Multifurcation', 'Angle Error', 'Missing']
pipe13_labels_new = ['Missing', 'Missing Branch', 'Internal Error among Branches', 'Over-tracing', 'Multifurcation', 'Angle Error']
pipe2_labels_new = ['Missing', 'Multifurcation', 'Angle Error']
mouse_label = ['Missing', 'Over-tracing', 'Internal Error among Branches', 'Missing Branch', 'Multifurcation', 'Overlapping Branch', 'Angle Error']

pipe1_sizes = [2, 1, 293, 79, 14, 45]  # 各类别的数量
pipe3_sizes = [2, 1, 311, 79, 14, 45]
pipe2_sizes = [2, 1, 224]

# pipe1_sizes_new = [293, 79, 45, 14, 2, 1]  # 各类别的数量
# pipe3_sizes_new = [311, 79, 45, 14, 2, 1]
# pipe2_sizes_new = [224, 2, 1]
pipe3_sizes_new = [1212, 330, 137, 28, 14, 4]
mouse_sizes = [496, 302, 327, 457, 28, 8, 5]

mouse_sizes_sum = 0
for i in mouse_sizes:
    mouse_sizes_sum += i
mouse_percentage = [i / mouse_sizes_sum for i in mouse_sizes]
print(mouse_percentage)

pipe13_colors = ['gold', 'cyan', 'lightcoral', 'lightskyblue', 'lightgreen', 'lightpink']
# pipe13_colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
pipe2_colors = ['gold', 'cyan', 'lightcoral']

pipe13_colors_new = ['lightcoral', 'lightskyblue', 'lightpink', 'lightgreen', 'gold', 'cyan']
pipe2_colors_new = ['lightcoral', 'gold', 'cyan']
mouse_color = ['lightcoral', 'lightgreen', 'lightpink', 'lightskyblue', 'gold', '#FFA500', 'cyan']

pipe13_explode = (0, 0, 0, 0, 0, 0)  # 突出显示第一块（即 'Category A'）
pipe2_explode = (0, 0, 0)
mouse_explode = (0, 0, 0, 0, 0, 0, 0)

matplotlib.use('TkAgg')

plt.figure(figsize=(12, 10))

# 绘制饼图
patches, texts = plt.pie(pipe3_sizes_new, explode=pipe13_explode, labels=None, colors=pipe13_colors_new,
        autopct=None, shadow=False, startangle=140)

plt.axis('equal')  # 保证饼图是圆的
# plt.title('Percentage of different types of errors of pipeline1', fontsize=26, pad=140, loc='center')
# plt.title('Percentage of different types of errors of pipeline3', fontsize=26, pad=130, loc='center')
# plt.title('Percentage of different types of errors of pipeline2', fontsize=26, pad=110, loc='center')
# 添加图例
# plt.legend(patches, pipe13_labels_new, loc="upper right", bbox_to_anchor=(1.50, 1.30), prop={'size': 20})
# plt.legend(patches, pipe13_labels_new, loc="upper right", bbox_to_anchor=(1.60, 1.20), prop={'size': 20})
# plt.legend(patches, pipe13_labels_new, loc="upper right", bbox_to_anchor=(1.26, 1.08), prop={'size': 20})
plt.legend(patches, pipe13_labels_new, loc="upper right", bbox_to_anchor=(2.2, 1.08), prop={'size': 20})

# 调整边距以确保标题完全显示
plt.subplots_adjust(top=0.80, right=0.5)  # 默认值为1.0，减小值增加顶部边距
plt.show()
