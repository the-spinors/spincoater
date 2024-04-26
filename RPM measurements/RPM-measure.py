import matplotlib.pyplot as plt
import pandas as pd

filename = "5V_1000RPMs.csv"
df = pd.read_csv(f"./Datos/Cleaned/{filename}")

seconds = df["seconds"]
voltage = df["voltage"]

non_zero_seconds = []
for s, v, v_next in zip(seconds, voltage, voltage[1:]):
	if v > 0.2 and v_next < 0.2:
		non_zero_seconds.append(s)

non_zero_deltas = [non_zero_seconds[i] - non_zero_seconds[i - 1] for i in range(1, len(non_zero_seconds))]


fig, axs = plt.subplots(2, sharex = True)

axs[0].scatter(seconds, voltage, s = 5, color = "b", label = "Raw data")
# ax.scatter(seconds[:-1], delta_t, s = 2)
axs[0].scatter(non_zero_seconds[:-1], non_zero_deltas, color = "red", label = "Time deltas")
axs[0].set(ylabel = "Delta (s)")
axs[1].set(xlabel = "Segundos (s)", ylabel = "Velocidad angular (RPM)")

rpm = [60 / delta for delta in non_zero_deltas]
axs[1].scatter(non_zero_seconds[:-1], rpm, color = "g", label = "RPM")

axs[0].set(xlim = (0, 5), ylim = (0.01, 0.05))


with open("./to_excel.csv", "w") as f:
	f.write("second, t_delta, rpm\n")
	for n, m, r in zip(non_zero_seconds, non_zero_deltas, rpm):
		f.write(f"{n}, {m}, {r}\n")
		

plt.legend()
plt.grid(True)
plt.show()
