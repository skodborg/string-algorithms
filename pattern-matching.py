import time


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
    experiments('project3/chr1_10000000.txt', 'project3/pattern5000.txt')


if __name__ == '__main__':
    main()
