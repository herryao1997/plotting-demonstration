import matplotlib.pyplot as plt
import numpy as np

def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    x = []
    y = []
    for line in lines:
        data = line.strip().split(' ')
        y.append(float(data[1]))
        x.append(float(data[2]))

    return x, y




# 第一个文件的路径和名称
file1 = 'center_ave_0.5.txt'
# 第二个文件的路径和名称
file2 = 'side_ave_0.5.txt'
# 第三个文件的路径和名称
file3 = 'center_ave_1.txt'
# 第四个文件的路径和名称
file4 = 'side_ave_1.txt'
# 第五个文件的路径和名称
file5 = 'center_ave_1.5.txt'
# 第六个文件的路径和名称
file6 = 'side_ave_1.5.txt'
# # 第七个文件的路径和名称
# file7 = 'center_ave_1.67.txt'
# # 第八个文件的路径和名称
# file8 = 'side_ave_1.67.txt'

# # 第一个文件的路径和名称
# file1 = 'center_average.txt'
# # 第二个文件的路径和名称
# file2 = 'side_average.txt'
# # 第三个文件的路径和名称
# file3 = 'center_average_1.txt'
# # 第四个文件的路径和名称
# file4 = 'side_average_1.txt'

# 读取文件1的数据
x1, y1 = read_data(file1)
# 读取文件2的数据
x2, y2 = read_data(file2)
# 读取文件3的数据
x3, y3 = read_data(file3)
# 读取文件4的数据
x4, y4 = read_data(file4)
# 读取文件5的数据
x5, y5 = read_data(file5)
# 读取文件6的数据
x6, y6 = read_data(file6)
# # 读取文件7的数据
# x7, y7 = read_data(file7)
# # 读取文件6的数据
# x8, y8 = read_data(file8)



# 创建图表对象
fig, ax = plt.subplots()


# 绘制第一个文件的数据
# ax.plot(x1, y1, color='red', label='center_average_velocity_0.5')

# 绘制第二个文件的数据
ax.plot(x2, y2, color='red', label='side_average_velocity_0.5')

# 绘制第三个文件的数据
# ax.plot(x3, y3, '--', color='green', label='center_average_velocity_1.0')
#
# 绘制第四个文件的数据
ax.plot(x4, y4, '--', color='green', label='side_average_velocity_1.0')

# 绘制第五个文件的数据
# ax.plot(x5, y5, '-^', color='blue', label='center_average_velocity_1.5')
#
# 绘制第六个文件的数据
ax.plot(x6, y6, '-^', color='blue', label='side_average_velocity_1.5')

# # 绘制第七个文件的数据
# ax.plot(x7, y7, '-^', color='blue', label='center_average_velocity_1.67')
# #
# # 绘制第八个文件的数据
# ax.plot(x8, y8, '-^', color='red', label='side_average_velocity_1.67')



# # 绘制第一个文件的数据
# ax.plot(x1, y1, color='blue', label='center_maximum_velocity_0.5')
# #
# # 绘制第二个文件的数据
# ax.plot(x2, y2, color='red', label='side_maximum_velocity_0.5')
#
# # 绘制第三个文件的数据
# ax.plot(x3, y3, '--', color='blue', label='center_maximum_velocity_1.0')
# #
# # 绘制第四个文件的数据
# ax.plot(x4, y4, '--', color='red', label='side_maximum_velocity_1.0')
#
# # 绘制第五个文件的数据
# ax.plot(x5, y5, '-*', color='blue', label='center_maximum_velocity_1.5')
# #
# # 绘制第六个文件的数据
# ax.plot(x6, y6, '-*', color='red', label='side_maximum_velocity_1.5')
#
# # 绘制第七个文件的数据
# ax.plot(x7, y7, '-^', color='blue', label='center_maximum_velocity_1.67')
# #
# # 绘制第八个文件的数据
# ax.plot(x8, y8, '-^', color='red', label='side_maximum_velocity_1.67')



# 设置图表属性
ax.set_xlabel('Time (s)')
ax.set_ylabel(r'Particle number density ($\#/m^3$)')
# ax.set_title('Time vs. Mass Fraction')
# ax.set_ylim(0, 0.13)
ax.grid()

# 添加图例
ax.legend(loc='best', ncol=2, fontsize=9)
# plt.savefig("max_massfraction_maximum.png")
plt.savefig("ave_side.png")
# plt.savefig("ave_center.png")
# 显示图表
plt.show()

