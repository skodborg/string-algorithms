import math
import matplotlib.pyplot as plt
import tandem_repeat as tr
import suffix_tree as st
import argparse


def simple_profiling(aFile, stepsize):
    input = st.read_input(aFile)

    results = []
    for i in range(2, len(input), stepsize):
        string = input[:i]
        tree = st.Tree(string)
        ith_result = tr.optimized_tandemrepeat(tree, True)
        results.append((i, ith_result))

    xs = []
    linear_ys = []
    nlogn_ys = []
    squared_ys = []

    for p in results:
        xs.append(p[0])
        linear_ys.append(p[1] / p[0])
        nlogn_ys.append(p[1] / (p[0] * math.log(p[0])))
        squared_ys.append(p[1] / (p[0] * p[0]))

    plt.plot(xs, linear_ys)
    plt.show()
    plt.plot(xs, nlogn_ys)
    plt.show()
    plt.plot(xs, squared_ys)
    plt.show()


def plot(csvFile):
    data = st.read_input(csvFile)
    data = data.rstrip().split('\n')
    xs = []
    ys = []
    for p in data:
        data_tuple = p.split(',')
        xs.append(int(data_tuple[0]))
        ys.append(float(data_tuple[1]))
    plt.plot(xs, ys)
    plt.show()
    return xs, ys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument('-n', '--stepsize', type=int)
    args = parser.parse_args()

    stepsize = args.stepsize
    inputfile = args.file

    simple_profiling(inputfile, stepsize)


if __name__ == '__main__':
    main()
