from numpy import *
from scipy import signal
from scipy.io import loadmat
from scipy.io.wavfile import write
from winsound import PlaySound
from winsound import SND_FILENAME
import matplotlib.pyplot as plt
import os
from sys import exit
import Q1


# base frequency - A4
f0 = 440
# required notes - E4, D4, C4
e = -5
d = -7
c = -9
# note lengths
full_note = 0.4
hollow_note = 0.8
final_note = 2.4


# 2.1
def make_note(n, tao, fs):
    # note frequency
    f = (2 ** (double(n)/12)) * f0
    w = 2*pi*f

    dt = 1/fs
    # time vector
    t = arange(0, tao, dt)

    # return note signal
    return multiply(cos(w*t), exp((-3*t)/tao))


# 2.2
def make_tune(n_vec, t_vec, fs):
    if len(n_vec) != len(t_vec):
        print "Note vector and length vector must be of equal length!"
        exit(1)
    s = []
    for i, n in enumerate(n_vec):
        s = concatenate([s, make_note(n, t_vec[i], fs)])
    return s


# play tune s
def play(s, fs):
    # create temporary WAV file to play tune
    scaled = int16(s / max(absolute(s)) * 32767)
    write('tmp.wav', fs, scaled)
    PlaySound('tmp.wav', SND_FILENAME)
    os.remove('tmp.wav')


def main():

    # 2.3 - Marry had a little lamb tune
    # sampling frequency
    fs = math.pow(2, 13)

    # note_vector
    n = [e, d, c, d, e, e, e, d, d, d, e, e, e, e, d, c, d, e, e, e, c, d, d, e, d, c]
    # duration vector
    t = [full_note, full_note, full_note, full_note, full_note, full_note, hollow_note, full_note, full_note,
         hollow_note, full_note, full_note, hollow_note, full_note, full_note, full_note, full_note, full_note,
         full_note, full_note, full_note, full_note, full_note, full_note, full_note, final_note]

    s = make_tune(n, t, fs)
    play(s, fs)

    # 2.4 create spectrogram
    fig, ax = plt.subplots()
    cmap = plt.get_cmap('viridis')
    pxx, freq, _t, cax = ax.specgram(s, Fs=fs, mode='magnitude', NFFT=2**11, noverlap=0, cmap=cmap)
    fig.colorbar(cax, label='Power/frequency (dB/Hz)')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    axis = plt.gca()
    axis.set_ylim([0, 600])
    axis.set_xlim([0, 12])

    # 2.5 - Fourier transform of tune
    # time vector
    dt = 1/fs
    # adjust total time so vectors will be of equal length
    total_time = sum(t) + (len(s) - len(arange(0, sum(t), dt))) * dt
    t = arange(0, total_time, dt).transpose()

    # frequency vector
    dw = 2*pi
    w = arange(dw, 801*dw, dw).transpose()
    f = w/(2*pi)

    # plot Fourier transform of tune
    plt.figure(2)
    fourier_s = Q1.trans_fourier(s.transpose(), t, w)
    Q1.plot(f, absolute(fourier_s), "f[Hz]", "|S(f)|", "|Fourier{s(t)}|", 'b', "abs(Fourier{s(t)})")
    plt.tight_layout()

    # 2.6 - add noise to s and plot fourier transform of s with noise
    if not os.path.isfile(os.path.join(os.getcwd(), "noise.mat")):
        print "noise.mat file must be in working directory"
        exit(1)

    # load noise from mat file
    noise_dict = loadmat("noise.mat")
    noise = noise_dict['noise'][0]

    # play noise and add noise to s
    play(noise, fs)

    s_noise = add(s, noise[0: len(s)])
    # play tune with noise
    play(s_noise, fs)

    # plot clean tune and noisy tune
    fourier_s_noise = Q1.trans_fourier(s_noise.transpose(), t, w)
    plt.figure(3)

    plt.subplot(2, 1, 1)
    Q1.plot(f, absolute(fourier_s), "f[Hz]", "|S(f)|", "Fourier transform of tune", 'b', "|Fourier{s(t)}|")

    plt.subplot(2, 1, 2)
    Q1.plot(f, absolute(fourier_s_noise), "f[Hz]", "|S_noisy(f)|", "Fourier transform of tune with noise", 'b', "|Fourier{s_noisy(t)}|")
    plt.tight_layout()

    # 2.8 - use BPF to filter out noise
    filter_t = arange(-2, 2+dt, dt).transpose()

    # The Fourier transform of h(t) gives us H(w) = heaviside(w-500pi) - heaviside(w-900pi) - the desired BPF
    h = 900*sinc(900*filter_t) - 500*sinc(500*filter_t).transpose()
    fourier_h = Q1.trans_fourier(h, filter_t, w)

    # calculate tune after passing through BPF
    s_clean = convolve(h, s_noise, 'same').transpose()
    fourier_s_clean = Q1.trans_fourier(s_clean, t, w)

    plt.figure(4)

    plt.subplot(3, 1, 1)
    Q1.plot(f, absolute(fourier_s), "f[Hz]", "|S(f)|", "Fourier transform of tune", 'b', "|Fourier{s(t)}|")

    plt.subplot(3, 1, 2)
    Q1.plot(f, absolute(fourier_s_noise), "f[Hz]", "|S_noisy(f)|", "Fourier transform of tune with noise", 'b', "|Fourier{s_noisy(t)}|")
    Q1.plot(f, absolute(fourier_h), "", "", "", 'r', "BPF")

    plt.subplot(3, 1, 3)
    Q1.plot(f, absolute(fourier_s_clean), "f[Hz]", "|S_clean(f)|", "Fourier transform filtered tune", 'b', "|Fourier{s_clean(t)}|")

    plt.tight_layout()

    play(s_clean, fs)
    plt.show()


if __name__ == '__main__':
    main()

