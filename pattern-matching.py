import time
import suffix_tree as st
import profiling as pf
import re

 
def simple_longest_border(aString):
    ''' finds the longest border of aString in time O(n^2) '''
    borderlength = 0
    n = len(aString) - 1            # -1 to adjust for zero-indexing in loops
    x = aString
    for i in range(n):              # takes O(n)
        if x[:i + 1] == x[n - i:]:  # equality test has complexity O(n)
            borderlength = i + 1    # +1 as i is a list index, not a length
        # print(x[:i+1] + ' : ' + x[n-1-i:])
    return borderlength


def border_array(aString, profiling=False):
    ''' returns a list of length n of integers i, where each int i describes
        the longest border found in the string aString[0:i] '''
    ba = [0]
    n = len(aString)
    x = aString
    profiling_counter = 0

    for i in range(1, n):
        profiling_counter += 1
        b = ba[i - 1]  # -1 to convert i from one- to zero-indexed list index
        while b > 0 and x[i + 1 - 1] != x[b + 1 - 1]:  # -1's again to convert
            profiling_counter += 1
            b = ba[b - 1]  # -1 again to convert
        if x[i + 1 - 1] == x[b + 1 - 1]:  # -1's again to convert
            ba.append(b + 1)
        else:
            ba.append(0)
    if profiling:
        return profiling_counter
    else:
        return ba


def search_naive(aString, aPattern, profiling=False):
    ''' finds occurrences of aPattern in aString in time O(nm) and returns
        a list of one-indexed occurrences of aPattern in aString '''
    profiling_counter = 0
    n = len(aString) - 1
    m = len(aPattern) - 1
    s = aString
    p = aPattern
    occurrences = []
    for i in range(n):
        profiling_counter += 1

        if i+m+1 != len(p):
            profiling_counter += 1
        else:
            profiling_counter += len(p)

        if s[i:i + m + 1] == p:
            # found a pattern match! append index to list of occurrences
            occurrences.append(i + 1)

    if profiling:
        return profiling_counter
    else:
        return occurrences


def search_ba(aString, aPattern, profiling=False):
    # An occurrence of aPattern exists if a border in the array has
    # length m, the length of the pattern.
    # This is because the string we're looking at will always contain the
    # searched pattern as the left-most part of the string, and thus will
    # be a part of every border of length m. If one such exists, then the
    # right-most part of the border must equal the left-most, which is our
    # pattern, and we have then found an occurrence of the pattern within
    # the string.
    # An example: the string we consider is constructed as
    #             ssi$mississippi
    #             i.e. aPattern + '$' + aString
    #             every border found when looking at all prefixes of this
    #             string will then contain ssi and only ssi, as $ will only
    #             appear once by string construction assumptions
    m = len(aPattern)
    profiling_counter = 0
    string = aPattern + '$' + aString  # length: n + 1 + m
    if profiling:
        profiling_counter += border_array(string, profiling)
    borderarr = border_array(string)   # complexity: ?
    occurrences = []
    for i, length in enumerate(borderarr):  # complexity: O(n)
        profiling_counter += 1
        if length >= m:
            # adding 1 below to convert list zero-index to string one-index
            pattern_occurrence_idx = i - (2 * m) + 1
            occurrences.append(pattern_occurrence_idx)
    if profiling:
        return profiling_counter
    else:
        return occurrences


def search_kmp(aString, aPattern, profiling=False):
    occurrences = []
    global profiling_counter
    profiling_counter = 0

    # preprocessing:
    m = len(aPattern)
    n = len(aString)
    x = aString
    p = aPattern
    if profiling:
        ba_count = border_array(aPattern, profiling)
        profiling_counter += ba_count
    B = border_array(aPattern)
    Bm = [0]
    for j in range(2, m + 1 + 1):
        profiling_counter += 1
        Bm.append(B[j - 1 - 1] + 1)
    
    # helper
    def match(i, j, m):
        global profiling_counter
        if len(x[i - 1]) != len(p[j - 1]):
            profiling_counter += 1
        else:
            profiling_counter += len(p[j - 1])

        while j <= m and x[i - 1] == p[j - 1]:
            if len(x[i - 1]) != len(p[j - 1]):
                profiling_counter += 1
            else:
                profiling_counter += len(p[j - 1])

            profiling_counter += 1
            i += 1
            j += 1
        return i, j

    # main:
    i, j = 1, 1
    while i <= n - m + j:
        profiling_counter += 1
        i, j = match(i, j, m)
        if j == m + 1:
            # pattern found! 
            # subtract pattern length from current index and report this
            occurrences.append(i - m)
        if j == 1:
            i += 1
        else:
            j = Bm[j - 1]

    if profiling:
        return profiling_counter
    else:
        return occurrences


