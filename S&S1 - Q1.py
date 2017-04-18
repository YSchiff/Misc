import numpy
from matplotlib import pyplot


# plots f1 and f2 functions with a requested number of points
def plot(points):
    pyplot.figure()
    t = numpy.linspace(0, 5, num=points)
    f1 = numpy.sin(2 * numpy.pi * 10 * t)
    f2 = numpy.sin(2 * numpy.pi * 10.5 * t)
    pyplot.plot(t, f1, 'r', linewidth=1.75, label="f1")
    pyplot.plot(t, f2, 'b', linewidth=1.75, label="f2")
    axis = pyplot.gca()
    axis.set_xlim([0, 0.5])
    pyplot.ylabel("Amplitude")
    pyplot.xlabel("Time[sec]")
    pyplot.title("f1,f2 with {} point accuracy!".format(points))
    pyplot.legend()
    return t, f1, f2


def main():

    ##### Part A #####

    # 1:
    t1 = numpy.linspace(0, 5, num=100)

    # 2: range is [0,5.05) with step of 0.05 so last element is 5
    t2 = numpy.arange(0, 5.00, 0.05)

    # 3: t1 is of length 100 - as requested by num=100, t2 is of length 101 - from 0 to 5 with steps of 0.05
    print "t1 length: {}".format(len(t1))
    print "t2 length: {}".format(len(t2))

    # 4: (This is done twice - repeated in part B, for the sake of the assignment order only!)
    t = t1
    f1 = numpy.sin(2*numpy.pi*10*t)
    f2 = numpy.sin(2*numpy.pi*10.5*t)
    f = f1 + f2

    ##### Part B #####

    # 1,3,4,5: using t with 100 points
    plot(100)

    # 2,3,4,5: using t with 10000 points - increase accuracy since step is smaller
    t, f1, f2 = plot(10000)

    # 6: plot f. new f is calculated with higher accuracy - 10000 points
    f = f1 + f2
    pyplot.figure()
    pyplot.plot(t, f, 'g', linewidth=1.5, label="f")

    # 8: plot function envelope
    f_env = 2*numpy.cos(numpy.pi*0.5*t)
    pyplot.plot(t, f_env, 'b', linewidth=1.5, label="f_env")

    # 9: add titles
    pyplot.ylabel("Amplitude")
    pyplot.xlabel("Time[sec]")
    pyplot.title("Beat Effect")
    pyplot.legend()
    pyplot.gca().set_xlim([0, 5])
    pyplot.show()


if __name__ == '__main__':
    main()
