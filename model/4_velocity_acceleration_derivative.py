import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Time and speed data
time_arr = np.array([0, 2, 4, 6, 8, 10])
velocity = np.array([0, 10, 20, 30, 40, 50])

# Speed interpolation
time_interp = np.arange(0, 10.1, 0.1)
f = interp1d(time_arr, velocity, kind='cubic')
velocity_interp = f(time_interp)

# Speed extrapolation
time_extrap = np.arange(0, 12.1, 0.1)
f = interp1d(time_arr, velocity, kind='cubic', fill_value="extrapolate")
velocity_extrap = f(time_extrap)

# Acceleration calculation as velocity derivative
acceleration_interp = np.diff(velocity_interp) / np.diff(time_interp)
acceleration_extrap = np.diff(velocity_extrap) / np.diff(time_extrap)

# Plots
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(time_arr, velocity, 'o', time_interp, velocity_interp, '-', time_extrap, velocity_extrap, '--')
plt.title('Velocity vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.legend(['Data', 'Interpolation', 'Extrapolation'])

plt.subplot(2, 1, 2)
plt.plot(time_interp[:-1], acceleration_interp, '-', time_extrap[:-1], acceleration_extrap, '--')
plt.title('Acceleration vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.legend(['Interpolation', 'Extrapolation'])

plt.tight_layout()
plt.show()