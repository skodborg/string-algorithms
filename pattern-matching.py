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


def main():
    print(simple_longest_border('aabcdeaab'))

if __name__ == '__main__':
    main()
