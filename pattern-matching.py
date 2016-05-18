# import suffix_tree as suffix


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
    pass


def main():
    # print(simple_longest_border('aabcdeaab'))
    # print(search_naive('mississippi', 'ss'))
    # print(border_array('aabcdaaecaabc'))
    print(search_ba('mississippi', 'ss'))

if __name__ == '__main__':
    main()
