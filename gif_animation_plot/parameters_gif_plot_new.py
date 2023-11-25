import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import math


class VelocityIntegralCalculator:
    def __init__(self, acceleration, distance):
        self.acceleration = acceleration
        self.distance = distance

    def calculate_time(self, max_velocity):
        accelerating_time = max_velocity / self.acceleration
        accelerating_distance = 0.5 * max_velocity * accelerating_time
        steady_distance = self.distance - 2 * accelerating_distance
        steady_time = steady_distance / max_velocity
        period = 2 * steady_time + 4 * accelerating_time

        return accelerating_time, steady_time, period

    def calculate_velocity(self, t, max_velocity):
        accelerating_time, steady_time, period = self.calculate_time(max_velocity)

        if t < accelerating_time:
            return self.acceleration * t
        elif t < (accelerating_time + steady_time):
            return max_velocity
        elif t < (3 * accelerating_time + steady_time):
            return max_velocity - self.acceleration * (t - (accelerating_time + steady_time))
        elif t < (3 * accelerating_time + 2 * steady_time):
            return -max_velocity
        else:
            return 0.0

    def calculate_mass_fraction(self, velocity):
        a = 0.0761846677
        alpha = 1.5485185961
        velocity = abs(velocity)
        if velocity < 1.67:
            return a * math.exp(alpha * velocity)
        else:
            return 1

    def calculate_max_velocity(self):
        accelerating_distance = 0.5 * self.distance
        accelerating_time = math.sqrt(2 * accelerating_distance / self.acceleration)
        max_velocity = self.acceleration * accelerating_time
        return max_velocity

    def plot_gif_range(self, min_velocity, max_velocity):
        step = (max_velocity - min_velocity) / 4
        vel = np.arange(min_velocity, max_velocity + step, step)
        vel[vel > max_velocity] = max_velocity

        max_time = 0
        for v in vel:
            _, _, period = self.calculate_time(v)
            if period > max_time:
                max_time = period

        time = np.linspace(0, max_time, 68)
        velocities = np.zeros((len(vel), len(time)))
        mass_fractions = np.zeros((len(vel), len(time)))

        for i in range(len(vel)):
            velocities[i] = np.vectorize(self.calculate_velocity)(time, vel[i])
            mass_fractions[i] = np.vectorize(self.calculate_mass_fraction)(velocities[i])

        fig, axs = plt.subplots(1, 3, figsize=(16, 6))

        lines1 = []
        for i in range(len(vel)):
            line1, = axs[0].plot([], [], label=f"Max Velocity: {vel[i]:.2f} m/s")
            lines1.append(line1)
        axs[0].set_xlim(0, max_time)
        axs[0].set_ylim(-max_velocity - 1, max_velocity + 1)
        axs[0].grid(True)
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('Velocity (m/s)')
        axs[0].set_title('Velocity vs Time')
        axs[0].legend()

        lines2 = []
        for i in range(len(vel)):
            line2, = axs[1].plot([], [], label=f"Max Velocity: {vel[i]:.2f} m/s")
            lines2.append(line2)
        axs[1].set_xlim(0, max_time)
        axs[1].set_ylim(0, 1.05)
        axs[1].grid(True)
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel('Normalized Mass Fraction')
        axs[1].set_title('Mass Fraction vs Time')

        axs[1].legend()

        markers = []
        annotations = []
        red_lines = []

        for i in range(len(vel)):
            marker, = axs[2].plot([], [], 'o', markersize=8)
            markers.append(marker)

            annotation = axs[2].annotate("", xy=(0, 0), xytext=(10, -20), textcoords="offset points",
                                        color=marker.get_color(), weight="bold")
            annotations.append(annotation)

            red_line, = axs[2].plot([], [], '--', color=marker.get_color(), linewidth=1.5)
            red_lines.append(red_line)

        def find_zero(input_function, low, high, precision):
            # Use the bisection method to find the root of the function
            while abs(high - low) > precision:
                mid = (low + high) / 2
                f_mid = input_function(mid)
                if f_mid == 0:
                    return mid
                elif f_mid * input_function(low) < 0:
                    high = mid
                else:
                    low = mid
            return (low + high) / 2

        # Define the search range and precision for the bisection method
        low = -2.0
        high = 0.0
        precision = 1e-6

        zero_value = find_zero(self.calculate_mass_fraction, low, high, precision)
        x = np.linspace(zero_value, 2, 100)
        y = np.vectorize(self.calculate_mass_fraction)(x)
        background_line, = axs[2].plot([], [], '--', color='gray', linewidth=1)
        axs[2].plot(x, y, color='gray')

        axs[2].set_xlim(-0.1, 2)
        axs[2].set_ylim(-0.1, 1.1)
        axs[2].grid(True)
        axs[2].set_xlabel('Velocity (m/s)')
        axs[2].set_ylabel('Normalized Mass Fraction')
        axs[2].set_title('Absolute Velocity vs Mass Fraction')
        axs[2].legend(markers, [f"Max Velocity: {vel[i]:.2f} m/s" for i in range(len(vel))])

        def update(num):
            for i in range(len(vel)):
                lines1[i].set_data(time[:num], velocities[i][:num])
                lines2[i].set_data(time[:num], mass_fractions[i][:num])

                markers[i].set_data(np.abs(velocities[i][num]), mass_fractions[i][num])

                current_time = time[num]
                annotation_text = f"({velocities[i][num]:.2f}, {mass_fractions[i][num]:.2f}, {current_time:.2f})"
                annotation_text += f"\nMax Velocity: {vel[i]:.2f} m/s"
                annotations[i].set_text(annotation_text)
                annotations[i].xy = (np.abs(velocities[i][num]), mass_fractions[i][num])
                annotations[i].set_color(markers[i].get_color())

                red_lines[i].set_data([velocities[i][num], velocities[i][num]], [0, mass_fractions[i][num]])

            return lines1 + lines2 + markers + annotations + red_lines

        ani = animation.FuncAnimation(fig, update, frames=len(time), interval=100, blit=True)

        plt.suptitle("Velocity and Mass Fraction vs. Time")
        plt.tight_layout()
        ani.save('velocity_massfraction_animation_cases.gif', writer='pillow', fps=15)
        plt.show()


# 示例用法
acceleration = 0.5
distance = 7.3
calculator = VelocityIntegralCalculator(acceleration, distance)
calculator.plot_gif_range(0.5, 2.0)
