import numpy as np
from DSP.fft import apply_fft 

def add_signals(first,second):
    """
    new = first + second

    signal_format -> [(x1,y1)...(xn,yn)]
    """
    signals = [] #Append all signals in one big list of signals
    signals.append(first)
    signals.append(second)

    combined_signals = combine(signals) #Append all x,y values in one big compound signal
 
    combined_signals.sort() #Sort depending on X

    final_result = []
    temp = list(combined_signals)
    for i in range(len(combined_signals) - 1):
        s1 = combined_signals[i]
        s2 = combined_signals[i+1]
        if s1[0] == s2[0]:
            final_result.append((s1[0], s1[1]+s2[1]))
            temp.remove(s1)
            temp.remove(s2)

    final_result.extend(temp)
    final_result.sort()
    return final_result

def subtract_signals(first, second):
    """
    new = first + second
    
    signal_format -> [(x1,y1)...(xn,yn)]
    """
    n_signal = multiply_signal(second, -1)
    return add_signals(first, n_signal)

def multiply_signal(first, constant):
    """
    newPoint = (oldx, oldy * constant)
    
    first -> [(x1,y1)...(xn,yn)]
    """
    final_result = [(x[0], x[1] * constant) for x in first]
    return final_result

def combine(signals):
    """
    return a combined signal consists of all sub signals in the signals list

    signals -> [s1, s2,s3]
    
    s1-> [(x1,y1)...(xn,yn)]
    """
    combined_signals = [] #Append all x,y values in one big compound signal
    for i in range(len(signals)):
        for s in signals[i]:
            combined_signals.append(s)
    return combined_signals

def quantize_signal(signal, n, use_bit_mode = False):
    """
    Quantize a signal in n levels or 2^n levels if using bit mode

    return tuple of (Quantized Signal, Enconding Values, Mean Squared Error)
    """
    signalValues = [x[1]
                    for x in signal]
    signalTime = [x[0]
                    for x in signal]
    quantizationLevels = n if use_bit_mode == False else 2**n
    print("MY Signal " ,   signal)
    minVal = min(signalValues)
    maxVal = max(signalValues)
    delta = float((maxVal-minVal))
    delta /= float(quantizationLevels)
    intervals = []
    quantizedSignal = []
    encoding = {}
    for i in range(quantizationLevels):
        val = minVal + delta
        intervals.append([round(minVal, 2), round(val, 2)])
        minVal = val
    for i in range(len(signalValues)):
        for j in range(len(intervals)):
            val = intervals[j]
            if val[0] <= signalValues[i] <= val[1]:
                midPoint = (val[0] + val[1]) / 2.0
                quantizedSignal.append((signalTime[i], midPoint))
                encoding[signalTime[i]] = '{0:b}'.format(j)
                break
    error = []
    for i in range(len(quantizedSignal)):
        error.append(quantizedSignal[i][1] - signalValues[i])

    return (quantizedSignal, encoding,  error)

def shift_signal(signal, shift_amount, is_folded = False):
    sign = -1 if not is_folded else 1
    new_signal = []
    for val in signal:
        new_signal.append((val[0] + (sign * shift_amount ), val[1]))
    return new_signal

def fold_signal(signal):
    #We fold around signal of (0,Y)
    folded_signal = []
    for val in signal:
        folded_signal.append((val[0]*-1, val[1]))
        #val
    return folded_signal

def accumulate_signlas(signals_list, sign = 1):
    final_result = signals_list[0]
    
    for i in range(1,  len(signals_list)):
        second = multiply_signal(signals_list[i], sign)
        final_result = add_signals(final_result, second)
    
    return final_result

def remove_dc_component(signal):
    fft_signal = apply_fft(signal, False)
    fft_signal[0] = 0
    no_dc_signal = apply_fft(fft_signal, True)

    # _signal = [signal[k][1] for k in range(len(signal))]
    # fft_signal = np.fft.fft(_signal)
    # fft_signal[0] = 0a
    # no_dc_signal = np.fft.ifft(fft_signal)

    signal_values = [round(no_dc_signal[k].real, 4) for k in range(len(no_dc_signal))]
    final_signal = [(signal[k][0], signal_values[k]) for k in range(len(no_dc_signal))] 

    return final_signal

