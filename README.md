# Traffic_simulation_Model

## Description

Vehicle traffic simulation model that resembles a macroscopic vehicle traffic simulation model. This model focuses on the simulation of the interaction between vehicles and traffic signals at an intersection, using a macroscopic approach to represent traffic behavior at the intersection level.

The model is based on several key concepts of macroscopic vehicle traffic simulation:

* `Traffic Signals`: The model uses traffic signals to control the flow of vehicles at the intersection. Signals have green, yellow, and red light times, which are updated based on a timer. This approach is similar to how real traffic signals control the flow of vehicles at intersections.

* `Vehicles and Directions`: Vehicles are represented as objects with attributes such as speed, direction, and whether they are going to turn or not. Vehicles move in specific directions (right, down, left, up) and can turn if they are allowed to do so. This macroscopic approach allows for modeling traffic behavior at the intersection level, rather than focusing on the individual behavior of each vehicle.

* `Vehicle Movement`: Vehicles move based on traffic signals and intersection conditions. The model implements logic to handle vehicle movement, including how they stop, turn, and move through the intersection. This is crucial for simulating realistic traffic flow at an intersection.

* `Vehicle Generation`: The model generates vehicles randomly at time intervals, randomly selecting the vehicle type, lane, and whether they are going to turn or not. This allows for simulating a variety of traffic situations at the intersection.

* `Time Simulation`: The model counts the elapsed time in the simulation and displays statistics such as the total number of vehicles that have crossed the intersection and the total time elapsed. This is useful for evaluating the performance of the traffic signal system.

> In summary, the model implemented in the code resembles a macroscopic vehicle traffic simulation model, using traffic signals to control the flow of vehicles at an intersection and representing vehicles as objects with specific attributes that determine their behavior. This approach allows for effectively simulating traffic behavior at the intersection level, providing a valuable tool for traffic planning and management.

## Table of Contents
- [Prerequisites](#Prerequisites)
- [Installation](#installation)
- [Usage](#usage)

### Prerequisites

You need:

-   [Python](https://www.python.org) (3.7 or newer)
## Installation

```shell
    pip install pygame-ce
    pip install matplotlib
    pip install scipy
    pip install numpy
    pip install pandas
```

## Usage

### Run The file:

```shell
    python simulation.py
```

[Simulation Time](simulation.py) (Line: 132):
```python
# `simulationTime` is the total duration of the simulation.
simulationTime = 300
```

### Buttons:

> Disabled (Peak Hour):

<img src="./images/buttons/buttonGo_small.png" width="115" height="115">

> Enabled (Peak Hour):

<img src="./images/buttons/buttonStop3_small.png" width="100" height="100">

> Info (Results Analysis)

<img src="./images/buttons/infoBlue.png" width="100" height="100">

Which displays the Simulation Results:

<img src="./Docs//images/Screenshot 2024-04-07 120700.png" width="100%" height="100%">
