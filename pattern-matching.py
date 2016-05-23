import time
import suffix_tree as st


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


def border_array(aString):
    ''' returns a list of length n of integers i, where each int i describes
        the longest border found in the string aString[0:i] '''
    ba = [0]
    n = len(aString)
    x = aString

    for i in range(1, n):
        b = ba[i - 1]  # -1 to convert i from one- to zero-indexed list index
        while b > 0 and x[i + 1 - 1] != x[b + 1 - 1]:  # -1's again to convert
            b = ba[b - 1]  # -1 again to convert
        if x[i + 1 - 1] == x[b + 1 - 1]:  # -1's again to convert
            ba.append(b + 1)
        else:
            ba.append(0)
    return ba


def search_naive(aString, aPattern):
    ''' finds occurrences of aPattern in aString in time O(nm) and returns
        a list of one-indexed occurrences of aPattern in aString '''
    n = len(aString) - 1
    m = len(aPattern) - 1
    s = aString
    p = aPattern
    occurrences = []
    for i in range(n):
        if s[i:i + m + 1] == p:
            # found a pattern match! append index to list of occurrences
            occurrences.append(i + 1)
    return occurrences


def search_ba(aString, aPattern):
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
    string = aPattern + '$' + aString  # length: n + 1 + m
    borderarr = border_array(string)   # complexity: ?
    occurrences = []
    for i, length in enumerate(borderarr):  # complexity: O(n)
        if length >= m:
            # adding 1 below to convert list zero-index to string one-index
            pattern_occurrence_idx = i - (2 * m) + 1
            occurrences.append(pattern_occurrence_idx)
    return occurrences


def search_kmp(aString, aPattern):
    occurrences = []

    # preprocessing:
    m = len(aPattern)
    n = len(aString)
    x = aString
    p = aPattern
    B = border_array(aPattern)
    Bm = [0]
    for j in range(2, m + 1 + 1):
        Bm.append(B[j - 1 - 1] + 1)
    
    # helper
    def match(i, j, m):
        while j <= m and x[i - 1] == p[j - 1]:
            i += 1
            j += 1
        return i, j

    # main:
    i, j = 1, 1
    while i <= n - m + j:
        i, j = match(i, j, m)
        if j == m + 1:
            # pattern found! 
            # subtract pattern length from current index and report this
            occurrences.append(i - m)
        if j == 1:
            i += 1
        else:
            j = Bm[j - 1]

    return occurrences