def get_zero_crossings(signal):
    pass

def convolve_signal(signal, kernel):
    signal1_x = [x[0] for x in signal]
    signal1_y = [x[1] for x in signal]

    kernel_x = [x[0] for x in kernel]
    kernel_y = [x[1] for x in kernel]

    signal_minX = int(min(signal1_x))
    signal_maxX = int(max(signal1_x))
    
    kernel_minX = int(min(kernel_x))
    kernel_maxX = int(max(kernel_x))

    current_comp_num = signal_minX

    result = []
    while True:

        value = 0
        has_valid_term = False

        for i in range(signal_minX, current_comp_num +1):
            xk_ix = i
            hk_ix = current_comp_num - xk_ix

            if signal_maxX >= xk_ix >= signal_minX and  kernel_maxX >= hk_ix >= kernel_minX:
                has_valid_term = True
                value += (signal1_y[xk_ix] * kernel_y[hk_ix])
        
        if has_valid_term:
            result.append((current_comp_num, value))
        else:
            break
        current_comp_num+=1
    return result

def test_convolve():
    pass

def corelate_signal(signal, kernel, is_periodic = False):
    return __correlate_signal(signal, kernel, periodic= is_periodic)

def norm_correlate_signal(signal, kernel, is_periodic = False):
    return __correlate_signal(signal, kernel, periodic= is_periodic, normalized= True)

def __correlate_signal(signal, kernel, periodic = False, normalized = False):
    first_sample_number = signal[0][0] #S[0].X
    
    signal1_length = len(signal)
    kernel_length = len(kernel)

    signal1values = [x[1] for x in signal]
    kernelvalues  = [x[1] for x in kernel]
    num_of_samples = len(signal1values)
    
    if signal1_length != kernel_length:
        num_of_samples = signal1_length + kernel_length - 1
        signal1_augmentingzeros = num_of_samples - signal1_length
        kernel_augmentingzeros = num_of_samples - kernel_length

        # add augmenting zeros
        for i in range(0, signal1_augmentingzeros):
            signal1values.append(0)

        for i in range(0, kernel_augmentingzeros):
            kernelvalues.append(0)
        # print(signal1values)
        # print(kernelvalues)

    kernel_leftrotations = []
    
    if periodic:
        print("periodic")
        #Kernel Rotation
        for i in range(0, num_of_samples):
            first_element = kernelvalues[0]
            del(kernelvalues[0])
            kernelvalues.append(first_element)
            new_list = kernelvalues[:]
            kernel_leftrotations.append(new_list)
        last_rotation = kernel_leftrotations[-1]
        del(kernel_leftrotations[-1])
        
        kernel_leftrotations = [last_rotation] + kernel_leftrotations

    else:
        print("non periodic")
        signal1values2_tmp = list(kernelvalues)
        kernel_leftrotations = [signal1values2_tmp] + kernel_leftrotations
        # get rotations of kernel
        for i in range(0, num_of_samples):
            del kernelvalues[0]
            kernelvalues.append(0)
            new_list = kernelvalues[:]
            kernel_leftrotations.append(new_list)

        del kernel_leftrotations[-1]

    # cross correlate the kernel rotations with kernel
    resulted_signal = []

    current_sample_number = first_sample_number
    
    for i in range(0, num_of_samples):
        sample_sum = 0
        for y in range(0, num_of_samples):
            sample_sum += (signal1values[y] * kernel_leftrotations[i][y])

        resulted_signal.append((current_sample_number, (sample_sum / num_of_samples)))
        current_sample_number += 1
    
    if normalized:
        print("Exec Normalized")
        signal1_sum = np.sum(np.square(signal1values))
        kernel_sum = np.sum(np.square(kernelvalues))
        normalization_factor = np.sqrt(signal1_sum * kernel_sum) / num_of_samples

        resulted_signal = [(x[0], x[1] / normalization_factor) for x in resulted_signal]

    return resulted_signal

