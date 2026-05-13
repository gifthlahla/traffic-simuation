import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# FVADM model parameters
k = 0.1 # Parameter k
V1 = 10 # Parameter V1
V2 = 20 # Parameter V2
C1 = 10 # Parameter C1
C2 = 20 # Parameter C2
lambda_ = 0.5 # Parameter lambda
gamma = 0.1 # Parameter gamma

# Vehicle positions
x_l = 50 # Leader vehicle position
x = 40 # Follower vehicle position
l = 10 # Distance between vehicles
v_l = 30 # Leader vehicle speed
v = 20 # Follower vehicle speed
a = 5 # Vehicle acceleration

# Function defining the FVADM differential equation
def model_FVADM(v, t):
    return k * (V1 + V2 * np.tanh((C1 * (x_l - x - l)) / C2) - v) + lambda_ * (v_l - v) + gamma * a

# Simulation time
t = np.linspace(0, 300, 1000)

# Solving the differential equation
solution = odeint(model_FVADM, v, t)

# Plotting the solution
plt.plot(t, solution)
plt.xlabel('Time')
plt.ylabel('Follower vehicle speed')
plt.title('Full Velocity and Acceleration Difference Model')
plt.show()
