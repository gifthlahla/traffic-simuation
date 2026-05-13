import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pygame
import time
import sys
from scipy.integrate import odeint, cumulative_trapezoid
from scipy.interpolate import interp1d


class Presentation_Result(object):
    def __init__(self, simulation_time: int):
        """
            Initializes the `Presentation_Result` class with the simulation time.

            Args:
                simulation_time (int): Simulation time in seconds
        """
        self.time = simulation_time
        self.figures = []  # List to store figures and axes
        self.vehicles: dict[str, dict[str, float]] = {
            "car": {
                "mass": 1.814,
                "damping": 50,
                "spring": 10.0,
                "position": 1,
                "velocity": 2.25,
            },
            "bus": {
                "mass": 9.071,
                "damping": 100,
                "spring": 20.0,
                "position": 1,
                "velocity": 1.8,
            },
            "truck": {
                "mass": 3.629,
                "damping": 150,
                "spring": 30.0,
                "position": 1,
                "velocity": 1.8,
            },
            "bike": {
                "mass": 250,
                "damping": 30,
                "spring": 5000,
                "position": 1,
                "velocity": 2.5,
            },
        }

    def show_all_plots(self):
        """
            Displays all figures in a single window.
        """
        # Calculate the necessary number of rows and columns
        num_plots = len(self.figures)
        # You can adjust this as needed
        num_cols = int(len(self.figures)/4)
        num_rows = num_plots // num_cols
        if num_plots % num_cols:
            num_rows += 1

        # Create a grid of subplots
        # Adjust figure size as needed
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(13, 8))

        # Add each figure to the grid
        for i, ax in enumerate(self.figures):
            # Calculate grid position
            row = i // num_cols
            col = i % num_cols

            # Add the figure to the grid
            for line in ax.lines:
                # Create a copy of the line
                line_copy = line.__class__(line.get_xdata(), line.get_ydata(), color=line.get_color(
                ), linestyle=line.get_linestyle(), linewidth=line.get_linewidth())
                axs[row, col].add_line(line_copy)
            for patch in ax.patches:
                # Create a copy of the patch
                patch_copy = matplotlib.patches.Rectangle((patch.get_x(), patch.get_y(
                )), patch.get_width(), patch.get_height(), fill=True, color=patch.get_facecolor())
                axs[row, col].add_patch(patch_copy)
            axs[row, col].set_xlabel(ax.get_xlabel(), fontsize=8)
            axs[row, col].set_ylabel(ax.get_ylabel(), fontsize=8)
            axs[row, col].set_title(ax.get_title(), fontsize=10)
            axs[row, col].relim()
            axs[row, col].autoscale_view()

            # # Reducir el tamaño de la fuente de los ejes
            # axs[row, col].tick_params(axis='both', which='major', labelsize=4)

        # Adjust layout so plots don't overlap
        plt.tight_layout()
        # Maximize figure window
        mng = plt.get_current_fig_manager()
        try:
            mng.window.state('zoomed') # TkAgg backend
        except Exception:
            try:
                mng.window.showMaximized() # Qt backend
            except Exception:
                fig.set_size_inches(16, 9) # Fallback
        plt.savefig('graphs/all_plots.png')
        # Show the figure with all plots
        plt.close(fig)
        # Initialize Pygame
        pygame.init()

        # Load saved image
        image = pygame.image.load('graphs/all_plots.png')

        # Create a window the size of the image
        screen = pygame.display.set_mode(
            (image.get_width(), image.get_height()))

        # Display image
        screen.blit(image, (0, 0))
        pygame.display.flip()

        # Keep window open until closed
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
        pygame.quit()

    def traffic_model(self, position_leader: float = 50, position_follower: float = 40, velocity_leader: float = 30, velocity_follower: float = 20):
        """
            The `model_trafic` function simulates the FVADM traffic model and plots the 
            follower vehicle speed versus time.

            Args:
                position_leader (float): Leader vehicle position
                position_follower (float): Follower vehicle position
                velocity_leader (float): Leader vehicle speed
                velocity_follower (float): Follower vehicle speed
        """

        # FVADM model parameters
        k = 0.1  # Parámetro k
        V1 = 10  # Parámetro V1
        V2 = 20  # Parámetro V2
        C1 = 10  # Parámetro C1
        C2 = 20  # Parámetro C2
        lambda_ = 0.5  # Parámetro lambda
        gamma = 0.1  # Parámetro gamma

        # Vehicle positions
        x_l = position_leader  # Leader vehicle position
        x = position_follower  # Follower vehicle position
        l = 25  # Distance between vehicles
        v_l = velocity_leader  # Leader vehicle speed
        v = velocity_follower  # Follower vehicle speed
        a = 1.5  # Vehicle acceleration

        # Function defining the FVADM differential equation
        def modelo_FVADM(v, _):
            return k * (V1 + V2 * np.tanh((C1 * (x_l - x - l)) / C2) - v) + lambda_ * (v_l - v) + gamma * a

        # Simulation time
        t = np.linspace(0, self.time, 1000)

        # Solving the differential equation
        solution = odeint(modelo_FVADM, v, t)
        # Create figure and axes
        #         ax = plt.Axes(fig=plt.figure(), rect=[0,0,1,1])

        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])
        # Plotting the solution
        ax.plot(t, solution)
        ax.set_xlabel('Time')
        ax.set_ylabel('Follower vehicle speed')
        ax.set_title(
            'Full Velocity \n and Acceleration Difference Model')
        self.figures.append(ax)

    def root_calculation(self, num_vehicles: int = 220):
        """
        The `calculo_raices` function calculates the root of the equation Q^2 - C = 0 
        using the Newton-Raphson method.

        Args:
            num_vehicles (int): Number of vehicles in traffic

        """
        # Constant related to traffic flow
        C = 75000
        # Initial value for traffic flow
        Q0 = num_vehicles
        # Tolerance for convergence
        tolerancia = 1e-6
        # Maximum number of iterations
        maxIter = 100
        iter = 0
        Q = Q0

        while True:
            # Calculate the next value of Q using the Newton-Raphson formula
            Qnext = Q - (Q**2 - C) / (2*Q)
            # If the difference between Qnext and Q is less than tolerance, end loop
            if abs(Qnext - Q) < tolerancia:
                break
            # Update Q value
            Q = Qnext
            # Increment iteration counter
            iter = iter + 1
            # If maximum iterations exceeded, end loop
            if iter > maxIter:
                print('Maximum number of iterations exceeded')
                break

        # Print found root and iteration count
        print('Found root:', Q)
        print('Iteration count:', iter)

        # Define function f(Q)
        def f(Q): return Q**2 - C

        # Generate a set of Q values for plotting
        Q_vals = np.linspace(0, self.time, 400)
        # Crear los ejes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])
        # Plot f(Q) vs Q
        ax.plot(Q_vals, f(Q_vals))
        # Mark found root on plot
        ax.plot(Q, f(Q), 'ro')
        # Label axes and plot title
        ax.set_xlabel('traffic flow (Q)')
        ax.set_ylabel('f(Q)')
        ax.set_title(
            'Newton-Raphson Method \n for vehicle traffic calculation')
        # Enable plot grid
        ax.grid(True)
        # Show plot
        self.figures.append(ax)

    def curve_fitting(self, num_vehicles: int = 220):
        """
        The `ajuste_curvas` function performs linear regression on traffic data and plots 
        the results.

        Args:
            num_vehicles (int): Number of vehicles in traffic
        """
        
        # Data: time of day and vehicle traffic
        horas_dia = np.linspace(0, self.time, 7)

        trafico = np.linspace(0, num_vehicles, 7)

        # linear regression model
        coeficientes = np.polyfit(horas_dia, trafico, 1)

        # predictions
        horas_prediccion = np.linspace(horas_dia[0], horas_dia[-1], 100)
        trafico_predicho = np.polyval(coeficientes, horas_prediccion)

        # Crear los ejes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])
        # Plot
        ax.plot(horas_dia, trafico, 'o', markersize=10)
        ax.plot(horas_prediccion, trafico_predicho, '-r',
                linewidth=2)  # Plot regression line
        ax.set_xlabel('time of day')
        ax.set_ylabel('Vehicle traffic')
        ax.set_title('Linear regression of vehicle traffic')
        ax.legend(['Data', 'Regression line'],
                  loc='upper right')
        ax.grid(True)

        self.figures.append(ax)

    def velocity_acceleration_derivative(self, speeds: list = [2.25, 1.8, 1.8, 2.5]):

        """
            The `derivada_velocidad_aceleracion` function calculates vehicle acceleration at a given time.

            Args:
                speeds (list): List of vehicle speeds    
        """
        # Time and speed data
        tiempo = np.linspace(0, self.time, 4)
        # from m/s to km/s
        velocidad = np.array([speed * 50 for speed in speeds])

        # Speed interpolation
        tiempo_interp = np.arange(0, tiempo[-1], 0.1)
        f = interp1d(tiempo, velocidad, kind='cubic')
        velocidad_interp = f(tiempo_interp)

        # Speed extrapolation
        tiempo_extrap = np.arange(0, velocidad[0], 0.1)
        f = interp1d(tiempo, velocidad, kind='cubic', fill_value="extrapolate")
        velocidad_extrap = f(tiempo_extrap)

        # Acceleration calculation as velocity derivative
        aceleracion_interp = np.diff(velocidad_interp) / np.diff(tiempo_interp)
        aceleracion_extrap = np.diff(velocidad_extrap) / np.diff(tiempo_extrap)

        # Crear la figura y los ejes
        fig, axs = plt.subplots(2, 1)

        # Plots
        axs[0].plot(tiempo, velocidad, 'o', tiempo_interp,
                    velocidad_interp, '-', tiempo_extrap, velocidad_extrap, '--')
        axs[0].set_title('Speed vs. Time')
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('Speed (m/s)')
        axs[0].legend(['Data', 'Interpolation', 'Extrapolation'])

        axs[1].plot(tiempo_interp[:-1], aceleracion_interp,
                    '-', tiempo_extrap[:-1], aceleracion_extrap, '--')
        axs[1].set_title('Acceleration vs. Time')
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel('Acceleration (m/s^2)')
        axs[1].legend(['Interpolation', 'Extrapolation'])

        fig.tight_layout()
        # Aplanar axs y agregar cada objeto AxesSubplot a self.figures
        for ax in np.ravel(axs):
            self.figures.append(ax)

    def integral_accumulation(self, vehicleClass: str = "car"):
        """
            The `Acumulacion_integrales` function simulates displacement and velocity of two vehicles at a given time.

            Args:
                vehicleClass (str): Vehicle class to simulate
        """
        # Time range
        t = np.arange(0, self.time, 0.1)

        vehicle_velocity = self.vehicles[vehicleClass]["velocity"]
        # Velocity of vehicles A and B
        v_A = vehicle_velocity*t
        v_B = vehicle_velocity*t + 4

        # Displacement using numerical integration
        s_A = cumulative_trapezoid(v_A, t, initial=0)
        s_B = cumulative_trapezoid(v_B, t, initial=0)
        # Create figure and axes
        fig, axs = plt.subplots(2, 1)

        # Plot Velocity vs. Time
        axs[0].plot(t, v_A, 'b-', t, v_B, 'r--')
        axs[0].legend(['Velocity A', 'Velocity B'])
        axs[0].set_title('Velocity vs. Time')
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('Velocity (m/s)')

        # Plot Displacement vs. Time
        axs[1].plot(t, s_A, 'b-', t, s_B, 'r--')

        axs[1].legend(['Displacement A', 'Displacement B'])
        axs[1].set_title('Displacement vs. Time')
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel('Displacement (m)')

        fig.tight_layout()
        # Flatten axs and add each AxesSubplot object to self.figures
        for ax in np.ravel(axs):
            self.figures.append(ax)

    def trajectory_plotting(self, vehicle1: tuple[float, float, float] = (0, 0, 3), vehicle2: tuple[float, float, float] = (0, 0, 1.5)):
        """
            The `Trazado_trayectorias` function simulates the trajectory of two vehicles at a given time.

            Args:
                vehicle1 (tuple): Position, speed, and acceleration of vehicle 1
                vehicle2 (tuple): Position, speed, and acceleration of vehicle 2
        """

        final_time = self.time  # seconds
        dt = 0.1
        # initial conditions for vehicle 1
        position1, velocity1, acceleration1 = vehicle1

        # initial conditions for vehicle 2
        position2, velocity2, acceleration2 = vehicle2
        # Create figure and axes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])

        # Figure preparation for simulation

        ax.grid(True)
        ax.set_xlabel('time (s)')
        ax.set_ylabel('Position (m)')

        # Lists to store positions and times
        times = []
        positions1 = []
        positions2 = []

        # for simulation
        for t in np.arange(0, final_time+dt, dt):
            # Update Positions and Velocities
            position1 = position1 + velocity1 * dt
            velocity1 = velocity1 + acceleration1 * dt

            position2 = position2 + velocity2 * dt
            velocity2 = velocity2 + acceleration2 * dt

            # Store times and positions
            times.append(t)
            positions1.append(position1)
            positions2.append(position2)

        # Plot
        ax.plot(times, positions1, 'r-')
        ax.plot(times, positions2, 'b-')

        ax.set_title('Trajectory of two vehicles')
        ax.legend(['Vehicle 1', 'Vehicle 2'])
        self.figures.append(ax)

    def trapezoid(self, vehicle_class: str = "car"):
        """
            The `Trapecio` function calculates displacement and total distance traveled by a vehicle at a given time.

            Args:
                vehicle_class (str): Vehicle class to simulate
        """
        # Define time from 0 to 300 seconds
        t = np.arange(0, self.time, 0.1)

        # Vehicle speed
        velocity_vehicle = self.vehicles[vehicle_class]["velocity"]

        # Define velocity function in m/s
        v = velocity_vehicle*t - 2

        # Displacement
        displacement = np.trapezoid(v, t) / 1000  # km

        # Absolute speed
        v_abs = np.abs(v)

        # Total distance
        total_distance = np.trapezoid(v_abs, t) / 1000  # km

        # Create bar chart
        labels = ['Displacement', 'Total Distance Traveled']
        values = [displacement, total_distance]
        # Create figure and axes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])

        ax.bar(labels, values)
        ax.set_ylabel('Kilometers')
        ax.set_title('Displacement and Total Distance Traveled')
        self.figures.append(ax)

    def mass_damper(self, vehicleClass: str = "car"):
        """
            The `Masa_amortiguador` function simulates the behavior of a mass-spring-damper system.

            Args:
                vehicleClass (str): Vehicle class to simulate
        """

        mass = self.vehicles[vehicleClass]["mass"]
        damping = self.vehicles[vehicleClass]["damping"]
        spring = self.vehicles[vehicleClass]["spring"]
        position = self.vehicles[vehicleClass]["position"]
        velocity = self.vehicles[vehicleClass]["velocity"]
        # system parameters
        m = mass  # mass (kg)
        b = damping  # damping coefficient (Ns/m)
        k = spring  # spring constant (N/m)

        # Initial Conditions
        x0 = position  # initial position
        v0 = velocity  # Initial velocity (m/s)

        # Simulation Time
        t = np.linspace(0, self.time, 1000)  # from t=0 to t=10

        # Definition of motion equations
        def ode(y, t, b, k, m):
            x, v = y
            dydt = [v, -(b/m) * v + -(k/m) * x]
            return dydt

        # Solving motion equations
        y0 = [x0, v0]
        sol = odeint(ode, y0, t, args=(b, k, m))
        # Create figure and axes
        fig, axs = plt.subplots(2, 1)

        # Visualization of position vs time
        axs[0].plot(t, sol[:, 0], 'b', linewidth=2)
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('Position (m)')
        axs[0].set_title(
            "Position vs Time of the \n Mass-Spring-Damper System")

        # Visualization of velocity vs time
        axs[1].plot(t, sol[:, 1], 'b', linewidth=2)
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel('Velocity (m/s)')
        axs[1].set_title(
            "Velocity vs Time of the \n Mass-Spring-Damper System")

        fig.tight_layout()
        # Flatten axs and add each AxesSubplot object to self.figures
        for ax in np.ravel(axs):
            self.figures.append(ax)

    def mass_damper_analogy(self, vehicleClass: str = "car"):
        """
            The `analogia_masa_amortiguador` function simulates vehicle behavior following the mass-damper analogy.

            Args:
                vehicleClass (str): Vehicle class to simulate
        """
        mass = self.vehicles[vehicleClass]["mass"]
        damping = self.vehicles[vehicleClass]["damping"]
        spring = self.vehicles[vehicleClass]["spring"]
        position = self.vehicles[vehicleClass]["position"]
        velocity = self.vehicles[vehicleClass]["velocity"]
        # System parameters
        m = mass  # mass (kg)
        c = damping  # damping coefficient (Ns/m)
        k = spring  # spring constant (N/m)

        # Initial conditions
        x0 = position  # initial position
        v0 = velocity  # initial velocity (m/s)

        # Definition of motion equations
        def vehicle_dynamics(x, t, m, c, k):
            dxdt = np.zeros(2)
            dxdt[0] = x[1]

            leader_speed = 20 + 5*np.sin(0.5*t)
            dxdt[1] = (-c*x[1] - k*(x[0] - leader_speed)) / m

            return dxdt

        # Solving motion equations
        y0 = [x0, v0]
        t = np.linspace(0, self.time, 1000)
        sol = odeint(vehicle_dynamics, y0, t, args=(
            m, c, k), atol=1e-9, rtol=1e-6)
        # Create figure and axes
        fig = plt.figure()
        
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

        fig.tight_layout()
        # Flatten axs and add each AxesSubplot object to self.figures
        for ax in fig.axes:
            self.figures.append(ax)

    def simple_queue_theories(self, num_vehicles: int = 10):
        """
            The `Teorias_colas_simples` function calculates the probability distribution of the number of vehicles 
            in a single-server queuing system.
            
            Args:
                num_vehicles (int): Number of vehicles in the system
        """
        # System parameters
        _lambda = 4  # Vehicle arrival rate
        mu = 5  # Service rate
        k = num_vehicles  # Maximum number of vehicles in the system

        # Probability that the system is in state i
        pi = np.zeros(k+1)
        pi[0] = 1
        for i in range(1, k+1):
            pi[i] = (_lambda/mu)**i * pi[0]
        pi[0] = 1 / np.sum(pi)

        # Average number of vehicles in the system
        L = np.sum(pi * np.arange(0, k+1))

        # Probability that an arriving vehicle has to wait
        P_wait = 1 - pi[0]
        # Create figure and axes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])

        # Plot of probability distribution

        ax.bar(np.arange(0, k+1), pi)
        ax.set_xlabel('Number of vehicles in the system')
        ax.set_ylabel('Probability')
        ax.set_title(
            'Probability distribution \n of the number of vehicles in the system')
        self.figures.append(ax)

        # Print statistics
        print(f'Average number of vehicles in the system: {L:.2f}')
        print(
            f'Probability that an arriving vehicle has to wait: {P_wait:.2f}')

    def multiple_queue_theories(self, num_vehicles: int = 10):
        """
            The `Teorias_colas_multiples` function calculates the probability distribution of the number of vehicles 
            in a multi-server queuing system.
            
            Args:
                num_vehicles (int): Number of vehicles in the system
        """
        # System parameters
        _lambda = 6  # Vehicle arrival rate
        mu = 5  # Service rate
        c = 4  # Number of servers
        K = num_vehicles  # Maximum number of vehicles in the system

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
        # Create figure and axes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])

        # Plot of probability distribution

        ax.bar(np.arange(0, K+1), pi)
        ax.set_xlabel('Number of vehicles in the system')
        ax.set_ylabel('Probability')
        ax.set_title(
            'Probability distribution \n of the number of vehicles in the system')
        self.figures.append(ax)

        # Print statistics
        print(f'Average number of vehicles in the system: {L:.2f}')
        print(
            f'Probability that an arriving vehicle has to wait: {P_wait:.2f}')

    def bulawayo(self, simulations: int = 1000):
        """
            The `bulawayo` function simulates a queuing system and calculates the average waiting 
            time distribution based on specific parameters.

            Args:
                simulations (int): Number of simulations to perform
        """
        # Parameters
        lambda_ = 2  # average time between arrivals, in minutes
        mu = 1  # average service time, in minutes
        sigma = 0.5  # standard deviation of service time in minutes
        N = simulations  # number of simulations

        waiting_time = np.zeros(N)

        for i in range(N):
            arrivals = np.cumsum(np.random.exponential(
                lambda_, 100))  # 100 vehicles
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
        # Create figure and axes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])

        # Plot of waiting times
        ax.hist(waiting_time, bins=20)
        ax.set_xlabel('Average Waiting Time (Minutes)')
        ax.set_ylabel('Frequency')
        ax.set_title(
            'Distribution of average \n waiting time in interaction')
        self.figures.append(ax)


    def exec_all_plots(self, simulation_vehicle: list, leader: int, follower: int, speeds: dict, type_vehicle: str, simulationTime: int):
        """
        Executes all plots

        Args:
            simulation_vehicle (list): List of vehicles in the simulation
            leader (int): Leader vehicle index
            follower (int): Follower vehicle index
            speeds (dict): Vehicle speeds
            type_vehicle (str): Vehicle type
            simulationTime (int): Simulation time
            
        """
        vehicle_leader = simulation_vehicle[leader]
        vehicle_follower = simulation_vehicle[follower]
        time_execution = time.time()
        self.traffic_model(
            position_leader=vehicle_leader.x,
            position_follower=vehicle_follower.x,
            velocity_leader=vehicle_leader.speed,
            velocity_follower=vehicle_follower.speed
        )
        self.curve_fitting(num_vehicles=220)
        self.root_calculation(num_vehicles=220)
        self.velocity_acceleration_derivative(speeds=list(speeds.values()))
        self.integral_accumulation(vehicleClass=type_vehicle)
        self.trajectory_plotting(
            vehicle1=(vehicle_leader.x, vehicle_leader.speed, 1.5),
            vehicle2=(vehicle_follower.x, vehicle_follower.speed, 3)
        )
        self.trapezoid(vehicle_class=type_vehicle)
        self.mass_damper(vehicleClass=type_vehicle)
        self.mass_damper_analogy(vehicleClass=type_vehicle)
        self.simple_queue_theories(num_vehicles=220)
        self.multiple_queue_theories(num_vehicles=220)
        self.bulawayo(simulations=simulationTime)
        print(f"Execution time: {time.time() - time_execution} seconds")
        self.show_all_plots()


# if __name__ == '__main__':
#     modulo = Presentation_Result(300)
#     modulo.exec_all_plots()
#     modulo.show_all_plots()
