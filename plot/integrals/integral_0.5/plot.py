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

def calculate_integral(x, y):
    integral = np.trapz(y, x)
    return integral

# 第一个文件的路径和名称
file1 = 'centerwall-int.txt'
# file1 = 'sidewall-int.txt'

# 读取文件1的数据
x1, y1 = read_data(file1)

# 创建图表对象
fig, ax = plt.subplots()

# 绘制第一个文件的数据
ax.plot(x1, y1, color='blue', label='center_maximum_velocity_0.5')
# ax.plot(x1, y1, color='blue', label='side_maximum_velocity_0.5')

# 添加阴影标记
ax.fill_between(x1, y1, color='lightblue', alpha=0.5)

# 设置图表属性
ax.set_xlabel('Time (s)')
ax.set_ylabel('Particle accumulation rate (#/s)')
# ax.set_title('Time vs. Mass Fraction')
ax.grid()

# 添加图例
ax.legend()

# 计算曲线的积分
integral_value = calculate_integral(x1, y1)

# 在颜色区域上显示积分值（保留四位有效小数，并显示为数学公式）
ax.text(0.5, 0.022, f'total particle: ${integral_value:.4f}$', color='red', fontsize=12, transform=ax.transAxes)
# ax.text(0.55, 0.25, f'total particle: ${integral_value:.4f}$', color='red', fontsize=12, transform=ax.transAxes)
# 设置x和y轴的范围
ax.set_xlim(0, 40)
ax.set_ylim(0, None)

# plt.savefig("centerwall_integral_0.5.png")
plt.savefig("sidewall_integral_0.5.png")
# 显示图表
plt.show()