def verify_naive_Onm():

    input = open('project3/chr1_10000000.txt', 'r', encoding='latin1').read()
    p10 = open('project3/pattern10.txt', 'r', encoding='latin1').read()
    p20 = open('project3/pattern20.txt', 'r', encoding='latin1').read()
    p30 = open('project3/pattern30.txt', 'r', encoding='latin1').read()
    p40 = open('project3/pattern40.txt', 'r', encoding='latin1').read()
    p50 = open('project3/pattern50.txt', 'r', encoding='latin1').read()
    p100 = open('project3/pattern100.txt', 'r', encoding='latin1').read()
    p500 = open('project3/pattern500.txt', 'r', encoding='latin1').read()
    p1000 = open('project3/pattern1000.txt', 'r', encoding='latin1').read()
    p5000 = open('project3/pattern5000.txt', 'r', encoding='latin1').read()
    p10000 = open('project3/pattern10000.txt', 'r', encoding='latin1').read()
    p50000 = open('project3/pattern50000.txt', 'r', encoding='latin1').read()
    p100000 = open('project3/pattern100000.txt', 'r', encoding='latin1').read()
    p500000 = open('project3/pattern500000.txt', 'r', encoding='latin1').read()
    p1000000 = open('project3/pattern1000000.txt', 'r', encoding='latin1').read()

    patterns = [p10, p20, p30, p40, p50, p100, 
                p500, p1000, p5000, p10000, p50000, 
                p100000, p500000, p1000000]

    for p in patterns:
        naive_times = []
        ba_times = []
        kmp_times = []
        for _ in range(3):
            start_time = time.time()
            search_naive(input, p)
            end_time = time.time()
            naive_times.append(end_time - start_time)

            start_time = time.time()
            search_ba(input, p)
            end_time = time.time()
            ba_times.append(end_time - start_time)

            start_time = time.time()
            search_kmp(input, p)
            end_time = time.time()
            kmp_times.append(end_time - start_time)
        naive_times.sort()
        ba_times.sort()
        kmp_times.sort()
        print('p%i result median of 3 runs of naive, ba and kmp:' % len(p))
        print('naive: %f' % naive_times[1])
        print('ba: %f' % ba_times[1])
        print('kmp: %f\n' % kmp_times[1])


def experiments(aInputFile, aPatternFile):
    f = open(aInputFile, 'r', encoding='latin1')
    input = f.read()
    f = open(aPatternFile, 'r', encoding='latin1')
    pattern = f.read()
    
    total_time = 0
    count = 0

    for _ in range(3):
        start_time = time.time()
        naive_result = search_naive(input, pattern)
        end_time = time.time()
        count += 1
        total_time += end_time - start_time
    naive_avg = total_time / count
    print('naive avg: %f' % naive_avg)
    
    total_time = 0
    count = 0

    for _ in range(3):
        start_time = time.time()
        ba_result = search_ba(input, pattern)
        end_time = time.time()
        count += 1
        total_time += end_time - start_time
    ba_avg = total_time / count
    print('ba avg: %f' % ba_avg)

    total_time = 0
    count = 0

    for _ in range(3):
        start_time = time.time()
        kmp_result = search_kmp(input, pattern)
        end_time = time.time()
        count += 1
        total_time += end_time - start_time
    kmp_avg = total_time / count
    print('kmp avg: %f' % kmp_avg)

    print()
    print(naive_result)
    print()
    print(ba_result)
    print()
    print(kmp_result)

