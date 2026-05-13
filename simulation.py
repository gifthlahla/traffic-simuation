import random
import time
import threading
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pygame
import sys
from module.Result import Presentation_Result

# Run the simulation
run_simulation = True
# Default signal timer values
defaultGreen = {
    0: 10,
    1: 10,
    2: 10,
    3: 10
}
# Default red signal time
defaultRed = 150
# Default yellow signal time
defaultYellow = 5

# Signal list
signals = []

# Number of signals
noOfSignals = 4

# Indicates which signal is currently green
currentGreen = 0

# Indicates which signal will turn green next
nextGreen = (currentGreen+1) % noOfSignals

# Indicates if the yellow signal is on or off
currentYellow = 0

# average vehicle speeds in px/s to m/s
speeds = {
    'car': 2.25,
    'bus': 1.8,
    'truck': 1.8,
    'bike': 2.5
}

# Vehicle starting coordinates

# original
x = {
 'right': [0, 0, 0],
 'down': [755, 727, 697],
 'left': [1400, 1400, 1400],
 'up': [602, 627, 657],
 'vertical': [800, 800, 800]
}

y = {
 'right': [348, 370, 398],
 'down': [0, 0, 0],
 'left': [498, 466, 436],
 'up': [800, 800, 800],
 'vertical': [800, 800, 800]
}

# Characteristic vehicles
vehicles = {
    'right': {0: [], 1: [], 2: [], 'crossed': 0},
    'down': {0: [], 1: [], 2: [], 'crossed': 0},
    'left': {0: [], 1: [], 2: [], 'crossed': 0},
    'up': {0: [], 1: [], 2: [], 'crossed': 0},
    'vertical': {0: [], 1: [], 2: [], 'crossed': 0}
}

vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'bike'}

# Directions
directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

# Signal image, timer, and vehicle count coordinates
signalCoods = [(530, 230), (810, 230), (1000, 570), (530, 570)]
signalTimerCoods = [(530, 210), (810, 210), (1000, 550), (530, 550)]
signal_rotation = [0, 0, -0, 0] # signal rotation

# Stop line coordinates
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535,'vertical':535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545,'vertical':545}

# Gap between vehicles
stoppingGap = 25    # stopping gap
movingGap = 25   # moving gap

# allowed vehicle types
allowedVehicleTypes = {'car': True, 'bus': True, 'truck': True, 'bike': True}

# List of allowed vehicle types
allowedVehicleTypesList = []

vehiclesTurned = {
    'right': {1: [], 2: []},
    'down': {1: [], 2: []},
    'left': {1: [], 2: []},
    'up': {1: [], 2: []},
    'vertical': {1: [], 2: []}
}
vehiclesNotTurned = {
    'right': {1: [], 2: []},
    'down': {1: [], 2: []},
    'left': {1: [], 2: []},
    'up': {1: [], 2: []},
    'vertical': {1: [], 2: []}
}
rotationAngle = 3

# `mid` is a dictionary that stores central coordinates for each direction in the simulation.
# 'right', 'down', 'left', 'up' are the possible directions.
# 'x' and 'y' are the coordinates in the 2D simulation plane.
mid = {
    'right': {'x': 705, 'y': 445},
    'down': {'x': 695, 'y': 450},
    'left': {'x': 695, 'y': 425},
    'up': {'x': 695, 'y': 400},
    'vertical': {'x': 695, 'y': 425}
}

# random green signal
randomGreenSignalTimer = True


# `timeElapsed` is a variable that tracks the elapsed time in the simulation.
timeElapsed = 0

# `simulationTime` is the total duration of the simulation.
simulationTime = 300

# `timeElapsedCoods` are the coordinates on the screen where the elapsed time will be displayed.
timeElapsedCoods = (1000, 50)

# `vehicleCountTexts` is a list containing the vehicle count in each direction as text strings.
vehicleCountTexts = ["0", "0", "0", "0"]

# `vehicleCountCoods` are the coordinates on the screen where the vehicle count for each direction will be displayed.
vehicleCountCoods = [(480, 210), (880, 210), (1100, 550), (480, 550)]
# vehicleCountCoods = [(558, 79), (956, 184), (439, 360), (810, 516)]

# peak hour
peakHour = False

# simulation_vehicle
simulation_vehicle = []

