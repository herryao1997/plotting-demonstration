import numpy as np
import matplotlib.pyplot as plt
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
        elif t < period:
            return -max_velocity + acceleration * (t - (3*accelerating_time+2*steady_time))
        else:
            return 0.0

    def calculate_particle_number_source(self, velocity):
        a = 0.0761846677
        alpha = 1.5485185961
        velocity = abs(velocity)
        normalized_particle_number_source = 5e6
        if velocity < 1.67:
            return a * math.exp(alpha * velocity) * normalized_particle_number_source
        else:
            return normalized_particle_number_source

    def calculate_max_velocity(self):
        accelerating_distance = 0.5 * self.distance
        accelerating_time = math.sqrt(2 * accelerating_distance / self.acceleration)
        max_velocity = self.acceleration * accelerating_time
        return max_velocity

    def calculate_integral_velocity_range(self, velocity_range, time_steps=1000):
        integrals = []
        min_integral = np.inf
        max_integral = -np.inf
        min_integral_point = (0, 0)
        max_integral_point = (0, 0)
        max_velocity = self.calculate_max_velocity()

        for velocity in velocity_range:
            if velocity > max_velocity:
                velocity = max_velocity
            # _, _, period = self.calculate_time(velocity)
            period = 40
            times = np.linspace(0, period, time_steps)
            velocities = np.vectorize(self.calculate_velocity)(times, velocity)
            mass_fract = np.vectorize(self.calculate_particle_number_source)(velocities)
            integral = np.trapz(mass_fract, times)
            integrals.append(integral)

            if integral < min_integral:
                min_integral = integral
                min_integral_point = (velocity, integral)
            if integral > max_integral:
                max_integral = integral
                max_integral_point = (velocity, integral)

        return integrals, min_integral_point, max_integral_point, max_velocity

    def plot_integral_velocity_range(self, velocity_range, integrals, min_integral_point, max_integral_point, max_velocity):
        fig, ax = plt.subplots()
        ax.plot(velocity_range, integrals)

        ax.scatter(*min_integral_point, color='green')
        ax.annotate(f"Min Integral Point\n({min_integral_point[0]:.2f}, {min_integral_point[1]:.1e})",
                    xy=min_integral_point, xytext=(12, 10), fontsize=8,
                    textcoords='offset points', arrowprops=None, color='green')

        ax.scatter(*max_integral_point, color='red')
        ax.annotate(f"Max Integral Point\n({max_integral_point[0]:.2f}, {max_integral_point[1]:.1e})",
                    xy=max_integral_point, xytext=(-85, -30), fontsize=8,
                    textcoords='offset points', arrowprops=None, color='red')

        ax.scatter(max_velocity, integrals[-1], color='blue')
        ax.annotate(f"Max Reachable Velocity Point\n({max_velocity:.2f}, {integrals[-1]:.1e})",
                    xy=(max_velocity, integrals[-1]), xytext=(10, -30), fontsize=8,
                    textcoords='offset points', arrowprops=None, color='blue')

        plt.plot([min_integral_point[0], min_integral_point[0]], [min_integral_point[1], 0], color='green', linestyle='dashed')
        plt.plot([min_integral_point[0], 0], [min_integral_point[1], min_integral_point[1]], color='green', linestyle='dashed')

        plt.plot([max_integral_point[0], max_integral_point[0]], [max_integral_point[1], 0], color='red', linestyle='dashed')
        plt.plot([max_integral_point[0], 0], [max_integral_point[1], max_integral_point[1]], color='red', linestyle='dashed')

        plt.plot([max_velocity, max_velocity], [integrals[-1], 0], color='blue', linestyle='dashed')
        plt.plot([max_velocity, 0], [integrals[-1], integrals[-1]], color='blue', linestyle='dashed')

        plt.xlim(velocity_range[0] - 0.1, velocity_range[-1])
        plt.ylim(min(integrals)-5e5, max(integrals)+5e5)

        # ax.text(2.5, 3e7, r"$PE_{total} = \int_{0}^{period} ER(v) \cdot dt$",
        #         fontsize=12, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
        ax.text(2.5, 3e7, r"$PE_{total} = \int_{0}^{period_{longest}} ER(v) \cdot dt$",
                fontsize=12, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})


        plt.xlabel('Max Velocity (m/s)')
        plt.ylabel('Total Particle Emission Number')
        plt.title('Integral of Total Particle Emission Number vs Max Velocity', pad=15)
        plt.tight_layout()

        # plt.savefig('integral_of_emission.png')
        plt.savefig('integral_for_34s.png')
        plt.show()


if __name__ == '__main__':
    acceleration = 0.5  # m/s^2
    distance = 7.25  # m
    velocity_range = np.linspace(0.5, 5, 100)  # maximum

    integral_calculator = VelocityIntegralCalculator(acceleration, distance)
    integrals, min_integral_point, max_integral_point, max_velocity = integral_calculator.calculate_integral_velocity_range(velocity_range)
    integral_calculator.plot_integral_velocity_range(velocity_range, integrals, min_integral_point, max_integral_point, max_velocity)