def verify_search_correctness():
    input = open('project3/chr1_10000000.txt', 'r', encoding='latin1').read()
    p10 = open('project3/pattern10.txt', 'r', encoding='latin1').read()
    p20 = open('project3/pattern20.txt', 'r', encoding='latin1').read()
    p30 = open('project3/pattern30.txt', 'r', encoding='latin1').read()
    p40 = open('project3/pattern40.txt', 'r', encoding='latin1').read()
    p50 = open('project3/pattern50.txt', 'r', encoding='latin1').read()
    patterns = [p10, p20, p30, p40, p50]

    for p in patterns:
        naive_result = search_naive(input, p)
        naive_result.sort()
        ba_result = search_ba(input, p)
        ba_result.sort()
        kmp_result = search_kmp(input, p)
        kmp_result.sort()

        # comparison reference: python built-in regular expressions
        # adding 1 as apparently we index from 1 in strings in this course
        re_result = [m.start() + 1 for m in re.finditer('(?=%s)' % p, input)]
        re_result.sort()

        match = True
        if (naive_result != re_result):
            print('naive differs on pattern %s' % p)
            match = False
        if (ba_result != re_result):
            print('ba differs on pattern %s' % p)
            match = False
        if (kmp_result != re_result):
            print('kmp differs on pattern %s' % p)
            match = False

        if match:
            print('all implementations worked on pattern %s' % p)
        else:
            print(re_result)

def verify_running_time():
    # results = []
    # xs = []
    # for i in range(10, 1000, 10):
    #     input = 'a' * i
    #     pattern = 'a'
    #     results.append(search_naive(input, pattern, True)/i)
    #     xs.append(i)
    # pf.plot_list(results, xs)
    

    # results = []
    # xs = []
    # for i in range(100, 10000, 10):
    #     input = 'a' * 20000
    #     pattern = 'a' * i
    #     results.append(search_naive(input, pattern, True)/i)
    #     xs.append(i)
    # pf.plot_list(results, xs)


    # results = []
    # xs = []
    # for i in range(10, 1000, 10):
    #     input = 'a' * i
    #     pattern = 'a'
    #     results.append(search_ba(input, pattern, True)/i)
    #     xs.append(i)
    # pf.plot_list(results, xs)

    # results = []
    # xs = []
    # for i in range(10, 1000, 10):
    #     input = 'a' * 1000
    #     pattern = 'a' * i
    #     results.append(search_ba(input, pattern, True)/i)
    #     xs.append(i)
    # pf.plot_list(results, xs)

    results = []
    xs = []
    for i in range(10, 1000, 10):
        input = 'a' * i
        pattern = 'a'
        results.append(search_kmp(input, pattern, True)/i)
        xs.append(i)
    pf.plot_list(results, xs)

    results = []
    xs = []
    for i in range(10, 1000, 10):
        input = 'a' * 1000
        pattern = 'a' * i
        results.append(search_kmp(input, pattern, True)/i)
        xs.append(i)
    pf.plot_list(results, xs)

def compare_running_time():
    input = open('project3/chr1_10000000.txt', 'r', encoding='latin1').read()
    input = input[0:100000]
    search_pattern = open('project3/pattern500.txt', 'r', encoding='latin1').read()

    start_time = time.time()
    tree = st.Tree(input)
    construction_time_cunsumed = time.time() - start_time
    print('suffix tree construction time: %f' % construction_time_cunsumed)

    start_time = time.time()
    search_result = tree.search_pattern(search_pattern)
    suffix_tree_search = time.time() - start_time
    print('suffix tree search time: %f' % suffix_tree_search)

    start_time = time.time()
    search_result = search_naive(input, search_pattern)
    search_time = time.time() - start_time
    delta = construction_time_cunsumed/(search_time - suffix_tree_search)
    print('naive search time: %f' % search_time)
    print('naive searches to eat construction: %f' % delta)

    start_time = time.time()
    search_result = search_ba(input, search_pattern)
    search_time = time.time() - start_time
    delta = construction_time_cunsumed/(search_time - suffix_tree_search)
    print('ba search time: %f' % search_time)
    print('ba searches to eat construction: %f' % delta)

    start_time = time.time()
    search_result = search_kmp(input, search_pattern)
    search_time = time.time() - start_time
    delta = construction_time_cunsumed/(search_time - suffix_tree_search)
    print('kmp search time: %f' % search_time)
    print('kmp searches to eat construction: %f' % delta)

def main():
    # print(simple_longest_border('aabcdeaab'))
    # print(border_array('aabcdaaecaabc'))
    # print(search_naive('mississippi', 'ssi'))
    # print(search_ba('mississippi', 'ssi'))
    # print(search_kmp('mississippi', 'ssi'))
    # experiments('project3/chr1_10000000.txt', 'project3/pattern5000.txt')
    # verify_naive_Onm()
    # naive_worstcase_test()
    # verify_search_correctness()
    # verify_running_time()
    compare_running_time()


if __name__ == '__main__':
    main()
    