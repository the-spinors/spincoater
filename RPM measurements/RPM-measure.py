import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("./Datos/linear_accel7.csv")

seconds = df["seconds"]
voltage = df["voltage"]

fig, axs = plt.subplots(2, sharex = True)

non_zero_seconds = []
for s, v, v_next in zip(seconds, voltage, voltage[1:]):
	if v > 0.2 and v_next < 0.2:
		non_zero_seconds.append(s)

non_zero_deltas = [non_zero_seconds[i] - non_zero_seconds[i - 1] for i in range(1, len(non_zero_seconds))]

axs[0].scatter(seconds, voltage, s = 5, color = "b", label = "Raw data")
# ax.scatter(seconds[:-1], delta_t, s = 2)
axs[0].scatter(non_zero_seconds[:-1], non_zero_deltas, color = "red", label = "Time deltas")
axs[0].set(ylabel = "Delta (s)")
axs[1].set(xlabel = "Segundos (s)", ylabel = "Velocidad angular (RPM)")


rpm = [60 / delta for delta in non_zero_deltas]
axs[1].scatter(non_zero_seconds[:-1], rpm, color = "g", label = "RPM")

axs[0].set(xlim = (0, 10), ylim = (0.01, 0.05))

plt.legend()
plt.grid(True)
plt.show()
