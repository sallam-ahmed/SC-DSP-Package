import cmath
import numpy as np

def apply_dft(signal):
    signal_values = [x[1] for x in signal]
    return _apply_dft(signal_values, False)

def apply_idft(fourier_output):
    return _apply_dft(fourier_output, True)

def write_dft_polar_output(fourier_output):
    values = [cmath.polar(x) for x in fourier_output]
    with open('_data/outputSignal.ds', 'w') as writer:
        writer.writelines('1\n')
        writer.writelines('0\n')
        writer.writelines(str(len(values))+'\n')
        for i in range(len(values)):
            writer.writelines('{0} {1} {2}'.format(
                i, values[i][0], values[i][1])+'\n')
    print("Done writing suc.!")

def _apply_dft(fourier_input, bool_is_inverse):
    fourier_output = _apply_fourier(fourier_input, bool_is_inverse)

    if bool_is_inverse:
        cmpx = [round(x.real) for x in fourier_output]
        print('My Inverse Output = ', cmpx)
        return cmpx
    return fourier_output
    
def _apply_fourier(values, is_inverse):
    fourier_iterations = len(values)
    # x(n) * e^(-jk2PIn/N)
    final_fourier = []
    J = 1j if is_inverse else -1j
    for k in range(fourier_iterations):
        x_Value = 0
        for n in range(fourier_iterations):
            x_n = values[n]
            x_Value += x_n * \
                cmath.exp(J * k * 2 * np.pi * n/fourier_iterations)

        final_fourier.append(
            complex(round(x_Value.real), round(x_Value.imag)))

    if is_inverse:
        final_fourier = [x / fourier_iterations for x in final_fourier]

    return final_fourier

def apply_fft(signal, bool_is_inverse):
    y_values = [x[1] if not bool_is_inverse else x for x in signal]

    fourier_output = _recursive_fft(y_values, bool_is_inverse)

    for i in range(len(fourier_output)):
        inverse_len = 1 if not bool_is_inverse else len(y_values)
        real = round(fourier_output[i].real)/inverse_len
        imag = round(fourier_output[i].imag)
        
        if imag == -0.0:
           imag = 0

        cmx = complex(real, imag)
        fourier_output[i] = cmx
    final_output = list(fourier_output)
    if bool_is_inverse:
        final_output = [round(fourier_output[k].real) for k in range(len(fourier_output))]
    return final_output

def _recursive_fft(values, bool_is_inverse):
    N = len(values)
    # if np.log2(N) % 1 > 0:
    #     raise "Error, not power of 2."

    if N <= 1:
        return values

    even = _recursive_fft(values[0::2], bool_is_inverse)
    odd = _recursive_fft(values[1::2], bool_is_inverse)

    sign = 2j if bool_is_inverse else -2j
    omega_arr = [np.exp(sign*np.pi*k/N)*odd[k] for k in range(N//2)]

    return [even[k] + omega_arr[k] for k in range(N//2)] + [even[k] - omega_arr[k] for k in range(N//2)]

def test_fft():
    values = [(0,1), (1,2), (2,3), (3,4)]
    np_fft = np.fft.fft([1,2,3,4])
    my_fft = apply_fft(values, False)
    print("NP FFT:\b{0}".format(np_fft))
    print("My FFT:\b{0}".format(my_fft))

    np_ifft = np.fft.ifft(np_fft)
    my_ifft = apply_fft(my_fft, True)

    print("NP IFFT:\b{0}".format(np_ifft))
    print("My IFFT:\b{0}".format(my_ifft))

def get_amblitudes(fourier_output, sampled_frequency):
    signal_amblitude = []
    n = len(fourier_output)
    print(fourier_output)
    signal_amblitude = [cmath.sqrt(s.real**2 + s.imag**2)
                    for s in fourier_output]

    x_values = _get_fourier_signal_xvals(sampled_frequency, n)

    return (x_values, signal_amblitude)

def get_phase_shift(fourier_output, sampled_frequency):
    signal_phase_shift = []
    n = len(fourier_output)
    signal_phase_shift = [np.degrees(cmath.atan(x.imag / x.real).real)
                    for x in fourier_output]

    x_values = _get_fourier_signal_xvals(sampled_frequency, n)

    return (x_values, signal_phase_shift)

def _get_fourier_signal_xvals(sampled_frequency, fourier_length):
    x_values = []
    # 2*PI / N * (1/Fs) -? X0
    x_0 = 2 * np.pi / (fourier_length * (1/sampled_frequency))
    x_values = [(x * x_0) for x in list(range(2, fourier_length+1))]
    x_values.insert(0, x_0)
    
    return x_values

test_fft()

