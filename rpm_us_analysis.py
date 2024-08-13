from spin_analyser import extract_seconds_voltages, period_calculation
import matplotlib.pyplot as plt
import numpy as np

# Monitor 1 - RPM measurements, Monitor 2 - Filter points4
# filenames1 is data from monitor 1, filanames2 from monitor 2
filenames1 = [f"datos/TEK00{n:02}.csv" for n in range(55, 56)]
filenames2 = [f"datos/TEK00{n:02}.csv" for n in range(56, 57)]
microseconds = [20, 30, 98, 2938, 2]

# Extract data5
for filename1, filename2 in zip(filenames1, filenames2):
    seconds1, voltages1 = extract_seconds_voltages(filename1)
    seconds2, voltages2 = extract_seconds_voltages(filename2)
    voltages2 = voltages2 / 2582


# Get indices where oscilloscope's second monitor voltage jumps occur.
# jump_seconds, jump_voltages are the seconds, voltages at which these
# same jumps occur.
# voltage2_bound must be selected so that voltages below this bound
# correspond to the arduino pin being LOW, and above this bound being HIGH.
voltage2_bound = 1
indices = np.array([i for i in range(len(seconds2))])
jump_indices = np.array([], dtype = int)
jump_seconds = np.array([])
jump_voltages = np.array([])
for n, s2, v2, v2next in zip(indices[:-1], seconds2[:-1], voltages2[:-1], voltages2[1:]):
    if (v2 < voltage2_bound and v2next > voltage2_bound) or (v2 > voltage2_bound and v2next < voltage_bound):
        jump_indices = np.append(jump_indices, int(n))
        jump_seconds = np.append(jump_seconds, s2)
        jump_voltages = np.append(jump_voltages, v2)

# Split monitor 1 data points
matrix_seconds = np.split(seconds1, jump_indices)[::2]
matrix_voltages = np.split(voltages1, jump_indices)[::2]

# Get RPM mean for each of the splitted groups
bound = 0.025
RPMs_means = np.array([])
for seconds, voltages, us in zip(matrix_seconds, matrix_voltages, microseconds):
    event_seconds, periods = period_calculation(seconds, voltages, bound)
    RPMs = 60 / periods
    RPMs_mean = np.mean(RPMs)
    RPMs_means = np.append(RPMs_means, RPMs_mean)

    plt.plot(event_seconds, RPMs)
    plt.title(f"writeMicroseconds: {us}")
    plt.axhline(RPMs_mean, color = "r", label = f"Mean: {RPMs_mean}")
    plt.legend()
    plt.show()

print(RPMs_means)
0
# Visualization of array separation
filter_array = voltages2 < voltage2_bound
voltages1[filter_array] = -2
marker_size = 8
plt.scatter(seconds1, voltages1, label = "data", s = marker_size)
plt.scatter(seconds2, voltages2, color = "r", label = "filter", s = marker_size)
plt.scatter(jump_seconds, jump_voltages, color = "k", label = "filter")
plt.legend()
plt.show()