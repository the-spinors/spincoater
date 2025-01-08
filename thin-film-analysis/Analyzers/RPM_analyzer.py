import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract_seconds_voltages(filename):
    df = pd.read_csv(filename)
    return (df.iloc[:, 3], df.iloc[:, 4])


def period_calculation(seconds, voltages, bound):
    '''
    Calculates period of motor from voltage and the time of given period.
    bound: bound voltage for event (see below)
    match_lengths: makes times-of-period array match length of periods array.
    '''
    # In order to calculate the period we need to find an event that only
    # happens once per cycle and at regular intervals.
    # We'll consider a bound voltage value. We suppose that there's only
    # one data point per cycle that satisfies being below this bound voltage
    # and whose next data point is above this bound voltage.
    # This is our "event" which in real life may correspond to
    # the laser inciding on the black tape to inciding on the reflecting surface.
    # Period calculation will be done considering this event so
    # bound (voltage) must be selected so as to .only be satisfied once per cycle.

    # We pick a list of seconds whose voltages satisfy the event.
    # As the event is satisfied once per cycle, we'll be able to determine   
    # the period by finding the diferences between these times.
    event_seconds = np.array([])
    for s, v, v_next in zip(seconds, voltages, voltages[1:]):
        if v <= bound and v_next > bound:
            event_seconds = np.append(event_seconds, s)

    periods = np.array([event_seconds[i] - event_seconds[i - 1] for i in range(1, len(event_seconds))])
    return event_seconds, periods


def extract_integer(filename):
    return float(filename.split(' ')[-1][:-4])


def graph(s, V, t, T, voltage_bound, title):
    # Format
    rc_update = {'font.size': 18, 'font.family': 'serif', 'font.serif': ['Times New Roman', 'FreeSerif']}
    plt.rcParams.update(rc_update)

    # Plots
    fig, axs = plt.subplots(2)
    axs[0].plot(s, V, label = "Voltage", color = 'Red')
    axs[0].axhline(voltage_bound, label = "Voltage bound")
    axs[1].plot(t[:-1], T, label = "Periods")
    
    # Titles
    axs[0].set_title('Voltage vs Time')
    axs[0].set(xlabel = "Time (s)", ylabel = "Voltage (V)")
    axs[1].set_title('Periods vs Time')
    axs[1].set(xlabel = "Time (s)", ylabel = "Period (s)")

    # Format
    for ax in axs:
        ax.grid(color = '#999', linestyle = '--')
        ax.legend(loc = 1, fontsize = 10)

    # Display on fullscreen
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    fig.suptitle(title)
    plt.subplots_adjust(hspace = 0.5)
    plt.show()


def export_df(RPM, RPM_std, listdir, df_filename, show = True):
        short_filenames = [filename.split('/')[-1] for filename in listdir]
        pdms_nums = [int(np.floor(extract_integer(filename))) for filename in listdir]
        RPM_df = pd.DataFrame({'RPM_filename': short_filenames, 'PDMS #': pdms_nums,
                           'RPM': RPM, 'RPM_std': RPM_std})
        RPM_df.to_csv(f'./{df_filename}')

        if show:
            pd.set_option('display.max_rows', None, 'display.max_columns', None,
                          'display.width', 1000)
            print(RPM_df)


def main():
    pass


if __name__ == "__main__":
    main()
