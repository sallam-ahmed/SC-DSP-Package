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