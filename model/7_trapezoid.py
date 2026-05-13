import numpy as np
import matplotlib.pyplot as plt

# Define time from 0 to 300 seconds
t = np.arange(0, 300, 0.1)

# Define the velocity function
v = 4*t - 2

# Displacement
displacement = np.trapezoid(v, t) / 1000 # km

# Absolute speed
v_abs = np.abs(4*t - 2)

# Total distance
total_distance = np.trapezoid(v_abs, t) / 1000 # km

# Create bar chart
labels = ['Displacement', 'Total Distance Traveled']
values = [displacement, total_distance]

plt.bar(labels, values)
plt.ylabel('Kilometers')
plt.title('Displacement and Total Distance Traveled')
plt.show()