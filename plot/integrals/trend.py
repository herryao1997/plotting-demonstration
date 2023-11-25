import numpy as np
import matplotlib.pyplot as plt

x = [0.5, 1.0, 1.5]
y = [212.2211, 1212.3804, 542.0498]
y1 = [8412.9769, 21992.8109, 32790.7437]

x = np.array(x)
y = np.array(y)
y1 = np.array(y1)

# 创建图表对象
fig, ax = plt.subplots()

# 绘制第一个文件的数据
ax.plot(x, y, '-o', color='blue', label='center_instrument')
ax.plot(x, y1, '-*', color='red', label='side_instrument')

# 添加阴影标记
# ax.fill_between(x1, y1, color='lightblue', alpha=0.5)

# 设置图表属性
ax.set_xlabel('Velocity (m/s)')
ax.set_ylabel("Total particle accumulation number (#)")
# ax.set_title('Mass Fraction Acculumation on Center Wall ')
# ax.set_title('Mass Fraction Accumulation on Instruments ')
ax.grid()
plt.legend()
# 添加图例
# ax.legend()

# 计算曲线的积分
# integral_value = calculate_integral(x1, y1)

# 在颜色区域上显示积分值
# ax.text(0.5, 0.5, f'Integral: {integral_value} m^2*s', color='red', fontsize=12, transform=ax.transAxes)
# ax.text(0.5, 0.5, f'Integral: {integral_value:.4f} m^2*s', color='red', fontsize=12, transform=ax.transAxes)
# 在颜色区域上显示积分值（保留四位有效小数，并显示为数学公式）
# ax.text(0.5, 0.5, f'Integral: ${integral_value:.4f} \, \mathrm{{m^2 \cdot s}}$', color='red', fontsize=12, transform=ax.transAxes)


# plt.savefig("centerwall_integral_trend.png")
plt.savefig("sidewall_integral_trend.png")
# 显示图表
plt.show()