# Pygame initialization
pygame.init()
simulation = pygame.sprite.Group()

# Presentation_Result
presentation_result = Presentation_Result(simulation_time=simulationTime)


class TrafficSignal:
    """
    The `TrafficSignal` class in Python represents a traffic signal with red, 
    yellow, and green light durations.
    """

    def __init__(self, red: int, yellow: int, green: int):
        """
        This Python function initializes an object with integer values for red, yellow, and green,
        along with an empty string for signalText.
        """
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane: int, vehicleClass: str, direction_number: int, direction: str, will_turn: int):
        """
        This function initializes a vehicle object with specific attributes and coordinates based on
        the direction and lane.

        :param `lane` int: 
            Represents the lane the vehicle is in. 

        :param `vehicleClass` str:
            Represents the class or type of the vehicle being initialized. 

        :param `direction_number` int: 
            Represents the numerical value associated with the direction the vehicle is moving (up, down...). 

        :param `direction` str: 
            Represents the direction the vehicle is moving. 

        :param `will_turn` int: 
            Represents whether the vehicle will turn or not. 
        """
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        self.willTurn = will_turn
        self.turned = 0
        self.rotateAngle = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        self.crossedIndex = 0
        # path of vehicle image
        path = f"images/{direction}/{vehicleClass}.png"
        originalImage = pygame.image.load(path)
        image = pygame.image.load(path)
        self.originalImage = pygame.transform.rotate(originalImage,0)
        self.image = pygame.transform.rotate(image,0)
        previousVehicle = vehicles[direction][lane][self.index-1]
        self.image_width = self.image.get_rect().width
        self.image_height = self.image.get_rect().height

        # Set stopping coordinate
        # If there is more than one vehicle in the lane and the previous vehicle has not crossed the stop line
        if (len(vehicles[direction][lane]) > 1 and previousVehicle.crossed == 0):
            width = previousVehicle.image.get_rect().width
            height = previousVehicle.image.get_rect().height
            # Set the current vehicle's stopping coordinate based on the direction
            if (direction == 'right'):
                self.stop = previousVehicle.stop - width - stoppingGap
            elif (direction == 'left'):
                self.stop = previousVehicle.stop + width + stoppingGap
            elif (direction == 'down'):
                self.stop = previousVehicle.stop - height - stoppingGap
            elif (direction == 'up'):
                self.stop = previousVehicle.stop + height + stoppingGap
        else:
            self.stop = defaultStop[direction]

        # Set new starting and stopping coordinate
        if (direction == 'right'):
            temp = self.image_width + stoppingGap
            x[direction][lane] -= temp
        elif (direction == 'left'):
            temp = self.image_width + stoppingGap
            x[direction][lane] += temp
        elif (direction == 'down'):
            temp = self.image_height + stoppingGap
            y[direction][lane] -= temp
        elif (direction == 'up'):
            temp = self.image_height + stoppingGap
            y[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        """
        The `render` function in Python takes a `screen` parameter and draws the `image` at 
        `(x, y)` coordinates.

        :param screen: 
            This parameter is used with the `blit` method
            to draw the image at the specified coordinates `(self.x, self.y)` on the screen.
        """
        screen.blit(self.image, (self.x, self.y))

    def Move_right(self):
        """
        The `Move_right` function in Python handles vehicle movement based on various
        conditions, such as crossing stop lines, turning, and maintaining gaps between vehicles.
        """
        if (self.crossed == 0 and self.x + self.image_width > stopLines[self.direction]):
            self.crossed = 1
            vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(
                    vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            last_Vehicule = vehicles[self.direction][self.lane][self.index-1]
            x_with_width = self.x + self.image_width
            last_vehicles_turned = vehiclesTurned[self.direction][self.lane][self.crossedIndex -
                                                                             1] if self.crossedIndex != 0 else None

            if self.lane == 1:
                if self.crossed == 0 or x_with_width < stopLines[self.direction]+40:
                    can_move_forward = x_with_width <= self.stop or (
                        currentGreen == 0 and currentYellow == 0) or self.crossed == 1
                    is_first_vehicle_or_has_gap = self.index == 0 or x_with_width < (
                        last_Vehicule.x - movingGap) or last_Vehicule.turned == 1

                    if can_move_forward and is_first_vehicle_or_has_gap:
                        self.x += self.speed
                else:
                    if self.turned == 0:
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x += 2.4
                        self.y -= 2.8

                        if self.rotateAngle == 90:
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        has_gap_to_previous_turned_vehicle = self.crossedIndex == 0 or self.y > (
                            last_vehicles_turned.y + last_vehicles_turned.image.get_rect().height + movingGap)

                        if has_gap_to_previous_turned_vehicle:
                            self.y -= self.speed
            elif self.lane == 2:
                x_with_width = self.x + self.image_width
                y_with_height = self.y + self.image_height

                if self.crossed == 0 or x_with_width < mid[self.direction]['x']:
                    can_move_forward = x_with_width <= self.stop or (
                        currentGreen == 0 and currentYellow == 0) or self.crossed == 1
                    is_first_vehicle_or_has_gap = self.index == 0 or x_with_width < (
                        last_Vehicule.x - movingGap) or last_Vehicule.turned == 1

                    if can_move_forward and is_first_vehicle_or_has_gap:
                        self.x += self.speed
                else:
                    if self.turned == 0:
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x += 2
                        self.y += 1.8

                        if self.rotateAngle == 90:
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        has_gap_to_previous_turned_vehicle = self.crossedIndex == 0 or y_with_height < (
                            vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap)

                        if has_gap_to_previous_turned_vehicle:
                            self.y += self.speed
        else:
            if (self.crossed == 0):
                if ((self.x+self.image_width <= self.stop or (currentGreen == 0 and currentYellow == 0)) and (self.index == 0 or self.x+self.image_width < (vehicles[self.direction][self.lane][self.index-1].x - movingGap))):
                    self.x += self.speed
            else:
                if ((self.crossedIndex == 0) or (self.x+self.image_width < (vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):
                    self.x += self.speed

    def Move_down(self):
        """
        This function controls the movement of vehicles in a simulation, including handling 
        intersection crossings and turns.
        """

        if (self.crossed == 0 and self.y+self.image_height > stopLines[self.direction]):
            self.crossed = 1
            vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(
                    vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            if (self.lane == 1):
                if (self.crossed == 0 or self.y+self.image_height < stopLines[self.direction]+50):
                    if ((self.y+self.image_height <= self.stop or (currentGreen == 1 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.image_height < (vehicles[self.direction][self.lane][self.index-1].y - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y += self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x += 1.2
                        self.y += 1.8
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or ((self.x + self.image_width) < (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):
                            self.x += self.speed
            elif (self.lane == 2):
                if (self.crossed == 0 or self.y+self.image_height < mid[self.direction]['y']):
                    if ((self.y+self.image_height <= self.stop or (currentGreen == 1 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.image_height < (vehicles[self.direction][self.lane][self.index-1].y - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y += self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x -= 2.5
                        self.y += 2
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.x > (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                            self.x -= self.speed
        else:
            if (self.crossed == 0):
                if ((self.y+self.image_height <= self.stop or (currentGreen == 1 and currentYellow == 0)) and (self.index == 0 or self.y+self.image_height < (vehicles[self.direction][self.lane][self.index-1].y - movingGap))):
                    self.y += self.speed
            else:
                if ((self.crossedIndex == 0) or (self.y+self.image_height < (vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):
                    self.y += self.speed

    def Move_left(self):
        """
        This function defines the movement behavior of a vehicle object in a simulation,
        including conditions for turning and lane changing.
        """

        if (self.crossed == 0 and self.x < stopLines[self.direction]):
            self.crossed = 1
            vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(
                    vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            if (self.lane == 1):
                if (self.crossed == 0 or self.x > stopLines[self.direction]-70):
                    if ((self.x >= self.stop or (currentGreen == 2 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x -= 1
                        self.y += 1.2
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or ((self.y + self.image_height) < (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):
                            self.y += self.speed
            elif (self.lane == 2):
                if (self.crossed == 0 or self.x > mid[self.direction]['x']):
                    if ((self.x >= self.stop or (currentGreen == 2 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x -= 1.8
                        self.y -= 2.5
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.y > (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):
                            self.y -= self.speed
        else:
            if (self.crossed == 0):
                if ((self.x >= self.stop or (currentGreen == 2 and currentYellow == 0)) and (self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap))):
                    self.x -= self.speed
            else:
                if ((self.crossedIndex == 0) or (self.x > (vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                    self.x -= self.speed

    def Move_up(self):
        """
        The "Move_up" function controls the vertical movement of vehicles based on various
        conditions, such as crossing lines, turning, lanes, and traffic signals.
        """
        if (self.crossed == 0 and self.y < stopLines[self.direction]):
            self.crossed = 1
            vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(
                    vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            if (self.lane == 1):
                if (self.crossed == 0 or self.y > stopLines[self.direction]-60):
                    if ((self.y >= self.stop or (currentGreen == 3 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x -= 2
                        self.y -= 1.2
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.x > (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                            self.x -= self.speed
            elif (self.lane == 2):
                if (self.crossed == 0 or self.y > mid[self.direction]['y']):
                    if ((self.y >= self.stop or (currentGreen == 3 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x += 1
                        self.y -= 1
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.x < (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width - movingGap))):
                            self.x += self.speed
        else:
            if (self.crossed == 0):
                if ((self.y >= self.stop or (currentGreen == 3 and currentYellow == 0)) and (self.index == 0 or self.y > (vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap))):
                    self.y -= self.speed
            else:
                if ((self.crossedIndex == 0) or (self.y > (vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].y + vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):
                    self.y -= self.speed

    def move(self):
        """
        The `move` function in Python selects a movement direction based on a dictionary and calls
        the corresponding method.
        """
        directios = {
            'right': self.Move_right,
            'down': self.Move_down,
            'left': self.Move_left,
            'up': self.Move_up
        }
        directios[self.direction]()


# Initialization of signals with default values
def initialize():
    """
    This function initializes the traffic signals with random or default values from the 
    green signal timer.
    """
    minTime = 10
    maxTime = 20
    if (randomGreenSignalTimer):
        ts1 = TrafficSignal(0, defaultYellow, random.randint(minTime, maxTime))
        signals.append(ts1)
        ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green,
                            defaultYellow, random.randint(minTime, maxTime))
        signals.append(ts2)
        ts3 = TrafficSignal(defaultRed, defaultYellow,
                            random.randint(minTime, maxTime))
        signals.append(ts3)
        ts4 = TrafficSignal(defaultRed, defaultYellow,
                            random.randint(minTime, maxTime))
        signals.append(ts4)
    else:
        ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
        signals.append(ts1)
        ts2 = TrafficSignal(ts1.yellow+ts1.green,
                            defaultYellow, defaultGreen[1])
        signals.append(ts2)
        ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])
        signals.append(ts3)
        ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])
        signals.append(ts4)

    repeat()

# Print the signal timers on Console


def print_traffic_signal_status():
    """
    This function prints the status of each traffic signal in the simulation.
    It iterates through a list of signals and prints their status based on their color and current state.
    """
    for i in range(4):
        if signals[i] is not None:
            signal = signals[i]
            signal_number = i + 1

            # current signal color for console
            if i == currentGreen:
                color = "YELLOW" if currentYellow == 1 else "GREEN"
            else:
                color = "RED"

            print(
                f"{color} TS{signal_number} -> r:{signal.red} y:{signal.yellow} g:{signal.green}")

    print()


def repeat():
    """
    This Python function controls traffic signal timings and transitions between
    green, yellow, and red signals in a loop.
    """
    global currentGreen, currentYellow, nextGreen
    # while the current green signal timer is not zero
    while (signals[currentGreen].green > 0):
        # print_traffic_signal_status()
        updateValues()
        time.sleep(1)

    currentYellow = 1   # set yellow signal on

    # Reset lane stop coordinates and vehicle coordinates
    for i in range(0, 3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]

    # while the current yellow signal timer is not zero
    while (signals[currentGreen].yellow > 0):
        # print_traffic_signal_status()
        updateValues()
        time.sleep(1)

    currentYellow = 0   # Reset yellow signal

    # Reset all current signal times to default/random times
    if (randomGreenSignalTimer):
        signals[currentGreen].green = random.randint(10, 20)
    else:
        signals[currentGreen].green = defaultGreen[currentGreen]

    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    currentGreen = nextGreen  # next signal as green signal

    nextGreen = (currentGreen+1) % noOfSignals    # next green signal

    # next signal's red time as (yellow time + green time) of the current signal
    signals[nextGreen].red = signals[currentGreen].yellow + \
        signals[currentGreen].green

    repeat()


# Update values of the signal timers after every second
def updateValues():
    """
    The `updateValues` function iterates through a range of signals and decreases their green,
    yellow, or red values based on certain conditions.
    """
    for i in range(0, noOfSignals):
        if (i == currentGreen):
            if (currentYellow == 0):
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1


# Generating vehicles in the simulation
def generateVehicles():
    """
    The "generateVehicles" function randomly selects vehicle types, lane numbers,
    turn probabilities, and directions to create vehicles at 1-second intervals.
    """
    global peakHour
    global run_simulation
    while peakHour == False:
        if run_simulation == False:
            break
        print("Vehicles are generating", peakHour)  
        vehicle_type = random.choice(allowedVehicleTypesList)

        # Random lane selection for the vehicle
        lane_number = random.randint(1, 2)

        # Random turn selection for the vehicle
        will_turn = random.randint(0, 99) < 40 if lane_number in [1, 2] else 0

        # Random direction selection for the vehicle
        temp = random.randint(0, 99)
        dist = [25, 50, 75, 100]
        direction_number = next(i for i, val in enumerate(dist) if temp < val)

        # vehicle instance
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number,
                directionNumbers[direction_number], will_turn)

        time.sleep(0.8)

def Traffic_generate():
    """
    The `Traffic_generate` function in Python prints a message to the console when the button is pressed.
    """
    global peakHour
    global run_simulation
    while peakHour:
        if run_simulation == False:
            break
        print("Traffic is generating", peakHour)
        vehicle_type = random.choice(allowedVehicleTypesList)

        # Random lane selection for the vehicle
        lane_number = random.randint(1, 2)

        # Random turn selection for the vehicle
        will_turn = random.randint(0, 99) < 40 if lane_number in [1, 2] else 0

        # Random direction selection for the vehicle
        temp = random.randint(0, 99)
        dist = [25, 50, 75, 100]
        direction_number = next(i for i, val in enumerate(dist) if temp < val)

        # vehicle instance
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number,
                directionNumbers[direction_number], will_turn)

        time.sleep(0.1)

def showStats():
    """
    The `showStats` function calculates and displays the total number of vehicles that have 
    crossed in each direction and the total time elapsed.
    """
    totalVehicles = 0
    print('Direction-wise Vehicle Counts')
    for i in range(0, 4):
        if (signals[i] != None):
            print(
                f"Direction {i+1}: {vehicles[directionNumbers[i]]['crossed']} vehicles crossed")
            totalVehicles += vehicles[directionNumbers[i]]['crossed']
    print('Total vehicles passed:', totalVehicles)
    print('Total time:', timeElapsed)


def simTime():
    """
    The `simTime` function increments `timeElapsed` by 1 every second until it reaches `simulationTime`,
    at which point it displays statistics and exits the program.
    """
    global timeElapsed, simulationTime, run_simulation
    while (True):
        timeElapsed += 1
        time.sleep(1)
        if (timeElapsed == simulationTime):
            showStats()
            run_simulation = False
            try:
                os._exit(1)
            finally:
                show_results()

def Thread_generate_traffic():
    """
    The `Thread_generate_traffic` function in Python creates a thread to generate traffic in the simulation.
    """
    thread1 = threading.Thread(
        name="generateTraffic",
        target=Traffic_generate,
        args=()
    )
    thread1.daemon = True
    thread1.start()


def Thread_generate_vehicle():
    """
    The `Thread_generate_vehicle` function in Python creates a thread to generate vehicles in the simulation.
    """
    thread2 = threading.Thread(
        name="generateVehicles",
        target=generateVehicles,
        args=()
    )
    thread2.daemon = True
    thread2.start()


def show_results():
    """
    The `show_results` function in Python displays simulation results in a popup window.
    """
    
    copy_simulation_vehicle = simulation_vehicle.copy()
    if len(copy_simulation_vehicle) >= 2:
        # Get a random index for 'leader' (excluding the first element)
        leader = random.randint(1, len(copy_simulation_vehicle) - 1)
        # Get 'follower' as the index before 'leader'
        follower = leader - 1
        type_vehicle = random.choice(allowedVehicleTypesList)

        presentation_result.exec_all_plots(
            simulation_vehicle=copy_simulation_vehicle, 
            leader=leader, 
            follower=follower,
            type_vehicle=vehicleTypes[type_vehicle], 
            speeds=speeds,
            simulationTime=simulationTime
        )


class Main:
    global allowedVehicleTypesList
    global peakHour
    global run_simulation
    i = 0
    # The code iterates over an "allowedVehicleTypes" dictionary and checks if the value of each key is
    # True. If the value is True, it adds the corresponding key to `allowedVehicleTypesList`.
    for vehicleType in allowedVehicleTypes:
        if (allowedVehicleTypes[vehicleType]):
            allowedVehicleTypesList.append(i)
        i += 1

    # Simulation initialization
    thread1 = threading.Thread(
        name="initialization", target=initialize, args=())    # initialization
    thread1.daemon = True
    thread1.start()

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Load button images
    button_image1 = pygame.image.load('images/buttons/buttonGo_small.png')
    button_image2 = pygame.image.load('images/buttons/buttonStop3_small.png')
    button_info = pygame.image.load('images/buttons/infoBlue.png')
    button_info = pygame.transform.scale(button_info, (100, 100))

    # Button coordinates (top left of the screen)
    button_rect = button_image1.get_rect(topleft=(screenWidth - button_image1.get_width(), 0))

    # Information button coordinates
    button_info_rect = button_info.get_rect(topleft=(screenWidth - button_image1.get_width() - 100, 10))

    # Button state
    button_state = 0

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/Av_casanovaV2.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Loading signal images and font
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)

    # threads for generating vehicles and simulation time

    # Generating vehicles
    Thread_generate_vehicle()

    # Time of simulation
    # TRAFFIC ENFORCER
    thread3 = threading.Thread(
        name="simTime",
        target=simTime,
        args=()
    )
    thread3.daemon = True
    thread3.start()
    def rotate(image, angle: float):
        return pygame.transform.rotate(image, angle)
    

    # Main loop (while program is running)
    while run_simulation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showStats()
                run_simulation = False
                try:
                    sys.exit()
                finally:
                    show_results()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si el botón fue presionado
                if button_rect.collidepoint(event.pos):
                    # Change button state
                    button_state = 1 - button_state
                    # Ejecutar la función
                    if button_state == 1:
                        peakHour = True
                        Thread_generate_traffic()
                    else:
                        peakHour = False
                        Thread_generate_vehicle()
                # Verificar si el botón fue presionado
                elif button_info_rect.collidepoint(event.pos):
                    # Ejecutar la función
                    run_simulation = False

                    show_results()

        screen.blit(background, (0, 0))   # display background in simulation
        # Show the correct button based on state
        if button_state == 0:
            # display the button
            screen.blit(button_image1, button_rect.topleft)
        else:
            # display the button
            screen.blit(button_image2, button_rect.topleft)

        # display the button
        screen.blit(button_info, button_info_rect.topleft)



        # display signal and set timer according to current status: green, yello, or red
        for i in range(0, noOfSignals):
            if (i == currentGreen):
                if (currentYellow == 1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(rotate(yellowSignal,signal_rotation[i]), signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(rotate(greenSignal,signal_rotation[i]), signalCoods[i])
            else:
                if (signals[i].red <= 10):
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "STOP"
                screen.blit(rotate(redSignal,signal_rotation[i]), signalCoods[i])
        signalTexts = ["", "", "", ""]

        # display signal timer
        for i in range(0, noOfSignals):
            signalTexts[i] = font.render(
                str(signals[i].signalText),
                True,
                white,
                black
            )
            screen.blit(signalTexts[i], signalTimerCoods[i])

        # display vehicle count
        # see how many vehicles have crossed
        for i in range(0, noOfSignals):
            displayText = vehicles[directionNumbers[i]]['crossed']
            vehicleCountTexts[i] = font.render(
                str(displayText),
                True,
                black,
                white
            )
            screen.blit(vehicleCountTexts[i], vehicleCountCoods[i])

        # display time elapsed
        # see simulation time
        timeElapsedText = font.render(
            (f"Time Elapsed: {str(timeElapsed)}"),
            True,
            black,
            white
        )
        screen.blit(timeElapsedText, timeElapsedCoods)

        # display the vehicles
        # this is where it's determined that the vehicle moves in some direction
        for vehicle in simulation:
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            simulation_vehicle.append(vehicle)
            vehicle.move()
        pygame.display.update()
