import numpy as np
import matplotlib.pyplot as plt

final_time = 30  # seconds
dt = 0.1

# initial conditions for vehicle 1
position1 = 0
velocity1 = 0
acceleration1 = 3

# initial conditions for vehicle 2
position2 = 0
velocity2 = 0
acceleration2 = 1.5

# Figure preparation for simulation
plt.figure()
plt.grid(True)
plt.xlabel('time (s)')
plt.ylabel('Position (m)')

# Lists to store positions and times
times = []
positions1 = []
positions2 = []

# for simulation
for t in np.arange(0, final_time+dt, dt):
    # Update Positions and Speeds
    position1 = position1 + velocity1 * dt
    velocity1 = velocity1 + acceleration1 * dt

    position2 = position2 + velocity2 * dt
    velocity2 = velocity2 + acceleration2 * dt

    # Store times and positions
    times.append(t)
    positions1.append(position1)
    positions2.append(position2)

# Plot
plt.plot(times, positions1, 'r-')
plt.plot(times, positions2, 'b-')

plt.title('Trajectory of two vehicles')
plt.legend(['Vehicle 1', 'Vehicle 2'])
plt.show()