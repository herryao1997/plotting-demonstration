# centerwallplotting.py
import matplotlib.pyplot as plt
import numpy as np

def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    x, y = [], []
    for line in lines:
        data = line.strip().split(' ')
        y.append(float(data[1]))
        x.append(float(data[2]))
    return x, y

def calculate_integral(x, y):
    return np.trapz(y, x)

def plot_centerwall(ax, filepath, velocity_label, color='blue', alpha_fill=0.5):
    x, y = read_data(filepath)
    ax.plot(x, y, color=color, label=velocity_label)
    ax.fill_between(x, y, color=color, alpha=alpha_fill)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Particle accumulation rate (#/s)')
    ax.legend()
    integral_value = calculate_integral(x, y)
    ax.text(0.5, 0.022, f'Total particle: ${integral_value:.4f}$', color='red', fontsize=12, transform=ax.transAxes)
    ax.set_xlim(0, 40)
    ax.set_ylim(0, None)

def main():
    fig, ax = plt.subplots()
    file1 = 'centerwall-int.txt'
    plot_centerwall(ax, file1, 'center_maximum_velocity_0.5')
    plt.savefig("centerwall_integral_0.5.png")
    plt.show()

if __name__ == "__main__":
    main()
