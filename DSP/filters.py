import numpy as np
######################      WINDOW FUNCTIONS      #######################################

def rectangular_window(n, N):
    """ Return tuple of (WindowFunction, N) """
    return 1

def get_rectangular_window_n(delta_f):
    return round(0.9 / delta_f)


def hanning_window(n, N):
    """ Return tuple of (WindowFunction, N) """
    return 0.5 + (0.5 * np.cos((2 * np.pi * n) / N))

def get_hanning_window_n(delta_f):
    return round(3.1 / delta_f)


def hamming_window(n, N):
    return 0.54 + (0.46 * np.cos((2 * np.pi * n) / N))

def get_hamming_window_n(delta_f):
    return round(3.3 / delta_f)


def blackman_window(n, N):
    return 0.42 + (0.5 * np.cos((2 * np.pi * n) / (N-1))) + (0.08 * np.cos((4 * np.pi * n) / (N-1)))

def get_blackman_window_n(delta_f):
    return round(5.5 / delta_f)

######################      FILTER FUNCTIONS      #######################################


def __lowpass_filter__(n, fc):
    if n == 0:
        return 2*fc

    n_omega = n * 2 * np.pi * fc

    return 2*fc * (np.sin(n_omega) / n_omega)   


def __highpass_filter__(n, fc):
    if n == 0:
        return 1 - (2*fc)

    n_omega = n * 2 * np.pi * fc

    return -2*fc * (np.sin(n_omega) / n_omega)   


def __bandpass_filter__(n, f1, f2):
    if n == 0:
        return 2 * (f2 - f1)

    n_omega2 = n * 2*np.pi*f2
    n_omega1 = n * 2*np.pi*f1
    return 2 * f2 * (np.sin((n_omega2)) / n_omega2) - (2 * f1 * (np.sin(n_omega1) / n_omega1))


def __bandreject_filter__(n, f1, f2):
    if n == 0:
        return 1 - __bandpass_filter__(n, f1, f2)

    return -1 * __bandpass_filter__(n, f1, f2)
##########################################################################################


from enum import Enum


frequency_window_map = {
    21: (rectangular_window, get_rectangular_window_n),
    44: (hanning_window, get_hanning_window_n),
    53: (hamming_window, get_hamming_window_n),
    74: (blackman_window, get_blackman_window_n)
}


class FIR_FILTERS(Enum):
    Low = 0
    High = 1
    BandPass = 2
    BandReject = 3


def get_filter_function(filter_type=FIR_FILTERS.Low):
    if filter_type == FIR_FILTERS.Low:
        return __lowpass_filter__
    elif filter_type == FIR_FILTERS.High:
        return __highpass_filter__
    elif filter_type == FIR_FILTERS.BandPass:
        return __bandpass_filter__
    elif filter_type == FIR_FILTERS.BandReject:
        return __bandreject_filter__

def get_suitable_window(stop_attenuation):
    keys_arr = (frequency_window_map.keys())
    keys_arr = np.array([x for x in keys_arr])
    return frequency_window_map[keys_arr[np.abs(keys_arr - stop_attenuation).argmin()]]

def apply_filter(signal, sampling_frequency, stop_attenuation, transition_band, cutoff_frequency, filter_type=FIR_FILTERS.Low):

    window_function, filter_samples_function = get_suitable_window(stop_attenuation)
    print('My Window Function ' , window_function)

    filter_function = get_filter_function(filter_type)
    centered_frequency = 0
    if filter_type is FIR_FILTERS.Low:
        centered_frequency = cutoff_frequency + (transition_band / 2)
        centered_frequency = centered_frequency / sampling_frequency
    elif filter_type is FIR_FILTERS.High:
        centered_frequency = cutoff_frequency - (transition_band / 2)
        centered_frequency = centered_frequency / sampling_frequency

    normalized_transition_band = transition_band / sampling_frequency
    N = filter_samples_function(normalized_transition_band)
    
    if int(N)%2== 0:
        N = N+1
    # Filtering
    filter_origin = N //2
    filter_values = []
    for n in range(filter_origin+1):
        window = window_function(n, N)
        value = filter_function(n, centered_frequency)
        filter_values.append(value * window)

    filter_values = filter_values[:0:-1] + filter_values[::1]
    # Now we have final filter, let's convolve the signal 
    k1 = [i for i in range(N//2+1)]
    k1 = np.array(k1)
    rev = -1*k1
    final = np.concatenate((rev[:0:-1], k1))
    kernel = [(final[i], filter_values[i]) for i in range(N)]
    with open('filtered.ds','w') as f:
        f.write(str(len(kernel)) + '\n')
        for i in kernel:
            f.write('{0} {1}\n'.format(i[0], i[1]))
    print(kernel[:10])
    return kernel

def apply_band_filter(signal, sampling_frequency, stop_attenuation, transition_band, band1, band2, filter_type=FIR_FILTERS.BandPass):
    
    window_function, filter_samples_function = get_suitable_window(stop_attenuation)
    filter_function = get_filter_function(filter_type)
    
    centered_frequency_1 = 0
    centered_frequency_2 = 0
    if filter_type is FIR_FILTERS.BandPass:
        centered_frequency_1 = band1 + (transition_band / 2)
        centered_frequency_1 = centered_frequency_1 / sampling_frequency
   
        centered_frequency_2 = band2 - (transition_band / 2)
        centered_frequency_2 = centered_frequency_2 / sampling_frequency
    elif filter_type is FIR_FILTERS.BandReject:
        centered_frequency_1 = band1 - (transition_band / 2)
        centered_frequency_1 = centered_frequency_1 / sampling_frequency
   
        centered_frequency_2 = band2 + (transition_band / 2)
        centered_frequency_2 = centered_frequency_2 / sampling_frequency
    
    normalized_transition_band = transition_band / sampling_frequency
    N = filter_samples_function(normalized_transition_band)
    
    if int(N)%2== 0:
        N = N+1
    # Filtering
    filter_origin = N //2
    filter_values = []
    for n in range(filter_origin+1):
        window = window_function(n, N)
        value = filter_function(n, centered_frequency_1, centered_frequency_2)
        filter_values.append(value * window)

    filter_values = filter_values[:0:-1] + filter_values[::1]

    # Now we have final filter, let's convolve the signal 
    k1 = [i for i in range(N//2+1)]
    k1 = np.array(k1)
    rev = -1*k1
    final = np.concatenate((rev[:0:-1], k1))
    kernel = [(final[i], filter_values[i]) for i in range(N)]
    with open('filtered.ds','w') as f:
        f.write(str(len(kernel)) + '\n')
        for i in kernel:
            f.write('{0} {1}\n'.format(i[0], i[1]))
    return kernel