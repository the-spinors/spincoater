import numpy as np
import scipy as sp
import pandas as pd


def extract_seconds_voltages(filename):
    df = pd.read_csv(filename)
    return (df.iloc[:, 3], df.iloc[:, 4])


def period_calculation(seconds, voltages, bound, match_lengths = True):
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
        if v < bound and v_next > bound:
            event_seconds = np.append(event_seconds, s)

    # We take the average of the time differences between four pairs of points centered at our current time.
    periods = np.array([np.mean([event_seconds[i - 1] - event_seconds[i - 2], event_seconds[i] - event_seconds[i - 1], event_seconds[i + 1] - event_seconds[i], event_seconds[i + 2] - event_seconds[i + 1]]) for i in range(2, len(event_seconds) - 2)])
    
    if match_lengths:
        return event_seconds[2:-2], periods
    return event_seconds, periods


def acceleration_calculation(seconds, voltages, bound, maximum_seconds):
    event_seconds, periods = period_calculation(seconds, voltages, bound)
    RPMs = 60 / periods

    filter_array = event_seconds < maximum_seconds
    RPMs = RPMs[filter_array]
    event_seconds = event_seconds[filter_array]

    # Linear approximation for RPM per second
    # a: slope, acceleration; y: y-intercept, initial speed
    linear_fit = lambda t, a, y: a * t + y
    a, y = sp.optimize.curve_fit(linear_fit, event_seconds, RPMs)[0]
    return a, y


def main():
    filename = "datos/TEK0026.CSV"
    seconds, voltage = extract_seconds_voltages(filename)
    print(seconds, voltage)


if __name__ == "__main__":
    main()