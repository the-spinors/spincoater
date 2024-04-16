import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean

# Bound voltage for if-condition below to find the period.
# Voltage satisfies if-condition if itself is below bound
# and its following voltage is above bound.
# Bound must be selected so as to be satisfied only once per cycle.
bound = 0.17

# Cooler graphs
params = {
	'font.family': "Times New Roman",
	'font.size': 19
}
plt.rcParams.update(params)


# Imports
filename = "linear_accel_TEK7.csv"
df = pd.read_csv(f"./Datos/Cleaned/{filename}")

seconds = df["seconds"]
voltages = df["voltage"]


# We pick a list of seconds whose voltages satisfy the if-condition.
# As the if-condition is satisfied once per cycle, we'll be able to determine
# the period by finding the diferences between these times.
bound_voltage_seconds = []
for s, v, v_next in zip(seconds, voltages, voltages[1:]):
	if v < bound and v_next > bound:
		bound_voltage_seconds.append(s)

# We take the average of the time differences between two pairs of points centered at our current time.
periods = [mean([bound_voltage_seconds[i] - bound_voltage_seconds[i - 1], bound_voltage_seconds[i + 1] - bound_voltage_seconds[i]]) for i in range(1, len(bound_voltage_seconds) - 1)]


# Graphs
fig, axs = plt.subplots(3)

fig.suptitle("Periodos y RPM con bipromedio")

axs[0].scatter(seconds, voltages, color = "b")
axs[0].set(ylabel = "Voltaje (V)", yticks = [0, bound, max(voltages)], title = "Voltage vs Tiempo")

axs[1].scatter(bound_voltage_seconds[1:-1], periods, color = "red")
axs[1].set(ylabel = "Delta (s)", title = "Periodos")

rpm = [60 / delta for delta in periods]
axs[2].scatter(bound_voltage_seconds[1:-1], rpm, color = "g")
axs[2].set(xlabel = "Segundos (s)", ylabel = "Velocidad angular (RPM)", title = "Velocidad angular")

offset = 0.2
xlim = (min(bound_voltage_seconds) - offset, max(bound_voltage_seconds) + offset)
axs[0].set(xlim = xlim, ylim = (-0.1, max(voltages) + offset))
axs[1].set(xlim = xlim)
axs[2].set(xlim = xlim)
		
for ax in axs:
	ax.grid(True, linestyle = "--")

fig.subplots_adjust(hspace = 0.5)
plt.show()


# Export
# with open(f"./Datos salida/biavg_{filename}_output.csv", "w") as f:
# 	f.write("Tiempo,periodo,rpm\n")
# 	for t, T, RPM in zip(bound_voltage_seconds, periods, rpm):
# 		f.write(f"{t},{T},{RPM}\n")