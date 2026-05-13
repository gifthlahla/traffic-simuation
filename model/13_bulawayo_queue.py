import numpy as np
import matplotlib.pyplot as plt

# Parameters
lambda_ = 2  # average time between arrivals, in minutes
mu = 1  # average service time, in minutes
sigma = 0.5  # standard deviation of service time in minutes
N = 1000  # number of simulations

waiting_time = np.zeros(N)

for i in range(N):
    arrivals = np.cumsum(np.random.exponential(lambda_, 100))  # 100 vehicles
    service_start = max(0, arrivals[0] - np.random.normal(mu, sigma))
    service_end = service_start + np.random.normal(mu, sigma)
    waiting = service_start - arrivals[0]

    for j in range(1, len(arrivals)):
        service_start = max(service_end, arrivals[j])
        service_end = service_start + np.random.normal(mu, sigma)
        waiting += service_start - arrivals[j]

    waiting_time[i] = waiting / len(arrivals)

mean_waiting = np.mean(waiting_time)
waiting_deviation = np.std(waiting_time)

# Plot of waiting times
plt.hist(waiting_time, bins=20)
plt.xlabel('Average Waiting Time (Minutes)')
plt.ylabel('Frequency')
plt.title('Distribution of average waiting time in interaction')
plt.show()