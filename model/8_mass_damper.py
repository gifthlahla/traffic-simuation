import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# system parameters
m = 1000  # mass (kg)
b = 0.5  # damping coefficient (Ns/m)
k = 200  # spring constant (N/m)

# Initial Conditions
x0 = 1  # initial position
v0 = 0  # Initial velocity (m/s)

# Simulation Time
t = np.linspace(0, 20, 1000)  # from t=0 to t=20

# Definition of motion equations
def ode(y, t, b, k, m):
    x, v = y
    dydt = [v, -(b/m) * v + -(k/m) * x]
    return dydt

# Solving motion equations
y0 = [x0, v0]
sol = odeint(ode, y0, t, args=(b, k, m))

# Visualization of position vs time
plt.figure()
plt.subplot(2,1,1)
plt.plot(t, sol[:, 0], 'b', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title("Position vs Time of the Mass-Spring-Damper System")

# Visualization of velocity vs time
plt.subplot(2,1,2)
plt.plot(t, sol[:, 1], 'b', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title("Velocity vs Time of the Mass-Spring-Damper System")

plt.tight_layout()
plt.show()