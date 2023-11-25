import math

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

period = 34.0
accelerationTime = 2.0
decelerationTime = 2 * accelerationTime
steadyTime = (period - accelerationTime * 4) / 2
maxVelocity = 0.5
acceleration = maxVelocity / accelerationTime


def calculate_velocity(t):
    # t = t % period

    if t < accelerationTime:
        # acceleration period
        return acceleration * t
    elif t < (accelerationTime + steadyTime):
        # forward steady
        return maxVelocity
    elif t < (accelerationTime + steadyTime + decelerationTime):
        # forward deceleration
        return maxVelocity - acceleration * (t - (accelerationTime + steadyTime))
    elif t < (accelerationTime + steadyTime * 2 + decelerationTime):
        # backward steady
        return -maxVelocity
    else:
        # backward deceleration
        return -maxVelocity + acceleration * (t - (accelerationTime + steadyTime * 2 + decelerationTime))


a = 0.0761846677
alpha = 1.5485185961


def calculate_mass_fraction(v):
    v = abs(v)
    if v <= 1.67:
        return a * math.exp(alpha*v)
    else:
        return 1


# find the zero point of the function
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

# Perform the bisection method search
zero_value = find_zero(calculate_mass_fraction, low, high, precision)

print("The approximate input value 'v' for which the function returns 0 is:", zero_value)

# --------create time series------
time = np.linspace(0, period, 68)
# calc on time
velocity = np.vectorize(calculate_velocity)(time)
mass_fraction = np.vectorize(calculate_mass_fraction)(np.abs(velocity))

# create figure object
fig, (ax, bx, cx) = plt.subplots(1, 3, figsize=(15, 5))
line1, = ax.plot([], [], color='blue')
line2, = bx.plot([], [], color='red')

# set figure properties
ax.set_xlabel('Time (s)')
ax.set_ylabel('Velocity (m/s)')
ax.set_title('Velocity vs Time')
ax.grid()
ax.set_xlim(0, 35)
ax.set_ylim(-0.8, 0.8)
bx.set_xlabel('Time (s)')
bx.set_ylabel('Normalized Mass Fraction')
bx.set_title('Mass Fraction vs Time')
bx.grid()
bx.set_xlim(0, 35)
bx.set_ylim(0, 1.0)
cx.set_xlabel('Absolute Velocity (m/s)')
cx.set_ylabel('Normalized Mass Fraction')
cx.set_title('Absolute Velocity vs Mass Fraction')
cx.set_xlim(zero_value-0.1, 2)
cx.set_ylim(0, 1.1)
cx.grid(True)

# plot background mass fraction vs velocity
x = np.linspace(zero_value, 2, 100)
y = np.vectorize(calculate_mass_fraction)(x)
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
    annotation.set_text(f"({velocity[num]:.2f}, {mass_fraction[num]:.2f}, {current_time:.2f})")
    annotation.xy = (np.abs(velocity[num]), mass_fraction[num])

    # Update red lines
    line3a.set_data([np.abs(velocity[num]), np.abs(velocity[num])], [0, mass_fraction[num]])
    line3b.set_data([0, np.abs(velocity[num])], [mass_fraction[num], mass_fraction[num]])

    return line1, line2, marker, annotation, line3a, line3b


ani = animation.FuncAnimation(fig, update, frames=len(time),
                              fargs=(time, velocity, mass_fraction, line1, line2, marker, annotation, line3a, line3b),
                              interval=100)

# save as GIF
ani.save('velocity_massfraction_animation.gif', writer='pillow', fps=15)
plt.show()
