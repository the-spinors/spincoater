import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp
import numpy as np
import scienceplots

# cooler graphs but you can't ñ
plt.style.use(["science", "no-latex"])


# Import data
df = pd.read_csv("acceleration_actual.csv")
a_n = df["gaved"]
a_r = df["actual"]

# Curve fit
fit_function = lambda x, m, b: m * x + b
fit_parameters, parameter_covariance = sp.optimize.curve_fit(
    fit_function, a_n, a_r)
print(parameter_covariance)
print(f"Pendiente: {fit_parameters[0]}, Intercept: {fit_parameters[1]}")


# Graphs
x = np.linspace(min(a_n), max(a_n), 10)
plt.scatter(a_n, a_r)
# plt.scatter(a_n, a_r - a_n)
plt.text(4000, 4000,
         f"$a_{{registrada}} = {round(fit_parameters[0], 3)}a_{{nominal}} + {round(fit_parameters[1], 3)}$")
plt.plot(x, fit_function(x, *fit_parameters))

# Labels
plt.title("Aceleraciones sin corregir")
plt.xlabel("Aceleracion nominal (RPM/s)")
plt.ylabel(ylabel="Aceleraciones obtenidas (RPM/s)")

# Ticks and grid
ticks = [x for x in range(1000, 5500, 500)]
plt.xticks(ticks)
plt.yticks(ticks)
plt.grid(True)
plt.show()
