import numpy as np
import matplotlib.pyplot as plt

# System parameters
_lambda = 6  # Vehicle arrival rate
mu = 5  # Service rate
c = 4  # Number of servers
K = 10  # Maximum number of vehicles in the system

# Probability that the system is in state i
pi = np.zeros(K+1)
pi[0] = 1
for i in range(1, c+1):
    pi[i] = (_lambda/mu)**i * pi[0]
for i in range(c+1, K+1):
    pi[i] = (_lambda/(c*mu))**i * pi[0]
pi[0] = 1 / np.sum(pi)

# Average number of vehicles in the system
L = np.sum(pi * np.arange(0, K+1))

# Probability that an arriving vehicle has to wait
P_wait = 1 - np.sum(pi[:c+1])

# Plot of probability distribution
plt.figure()
plt.bar(np.arange(0, K+1), pi)
plt.xlabel('Number of vehicles in the system')
plt.ylabel('Probability')
plt.title('Probability distribution of the number of vehicles in the system')
plt.show()

# Print statistics
print(f'Average number of vehicles in the system: {L:.2f}')
print(f'Probability that an arriving vehicle has to wait: {P_wait:.2f}')