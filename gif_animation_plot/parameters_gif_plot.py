import math

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


class VelocityEmissionCalculator:
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


acceleration = 0.5  # m/s^2
distance = 7.25  # m
# maxVelocity = 0.5 #m/s
maxVelocity = 1.0 #m/s
# maxVelocity = 1.5 #m/s


emission_calculator = VelocityEmissionCalculator(acceleration, distance)

accelerationTime, steadyTime, period = emission_calculator.calculate_time(maxVelocity)


# Define the search range and precision for the bisection method
low = -2.0
high = 0.0
precision = 1e-6

emission = emission_calculator.calculate_particle_number_source

# Perform the bisection method search
zero_value = find_zero(emission, low, high, precision)

print("The approximate input value 'v' for which the function returns 0 is:", zero_value)

# --------create time series------
time = np.linspace(0, period, int(period*2))
# calc on time
velocity = np.vectorize(emission_calculator.calculate_velocity)(time, maxVelocity)
mass_fraction = np.vectorize(emission)(np.abs(velocity))

# create figure object
fig, (ax, bx, cx) = plt.subplots(1, 3, figsize=(15, 5))
line1, = ax.plot([], [], color='blue')
line2, = bx.plot([], [], color='red')

# set figure properties
ax.set_xlabel('Time (s)')
ax.set_ylabel('Velocity (m/s)')
ax.set_title('Velocity vs Time',pad = 15)
ax.grid()
ax.set_xlim(0, period)
# ax.set_ylim(-0.8, 0.8)
# ax.set_ylim(-1.2, 1.2)
ax.set_ylim(-1.7, 1.7)


bx.set_xlabel('Time (s)')
bx.set_ylabel('Particles Emission Number Rate (#/s)')
bx.set_title('Mass Fraction vs Time',pad = 15)
bx.grid()
bx.set_xlim(0, period)
bx.set_ylim(0, 5000000)
cx.set_xlabel('Absolute Velocity (m/s)')
cx.set_ylabel('Particles Emission Number Rate (#/s)')
cx.set_title('Absolute Velocity vs Particle Number',pad = 15)
cx.set_xlim(zero_value-0.1, 2)
# cx.set_ylim(0, None)
cx.grid(True)

# plot background mass fraction vs velocity
x = np.linspace(zero_value, 2, 100)
y = np.vectorize(emission)(x)
cx.plot(x, y, color='gray')

# Create a marker for current point
marker, = cx.plot([], [], 'bo', markersize=8)

# Create annotation for current point
annotation = cx.annotate('', xy=(0, 0), xytext=(10, -20), textcoords='offset points', color='red', weight='bold')

# Create red lines
line3a, = cx.plot([], [], '--', color='red', linewidth=1.5)
line3b, = cx.plot([], [], '--', color='red', linewidth=1.5)

# adjust subplot spacing
plt.subplots_adjust(wspace=0.3)


# Update function
def update(num, time, velocity, mass_fraction, line1, line2, marker, annotation, line3a, line3b):
    line1.set_data(time[:num], velocity[:num])
    line2.set_data(time[:num], mass_fraction[:num])

    # Update marker position
    marker.set_data(np.abs(velocity[num]), mass_fraction[num])

    # Update annotation text and position
    current_time = time[num]
    annotation.set_text(f"({velocity[num]:.2f}, {mass_fraction[num]:.1e}, {current_time:.2f})")
    annotation.xy = (np.abs(velocity[num]), mass_fraction[num])

    # Update red lines
    line3a.set_data([np.abs(velocity[num]), np.abs(velocity[num])], [0, mass_fraction[num]])
    line3b.set_data([0, np.abs(velocity[num])], [mass_fraction[num], mass_fraction[num]])

    return line1, line2, marker, annotation, line3a, line3b


ani = animation.FuncAnimation(fig, update, frames=len(time),
                              fargs=(time, velocity, mass_fraction, line1, line2, marker, annotation, line3a, line3b),
                              interval=100)

# save as GIF
# ani.save('velocity_massfraction_animation.gif', writer='pillow', fps=15)
# ani.save('velocity_massfraction_animation_1.0.gif', writer='pillow', fps=15)
ani.save('velocity_massfraction_animation_1.5.gif', writer='pillow', fps=15)
plt.show()
