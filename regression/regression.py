import numpy as np
import matplotlib.pyplot as plt
import math

a = 0.0761846677
alpha = 1.5485185961

def func(x):
    if x < 1.67:
        return a * math.exp(alpha * x) * 5000000
    else:
        return 5000000

x = np.linspace(0, 2, 100)
y = np.vectorize(func)(x)

fig, ax = plt.subplots()
ax.plot(x, y, color='black')
ax.scatter([0.0, 1.67], [func(0.0), func(1.67)], color=['blue', 'red'])

# 添加注释
ax.annotate(f"Still Point\n(0.0,  {func(0.0):.1e})", xy=(0.0, func(0.0)), xytext=(10, -15), fontsize=8,
            textcoords='offset points', arrowprops=None, color='green')
ax.annotate(f"Maximum Point\n(1.67,  {func(1.67):.1e})", xy=(1.67, func(1.67)), xytext=(-90, -20), fontsize=8,
            textcoords='offset points', arrowprops=None, color='red')
# 绘制虚线
ax.plot([1.67, 1.67], [0, 5000000], color='red', linestyle='dashed')
ax.plot([-0.1, 1.67], [func(1.67), func(1.67)], color='red', linestyle='dashed')

ax.plot([0, 0], [0, func(0)], color='blue', linestyle='dashed')
ax.plot([-0.1, 0], [func(0), func(0)], color='blue', linestyle='dashed')

# 添加 LaTeX 公式
ax.text(0.1, 2200000,
        r"$ER(v) = a \cdot e^{\alpha \cdot x} \cdot C_{full}, x < 1.67$" "\n"
        r"$ER(v) = C_{full}, x \geq 1.67$" "\n"
        r"$C_{full} = 5,000,000$",
        fontsize=10, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})



plt.xlabel('Max Velocity (m/s)')
plt.ylabel('Total Particle Emission Rate (#/s)')
plt.xlim(-0.1, 2.0)
plt.ylim(0, None)
plt.title('Total Particle Emission Rate Regarding Velocity')
plt.savefig('plot_6.png')
plt.show()
