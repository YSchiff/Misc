import numpy
from matplotlib import pyplot
import collections

# Constants:
j = numpy.complex(0, 1)
pi = numpy.pi
# freq
w = 1
# period
T = 2*pi


# receives a discrete function x_t, the relevant vector t
# the time step and the requested coefficient index. returns the fourier coefficient of index l
def coefficient(x_t, l, t, delta_t):
    exp = numpy.exp(j * w * l * t)
    return (delta_t/T)*numpy.vdot(exp, x_t)


# calculates the FS of of given discrete function x_t, with elements in range of index l
def calculate_fs(x_t, l, t, delta_t):
    # list of elements of current FS
    elements = []
    for i in range(-l, l + 1):
        coeff_i = coefficient(x_t, i, t, delta_t)
        exp_i = numpy.exp(j * w * i * t)
        elements.append(coeff_i * exp_i)
    # return FS - sum of all elements. Used real function to remove negligible imaginary part
    return numpy.real(sum(elements))


def calc_overshoot(fs, x_t):
    max_index = numpy.argmax(fs)
    return ((fs[max_index] - x_t[max_index]) / x_t[max_index]) * 100


def main():

    # 3: time vector, time step
    t, delta_t = numpy.linspace(-numpy.pi, numpy.pi, num=10000, retstep=True)

    # function
    x_t = t

    # Fourier coefficients 0,1,-1,2,-2
    x_s0 = coefficient(x_t, 0, t, delta_t)
    x_s1 = coefficient(x_t, 1, t, delta_t)
    x_s2 = coefficient(x_t, 2, t, delta_t)
    x_s_neg1 = coefficient(x_t, -1, t, delta_t)
    x_s_neg2 = coefficient(x_t, -2, t, delta_t)
    print "Xs[0]: {}. Analytical value is: {}".format(x_s0, numpy.around(x_s0, decimals=1))
    print "Xs[1]: {}. Analytical value is: {}".format(x_s1, numpy.around(x_s1, decimals=1))
    print "Xs[2]: {}. Analytical value is: {}".format(x_s2, numpy.around(x_s2, decimals=1))
    print "Xs[-1]: {}. Analytical value is: {}".format(x_s_neg1, numpy.around(x_s_neg1, decimals=1))
    print "Xs[-2]: {}. Analytical value is: {}".format(x_s_neg2, numpy.around(x_s_neg2, decimals=1))

    # 4: plot Fourier Series with the following number of coefficient ranges:

    M = [1, 2, 3, 10, 50, 100, 1000]
    # dictionary of each FS function with varying number of elements, according to current M
    fourier_series = {}
    for m in M:
        fourier_series[m] = calculate_fs(x_t, m, t, delta_t)
        # plot
        pyplot.plot(t, fourier_series[m], linewidth=1.5, label="f_{}".format(m))

    pyplot.ylabel("FS{x(t)}")
    pyplot.xlabel("Time[sec]")
    pyplot.title("Fourier Series!")
    axis = pyplot.gca()
    axis.set_xlim([-pi, pi])
    pyplot.legend(loc=4)

    # 5: calculate average square error of FS functions - per M
    m_sq_error = collections.OrderedDict()
    for m in sorted(M):
        m_sq_error[m] = numpy.mean(numpy.square(x_t - fourier_series[m]), dtype=numpy.float64)
    # plot graph on MSE per M
    pyplot.figure()
    pyplot.plot(m_sq_error.keys(), m_sq_error.values(), 'r', linewidth=3, label="MSE", )
    pyplot.ylabel("MSE")
    pyplot.xlabel("M - number of elements")
    pyplot.title("Average Mean Square Error per #elements")
    pyplot.legend()

    # 6: Calculate overshot - caused by the Gibbs Phenomenon. No matter how big an M we take we will get an
    # overshoot of approximately 18%.
    # The Gibbs phenomenon gives a jump of 9% increase from the discontinuity in the function. The function jumps from
    # pi to -pi, total jump of 2 pi. We get double the effect - 18% - since overshoot relates to only half of the jump.
    # the overshoot here will be the point the fourier series reaches its maximum
    overshoot_1000 = calc_overshoot(fourier_series[1000], x_t)
    print "Overshoot for M=1000: {}".format(overshoot_1000)

    fs_2000 = calculate_fs(x_t, 2000, t, delta_t)
    overshoot_2000 = calc_overshoot(fs_2000, x_t)
    print "Overshoot for M=2000: {}".format(overshoot_2000)

    # 7: since these are discrete functions, the limit t->pi is the value closest to pi
    # i.e the last element of our functions, since the last one is pi
    # the fs value at the edge is fixed - 0, as expected from an odd periodic function
    lim_pi_1000 = x_t[-1] - fourier_series[1000][-1]
    print "limit t->pi [x(t) - FS[x(t)]_1000 = {}".format(lim_pi_1000)

    # for a greater M, for example M=2000. The result remains the same - the fs value at the edge is 0, but the
    # function value is pi. The series doesn't converge at this point!
    lim_pi_2000 = x_t[-1] - fs_2000[-1]
    print "limit t->pi [x(t) - FS[x(t)]_2000 = {}".format(lim_pi_2000)

    # 8: Parseval Theorem:
    # calculate the energy in the time plain and the frequency plain - we get convergence in energy
    time_energy = (delta_t/T) * numpy.vdot(x_t, x_t)
    coeffs_1000 = []
    for i in range(-1000, 1001):
        coeffs_1000.append(coefficient(x_t, i, t, delta_t))
    freq_energy = numpy.vdot(coeffs_1000, coeffs_1000)
    print "Energy in time plain: {}".format(time_energy)
    print "Energy in frequency plain: {}".format(numpy.real(freq_energy))
    pyplot.show()


if __name__ == '__main__':
    main()