def verify_naive_Onm():

    # results:

    # marc@skodborg:~/Documents/AU/Git/string-algorithms$ python3 pattern-matching.py
    # p10 result median of 10 runs: 2.932652
    # [2.851702928543091, 2.8580031394958496, 2.8740298748016357, 2.908234119415283, 2.932651996612549, 2.9392731189727783, 2.954724073410034, 2.9603519439697266, 2.960646867752075, 2.978085994720459]

    # p100 result median of 10 runs: 2.991202
    # [2.940295934677124, 2.948166847229004, 2.9726250171661377, 2.9734160900115967, 2.9912021160125732, 2.9928479194641113, 2.99674391746521, 3.008416175842285, 3.008962869644165, 3.030972957611084]

    # p1000 result median of 10 runs: 3.830846
    # [3.8139729499816895, 3.8151941299438477, 3.826303005218506, 3.826917886734009, 3.830845832824707, 3.846817970275879, 3.8474650382995605, 3.8650670051574707, 3.872408151626587, 3.8835649490356445]

    # p10000 result median of 10 runs: 5.706376
    # [5.673080205917358, 5.696889162063599, 5.697651147842407, 5.7003090381622314, 5.70637583732605, 5.716675043106079, 5.717229127883911, 5.718000173568726, 5.722609043121338, 5.75190806388855]

    # p100000 result median of 3 runs: 56.763344
    # [56.70022010803223, 56.763344049453735, 56.80017900466919]

    # p1000000 result median of 3 runs: 721.457279
    # [720.9139211177826, 721.4572789669037, 722.2307889461517]


    # tag faktiske kørselstider for forskellige m og sammenlign i graf
    # med O(nm) ved at plotte kørselstid/(n*m) for forskellige m
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

    p10_times = []
    for _ in range(10):
        start_time = time.time()
        # search_naive(input, p10)
        search_ba(input, p10)
        # search_kmp(input, p10)
        end_time = time.time()
        p10_times.append(end_time - start_time)
    p10_times.sort()
    print('p10 result median of 10 runs: %f' % p10_times[4])
    print(p10_times)
    print()

    p20_times = []
    for _ in range(10):
        start_time = time.time()
        # search_naive(input, p20)
        search_ba(input, p20)
        # search_kmp(input, p20)
        end_time = time.time()
        p20_times.append(end_time - start_time)
    p20_times.sort()
    print('p20 result median of 20 runs: %f' % p20_times[4])
    print(p20_times)
    print()

    p30_times = []
    for _ in range(10):
        start_time = time.time()
        # search_naive(input, p30)
        search_ba(input, p30)
        # search_kmp(input, p30)
        end_time = time.time()
        p30_times.append(end_time - start_time)
    p30_times.sort()
    print('p30 result median of 30 runs: %f' % p30_times[4])
    print(p30_times)
    print()

    p40_times = []
    for _ in range(10):
        start_time = time.time()
        # search_naive(input, p40)
        search_ba(input, p40)
        # search_kmp(input, p40)
        end_time = time.time()
        p40_times.append(end_time - start_time)
    p40_times.sort()
    print('p40 result median of 40 runs: %f' % p40_times[4])
    print(p40_times)
    print()

    p50_times = []
    for _ in range(10):
        start_time = time.time()
        # search_naive(input, p50)
        search_ba(input, p50)
        # search_kmp(input, p50)
        end_time = time.time()
        p50_times.append(end_time - start_time)
    p50_times.sort()
    print('p50 result median of 50 runs: %f' % p50_times[4])
    print(p50_times)
    print()

    p100_times = []
    for _ in range(10):
        start_time = time.time()
        # search_naive(input, p100)
        search_ba(input, p100)
        # search_kmp(input, p100)
        end_time = time.time()
        p100_times.append(end_time - start_time)
    p100_times.sort()
    print('p100 result median of 10 runs: %f' % p100_times[4])
    print(p100_times)
    print()

    p500_times = []
    for _ in range(10):
        start_time = time.time()
        # search_naive(input, p500)
        search_ba(input, p500)
        # search_kmp(input, p500)
        end_time = time.time()
        p500_times.append(end_time - start_time)
    p500_times.sort()
    print('p500 result median of 10 runs: %f' % p500_times[4])
    print(p500_times)
    print()

    p1000_times = []
    for _ in range(10):
        start_time = time.time()
        # search_naive(input, p1000)
        search_ba(input, p1000)
        # search_kmp(input, p1000)
        end_time = time.time()
        p1000_times.append(end_time - start_time)
    p1000_times.sort()
    print('p1000 result median of 10 runs: %f' % p1000_times[4])
    print(p1000_times)
    print()

    p5000_times = []
    for _ in range(10):
        start_time = time.time()
        # search_naive(input, p5000)
        search_ba(input, p5000)
        # search_kmp(input, p5000)
        end_time = time.time()
        p5000_times.append(end_time - start_time)
    p5000_times.sort()
    print('p5000 result median of 10 runs: %f' % p5000_times[4])
    print(p5000_times)
    print()

    p10000_times = []
    for _ in range(5):
        start_time = time.time()
        # search_naive(input, p10000)
        search_ba(input, p10000)
        # search_kmp(input, p10000)
        end_time = time.time()
        p10000_times.append(end_time - start_time)
    p10000_times.sort()
    print('p10000 result median of 10 runs: %f' % p10000_times[2])
    print(p10000_times)
    print()

    p50000_times = []
    for _ in range(5):
        start_time = time.time()
        # search_naive(input, p50000)
        search_ba(input, p50000)
        # search_kmp(input, p50000)
        end_time = time.time()
        p50000_times.append(end_time - start_time)
    p50000_times.sort()
    print('p50000 result median of 10 runs: %f' % p50000_times[2])
    print(p50000_times)
    print()

    p100000_times = []
    for _ in range(3):
        start_time = time.time()
        # search_naive(input, p100000)
        search_ba(input, p100000)
        # search_kmp(input, p100000)
        end_time = time.time()
        p100000_times.append(end_time - start_time)
    p100000_times.sort()
    print('p100000 result median of 3 runs: %f' % p100000_times[1])
    print(p100000_times)
    print()

    p500000_times = []
    for _ in range(3):
        start_time = time.time()
        # search_naive(input, p500000)
        search_ba(input, p500000)
        # search_kmp(input, p500000)
        end_time = time.time()
        p500000_times.append(end_time - start_time)
    p500000_times.sort()
    print('p500000 result median of 3 runs: %f' % p500000_times[1])
    print(p500000_times)
    print()

    p1000000_times = []
    for _ in range(3):
        start_time = time.time()
        # search_naive(input, p1000000)
        search_ba(input, p1000000)
        # search_kmp(input, p1000000)
        end_time = time.time()
        p1000000_times.append(end_time - start_time)
    p1000000_times.sort()
    print('p1000000 result median of 3 runs: %f' % p1000000_times[1])
    print(p1000000_times)
    print()


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

def main():
    # print(simple_longest_border('aabcdeaab'))
    # print(border_array('aabcdaaecaabc'))
    # print(search_naive('mississippi', 'ssi'))
    # print(search_ba('mississippi', 'ssi'))
    # print(search_kmp('mississippi', 'ssi'))
    # experiments('project3/chr1_10000000.txt', 'project3/pattern5000.txt')
    verify_naive_Onm()


if __name__ == '__main__':
    main()
