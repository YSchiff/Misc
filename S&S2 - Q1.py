from numpy import *
import matplotlib.pyplot as plt
from sys import exit


# 1.1 - Fourier transform
def trans_fourier(x, t, w):
    if x.shape != (len(x),) or t.shape != (len(t),) or w.shape != (len(w),):
        print 'Inputs must be column vector!'
        exit(1)
    if len(x) != len(t):
        print 'Sample and time vector must be of equal length!'
        exit(1)
    # create exponent matrix made up of phi(w) vectors - each line containing phi of different frequency
    w_mat, tmp = meshgrid(w, t)
    t_mat, tmp = meshgrid(t, w)
    phi_mat = exp(multiply(w_mat.transpose(), t_mat) * 1j)

    delta_t = abs(t[0] - t[1])
    # column vector which is the dot product of phi and x
    return delta_t * dot(conjugate(phi_mat), x)


# 1.2 - Inverse fourier transform
def inv_trans_fourier(X, w, t):
    # using duality property of fourier transform
    # assumed signal is real, return discards imaginary part anyway
    return real(trans_fourier(X, -w, t) / (2 * pi))


def heavyside(x):
    return 0.5 * (sign(x + 1))


def plot(x, y, x_label, y_label, title, color, label, x_lim=0):
    plt.plot(x, y, color, label=label)
    if title != "":
        plt.title(title)
    if x_label != "":
        plt.xlabel(x_label)
    if y_label != "":
        plt.ylabel(y_label)
    if x_lim != 0:
        axis = plt.gca()
        axis.set_xlim([-x_lim, x_lim])
    plt.legend()


def main():

    # 1.3 - time vector
    dt = 0.02
    t = arange(-3, 3, step=dt).transpose()

    # signal
    x = sin(2*pi*t) + 2*cos(4*pi*t)

    # 1.4 - frequency vector
    fs = 1/dt
    w = 2 * pi * linspace(-fs/2, fs/2, len(t)+1, endpoint=True).transpose()

    # plot signal x(t) and fourier transform
    plt.close('all')
    plt.subplot(2, 1, 1)

    # plot signal
    plot(t, x, "t[sec]", "x(t)", "x(t) = sin(2pi*t) + 2cos(2pi*2t)", 'g', "x(t)", pi)

    # calculate Fourier transform and inverse transform
    fourier_x = trans_fourier(x, t, w)
    inv_fourier_x = inv_trans_fourier(fourier_x, w, t)

    # plot inverse transform
    plot(t, inv_fourier_x, "", "", "", 'k--', "InverseFourier{x(t)}")

    plt.subplot(2, 1, 2)
    # plot Fourier transform and inverse Fourier transform
    plot(w, absolute(fourier_x), "w[Hz]", "|X(w)|", "|Fourier{x(t)}|", 'b', "abs(Fourier{x(t)})", 10*pi)
    plt.tight_layout()

    # 1.5
    _w = 3*pi
    # divide _w by pi since sinc multiplies input by factor pi
    y = (_w/pi) * sinc((_w/pi)*t)
    plt.figure(2)
    plt.subplot(2, 1, 1)

    # plot signal y(t) and fourier transform
    plot(t, y, "t[sec]", "y(t)", "y(t) = 3sincM(3*t)", 'g', "y(t)", pi)

    # calculate Fourier transform and inverse transform
    fourier_y = trans_fourier(y, t, w)
    inv_fourier_y = inv_trans_fourier(fourier_y, w, t)

    # plot inverse transform
    plot(t, inv_fourier_y, "", "", "", 'k--', "InverseFourier{y(t)}")

    plt.subplot(2, 1, 2)
    # plot Fourier transform and inverse Fourier transform
    plot(w, absolute(fourier_y), "w[Hz]", "|Y(w)|", "|Fourier{y(t)}|", 'b', "abs(Fourier{y(t)})", 10*pi)
    plt.tight_layout()

    # 1.6 - plot analytical version of Y(w): graphs are close but don't completely overlap due to not enough elements
    # in y(t). To increase match we need to use a more "crowded" time vector
    analytical_fourier_y = heavyside(w + 3*pi) - heavyside(w - 3*pi)
    plot(w, absolute(analytical_fourier_y), "", "", "", 'g', "|AnalyticalFourier{y(t)})|")

    # 1.8 - convulsion in time plane is multiplication in Fourier plane
    fourier_z = multiply(fourier_x, fourier_y)
    z = inv_trans_fourier(fourier_z, w, t)

    # plot - x(t), X(w), Y(w), Z(w)
    plt.figure(3)
    plt.subplot(2, 2, 1)
    plot(t, x, "t[sec]", "x(t)", "x(t) = sin(2pi*t) + 2cos(2pi*2t)", 'g', "x(t)", pi)
    plt.subplot(2, 2, 2)
    plot(w, absolute(fourier_x), "w[Hz]", "|X(w)|, |Y(w)|", "|Fourier{x(t)}|, |Fourier{y(t)}|", 'b', "abs(Fourier{x(t)})", 10 * pi)
    plot(w, absolute(fourier_y), "", "", "", 'r', "abs(Fourier{y(t)})", 10 * pi)
    plt.subplot(2, 2, 3)
    plot(t, z, "t[sec]", "z(t)", "z(t) = (x * y)(t)", 'g', "z(t)", pi)
    plt.subplot(2, 2, 4)
    plot(w, absolute(fourier_z), "w[Hz]", "|Z(w)|", "|Fourier{z(t)}|", 'b', "abs(Fourier{z(t)})", 10 * pi)
    plt.tight_layout()

    axis = plt.gca()
    axis.set_ylim(0, 5)

    plt.show()


if __name__ == '__main__':
    main()

