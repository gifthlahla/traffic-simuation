import numpy as np
from scipy.integrate import cumulative_trapezoid
import matplotlib.pyplot as plt

# Time range
t = np.arange(0, 300.1, 0.1)

# Velocity of vehicles A and B
v_A = 3*t
v_B = 3*t + 4

# Displacement using numerical integration
s_A = cumulative_trapezoid(v_A, t, initial=0)
s_B = cumulative_trapezoid(v_B, t, initial=0)

# Plot Velocity vs. Time
plt.figure()
plt.subplot(2,1,1)
plt.plot(t, v_A, 'b-', t, v_B, 'r--')
plt.legend(['Velocity A', 'Velocity B'])
plt.title('Velocity vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')

# Plot Displacement vs. Time
plt.subplot(2,1,2)
plt.plot(t, s_A, 'b-', t, s_B, 'r--')
plt.legend(['Displacement A', 'Displacement B'])
plt.title('Displacement vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')

plt.tight_layout()
plt.show()