import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define model parameters
num_simulations = 1000
num_vehicles = 220
average_speed = 80 # km/h
speed_deviation = 10 # km/h
num_vehicles_peak_hour = 330  # Increase in vehicles during peak hour
probability_peak_hour = 0.25  # Probability that it is peak hour

# Initialize list to store results
simulation_results: list = []

# Run the simulation
for _ in range(num_simulations):
    # Determine if it is peak hour
    is_peak_hour: bool = np.random.rand() < probability_peak_hour

    # Adjust the number of vehicles depending on whether it is peak hour
    num_vehicles_simulation: int  = num_vehicles_peak_hour if is_peak_hour else num_vehicles

    # Generate random speeds for the vehicles
    speeds = np.random.normal(average_speed, speed_deviation, num_vehicles_simulation)

    # Simulation test
    average_travel_time = np.mean(speeds) / 60 # Convert to hours

    # push results to the list
    simulation_results.append(average_travel_time)

# Convert the results list to a DataFrame for analysis
df_results: pd.DataFrame = pd.DataFrame(simulation_results, columns=['Average Travel Time'])

# Analyze the results
mean_travel_time: float = df_results['Average Travel Time'].mean()
deviation_travel_time: float = df_results['Average Travel Time'].std()

print(f"Average travel time: {mean_travel_time:.2f} hours")
print(f"Standard deviation of travel time: {deviation_travel_time:.2f} hours")

# Plot histogram of the results
plt.hist(simulation_results, bins=30, edgecolor='black')

# labels
plt.title('Distribution of Bulawayo Simulation Results')
plt.xlabel('Result Value') # x-axis: Represents the average travel time in hours
plt.ylabel('Frequency') # y-axis: Represents the frequency of each value

# Show the plot
plt.show()
