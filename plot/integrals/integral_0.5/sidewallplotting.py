# sidewallplotting.py
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

def plot(ax, filepath, label):
    x, y = read_data(filepath)
    ax.plot(x, y, color='blue', label=label)
    ax.fill_between(x, y, color='lightblue', alpha=0.5)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Particle accumulation rate (#/s)')
    ax.legend()
    integral_value = calculate_integral(x, y)
    ax.text(0.55, 0.25, f'total particle: ${integral_value:.4f}$', color='red', fontsize=12)

if __name__ == "__main__":
    fig, ax = plt.subplots()
    plot(ax, 'sidewall-int.txt', 'side_maximum_velocity_0.5')
    ax.set_xlim(0, 40)
    ax.set_ylim(0, None)
    plt.savefig("sidewall_integral_0.5.png")
    plt.show()
