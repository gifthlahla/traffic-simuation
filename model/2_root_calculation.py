import numpy as np
import matplotlib.pyplot as plt

# Define constants and initial variables

# Constant related to traffic flow
C = 75000
# Initial value for traffic flow
Q0 = 220
# Tolerance for convergence
tolerance = 1e-6
# Maximum number of iterations
max_iter = 100
iteration = 0
Q = Q0


while True:
    # Calculate the next value of Q using the Newton-Raphson formula
    Q_next = Q - (Q**2 - C) / (2*Q)
    # If the difference between Q_next and Q is less than tolerance, end loop
    if abs(Q_next - Q) < tolerance:
        break
    # Update Q value
    Q = Q_next
    # Increment iteration counter
    iteration = iteration + 1
    # If maximum iterations exceeded, end loop
    if iteration > max_iter:
        print('Maximum number of iterations exceeded')
        break

# Print found root and iteration count
print('Found root:', Q)
print('Number of iterations:', iteration)

# Define function f(Q)
f = lambda Q: Q**2 - C

# Generate a set of Q values for plotting
Q_vals = np.linspace(0, 300, 400)
# Plot f(Q) vs Q
plt.plot(Q_vals, f(Q_vals))
# Mark found root on plot
plt.plot(Q, f(Q), 'ro')
# Label axes and plot title
plt.xlabel('traffic flow (Q)')
plt.ylabel('f(Q)')
plt.title('Newton-Raphson Method for vehicle traffic calculation')
# Enable plot grid
plt.grid(True)
# Show plot
plt.show()