import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from spin_analyser import acceleration_calculation, period_calculation, extract_seconds_voltages

filenames = [f"datos/TEK00{n:02}.csv" for n in range(33, 46)]
maximum_seconds = [4.4, 3, 2.7, 1.9, 2, 0.77, 1.97, 10, 2.27, 1.745, 1.7, 1.3, 2.2]
expected_accels = ["1000", "1000", "1600", "2200", "2800", "3400", "4000", "4600", "4600", "5200", "5800", "6400", "7000"]

accelerations = np.array([])
y_intercepts = np.array([])
for file, ms, expected_accel in zip(filenames, maximum_seconds, expected_accels):
    filename = file
    bound = 0.05
    seconds, voltages = extract_seconds_voltages(filename)

    # Period and acceleration
    event_seconds, periods = period_calculation(seconds, voltages, bound)
    RPMs = 60 / periods
    a, y = acceleration_calculation(seconds, voltages, bound, ms)
    accelerations = np.append(accelerations, a)
    y_intercepts = np.append(y_intercepts, y)


    # # Graphs
    # filter_array = event_seconds < ms

    # marker_size = 8
    # fig, axs = plt.subplots(3)
    # fig.suptitle(f"{file}: Periodos y RPM con quadpromedio")

    # # Voltage vs Time
    # axs[0].scatter(seconds, voltages, color="b", s = marker_size)
    # axs[0].set(ylabel="Voltaje (V)", yticks=[
    #         0, bound, max(voltages)], title="Voltage vs Tiempo")

    # # Periods
    # axs[1].scatter(event_seconds[filter_array], periods[filter_array], color="red", s = marker_size)
    # axs[1].set(ylabel="Delta (s)", title="Periodos")

    # # RPMs
    # axs[2].scatter(event_seconds[filter_array], RPMs[filter_array], color="g", s = marker_size)
    # axs[2].set(xlabel="Segundos (s)", ylabel="Velocidad angular (RPM)",
    #         title=f"Velocidad angular (aceleración esperada: {expected_accel})")

    # # Plotting approximation for RPMs
    # t_space = np.linspace(min(event_seconds), max(event_seconds[2:-2]), 10)
    # axs[2].plot(t_space, a * t_space + y, color = "r", label = f"Aproximación: $a = {round(a, 2)}, v_0 = {round(y, 2)}$")
    # print(f"Acceleration: {a} RPM/s, y_intercept: {y}")


    # # x and y limits and grids
    # offset = 0.2
    # xlim = (min(event_seconds) - offset,
    #         max(event_seconds) + offset)
    # axs[0].set(xlim=xlim, ylim=(-0.1, max(voltages) + offset))
    # axs[1].set(xlim=xlim)
    # axs[2].set(xlim=xlim)

    # for ax in axs:
    #     ax.grid(True, linestyle="--")
    # axs[2].legend()
    # fig.subplots_adjust(hspace=0.75)

    # plt.show()
