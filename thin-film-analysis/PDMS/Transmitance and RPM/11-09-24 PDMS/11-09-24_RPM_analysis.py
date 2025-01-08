import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def main():
    sys.path.insert(0, '../../../Analyzers')
    import RPM_analyzer as Ra
    
    # Get data
    RPM = []
    RPM_std = []
    rpm_directory = "./RPM/"
    listdir = os.listdir(rpm_directory)
    listdir = [rpm_directory + filename for filename in listdir]
    listdir = sorted(listdir, key = Ra.extract_integer)
    listdir = [filename for filename in listdir if '-s' not in filename]

    # Default voltage_bounds which can be modified for each file.
    voltage_bounds = [0.1 for _ in range(len(listdir))]

    for i, x in enumerate(zip(listdir, voltage_bounds)):
        s, V = Ra.extract_seconds_voltages(x[0])
        t , T = Ra.period_calculation(s, V, x[1])
        rpm =  60 / T
        RPM.append(np.mean(rpm))
        RPM_std.append(np.std(rpm) / np.sqrt(len(rpm)))
        
        # Ra.graph(s, V, t, T, x[1], f'{x[0]} - Index: {i}')

    # New DF
    df_filename = '../../Thickness vs RPM/Data/PDMS_thickness_RPM_11-09-24.CSV'
    Ra.export_df(RPM, RPM_std, listdir, df_filename, show = True)


if __name__ == '__main__':
    main()