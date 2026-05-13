import numpy as np
import matplotlib.pyplot as plt

# Data: time of day and vehicle traffic
horas_dia = np.array([6, 7, 8, 9, 10, 11, 12])
trafico = np.array([100, 150, 200, 250, 300, 350, 400])

# linear regression model
coeficientes = np.polyfit(horas_dia, trafico, 1)

# predictions
horas_prediccion = np.linspace(6, 12, 100)
trafico_predicho = np.polyval(coeficientes, horas_prediccion)

# Plot
plt.figure()
plt.plot(horas_dia, trafico, 'o', markersize=10)
plt.plot(horas_prediccion, trafico_predicho, '-r', linewidth=2)  # Plot regression line
plt.xlabel('time of day')
plt.ylabel('Vehicle traffic')
plt.title('Linear regression of vehicle traffic')
plt.legend(['Data', 'Regression line'], loc='upper right')
plt.grid(True)

# Interpretation of results
print('Linear regression model coefficients: ')
print(f'Slope (coefficient 1): {coeficientes[0]}')
print(f'Intercept (coefficient 2): {coeficientes[1]}')

plt.show()