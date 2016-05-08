import tandem_repeat as tandem
import suffix_tree as suffix
import time
import argparse
import matplotlib.pyplot as plt
import math


def experiment(aString, aOutputPrefix):
    timings = []
    comparisons = []

    # run through aString, processing each of the possible prefixes
    # to generate data files showing how the two algorithms perform as n grows
    for i in range(2, len(aString)):
        n = i
        curr_str = aString[0:i]
        tree = suffix.Tree(curr_str)

        # timing basic algorithm
        basic_starttime = time.time()
        basic_branching, basic_nonbranching = tandem.basic_tandemrepeat(tree)
        basic_endtime = time.time()
        basic_timediff = basic_endtime - basic_starttime
        # basic_timediff = basic_timediff / (n * math.log(n))
        basic_timediff = basic_timediff / (n * n)

        # timing optimized algorithm
        optmzd_starttime = time.time()
        optmzd_branching, optmzd_nonbranching = tandem.optimized_tandemrepeat(tree)
        optmzd_endtime = time.time()
        optmzd_timediff = optmzd_endtime - optmzd_starttime
        optmzd_timediff = optmzd_timediff / (n * math.log(n))
        optmzd_timediff = optmzd_timediff / (n * n)

        timings.append((i, basic_timediff, optmzd_timediff))
        comparisons.append((i, 
                            (basic_branching, basic_nonbranching),
                            (optmzd_branching, optmzd_nonbranching)))

    # generating data points and writing to files for plotting
    basic_timings_datapoints = ''
    optmzd_timings_datapoints = ''
    for i, t in enumerate(timings):
        basic_timings_datapoints += '%i,%f\n' % (i, t[1])
        optmzd_timings_datapoints += '%i,%f\n' % (i, t[2])
    basic_output = '%s_basictimings.txt' % aOutputPrefix
    optmzd_output = '%s_optmzdtimings.txt' % aOutputPrefix
    suffix.write_output(basic_output, basic_timings_datapoints)
    suffix.write_output(optmzd_output, optmzd_timings_datapoints)

    # TODO: full string 100 iterations to find min, max, avg time?

def plot(csvFile):
    # data = np.loadtxt(csvFile, delimiter=',')
    data = suffix.read_input(csvFile)

    data = data.rstrip().split('\n')
    xs = []
    ys = []
    for p in data:
        data_tuple = p.split(',')
        xs.append(int(data_tuple[0]))
        ys.append(float(data_tuple[1]))

    plt.plot(xs, ys)
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input",
                        help="File containing text to perform experiment on")
    args = parser.parse_args()

    inputfile = args.input
    input = suffix.read_input(inputfile)

    outputprefix = inputfile[0:len(inputfile)-4]
    experiment(input, outputprefix)

    plot('%s_basictimings.txt' % outputprefix)
    plot('%s_optmzdtimings.txt' % outputprefix)

if __name__ == '__main__':
    main()
