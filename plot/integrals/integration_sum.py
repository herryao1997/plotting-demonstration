import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np
import os


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


def plot_and_save_integral(ax, x, y, label, text_pos):
    ax.plot(x, y, color='blue', label=label)
    ax.fill_between(x, y, color='lightblue', alpha=0.5)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Particle passing rate (#/s)')
    ax.set_xlim(0, 40)
    ax.set_ylim(0, None)
    ax.grid()
    ax.legend(loc='upper right', fontsize=10, ncol=2)
    integral_value = calculate_integral(x, y)
    ax.text(text_pos[0], text_pos[1], f'Particle number: ${integral_value:.2f}$', color='red', fontsize=9, transform=ax.transAxes)


subplot_labels = ['a.', 'b.', 'c.', 'd.', 'e.', 'f.']
integral_text_positions = [(0.45, 0.01), (0.35, 0.15), (0.35, 0.025), (0.55, 0.25), (0.282, 0.1), (0.36, 0.025)]
dir_0 = "integral_0.5"
dir_1 = "integral_1.0"
dir_2 = "integral_1.5"
save_dir = "integral"
filename_center = 'centerwall-int.txt'
filename_side = 'sidewall-int.txt'

fig, axes = plt.subplots(2, 3, figsize=(16, 8))
file_paths = [os.path.join(dir_0, filename_center), os.path.join(dir_1, filename_center), os.path.join(dir_2, filename_center), os.path.join(dir_0, filename_side), os.path.join(dir_1, filename_side), os.path.join(dir_2, filename_side)]
labels = ['center Vmax = 0.5', 'center Vmax = 1.0', 'center Vmax = 1.5', 'side Vmax = 0.5', 'side Vmax = 1.0', 'side Vmax = 1.5']

for i in range(len(file_paths)):
    row = i // 3
    col = i % 3
    x, y = read_data(file_paths[i])
    plot_and_save_integral(axes[row, col], x, y, label=labels[i], text_pos=integral_text_positions[i])
    axes[row, col].text(0.02, 0.9, subplot_labels[i], transform=axes[row, col].transAxes, fontsize=12, weight='bold')

plt.subplots_adjust(wspace=0.225, hspace=0.5)
plt.savefig(os.path.join(save_dir, "combined_integral.png"))
plt.show()
