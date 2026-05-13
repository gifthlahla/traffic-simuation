import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# System parameters
m = 1350 # mass (kg)
c = 600 # damping coefficient (Ns/m)
k = 1500 # spring constant (N/m)

# Initial conditions
x0 = 0 # initial position
v0 = 20 # initial velocity (m/s)

# Definition of motion equations
def vehicle_dynamics(x, t, m, c, k):
    dxdt = np.zeros(2)
    dxdt[0] = x[1]
    
    leader_speed = 20 + 5*np.sin(0.5*t)
    dxdt[1] = (-c*x[1] - k*(x[0] - leader_speed)) / m
    
    return dxdt

# Solving motion equations
y0 = [x0, v0]
t = np.linspace(0, 60, 1000)
sol = odeint(vehicle_dynamics, y0, t, args=(m, c, k), atol=1e-9, rtol=1e-6)

# Visualization of position vs time
plt.figure()
plt.subplot(2,1,1)
plt.plot(t, sol[:, 0])
plt.title('Follower vehicle Position')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')

# Visualization of velocity vs time
plt.subplot(2,1,2)
plt.plot(t, sol[:, 1])
plt.title('Follower vehicle Speed')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')

plt.tight_layout()
plt.show()

plt.tight_layout()
plt.show()