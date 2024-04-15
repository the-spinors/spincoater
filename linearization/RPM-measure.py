import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("./Datos/constant_vel6.csv")

seconds = df["seconds"]
voltage = df["voltage"]

fig, ax = plt.subplots()

non_zero_seconds = []
for s, v, v_next in zip(seconds, voltage, voltage[1:]):
	if v > 0.2 and v_next < 0.2:
		non_zero_seconds.append(s)

non_zero_deltas = [non_zero_seconds[i] - non_zero_seconds[i - 1] for i in range(1, len(non_zero_seconds))]

ax.scatter(seconds, voltage, s = 5, color = "b", label = "Raw data")
# ax.scatter(seconds[:-1], delta_t, s = 2)
ax.scatter(non_zero_seconds[:-1], non_zero_deltas, color = "red", label = "Time deltas")
ax.set(xlabel = "Segundos (s)", ylabel = "Delta (V)")


print(60 / non_zero_deltas[1])

plt.legend()
plt.grid(True)
plt.show()
