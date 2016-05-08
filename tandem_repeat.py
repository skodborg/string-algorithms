import suffix_tree as suffix
import visualize_suffix_tree as vst
import time
import argparse


def basic_tandemrepeat(aTree):
    branching = set()
    nonbranching = set()

    all_treenodes = []
    aTree.traverse(lambda x: all_treenodes.append(x))
    S = aTree.input
    for v in all_treenodes:
        # step 1: mark node v
        v.marked = True

        # step 2a:
        v_leaflist = v.leaflist()

        # step 2b:
        Lv = v.path   # L(v), concatenating all edge strings from root to v
        Dv = len(Lv)  # D(v), the string-depth of v
        for i in v_leaflist:
            j = i.id + Dv
            # test whether leaf j is in v_leaflist
            # i.e. whether any of the nodes in v's leaflist has an id == j
            test1 = any(n.id == j for n in v_leaflist)

            if test1:
                test2 = S[i.id - 1] != S[i.id + (2 * Dv) - 1]

                if test1 and test2:
                    # found branching tandem repeat!
                    start_idx = i.id - 1
                    tandem_length = 2 * Dv
                    branchingtandem = S[start_idx: start_idx + tandem_length]
                    branching.add((start_idx, branchingtandem))

                    k = i.id - 1
                    while S[k - 1] == S[k + (2 * Dv) - 1]:
                        # found non-branching tandem repeat!
                        start_idx = k - 1
                        tandem_length = 2 * Dv
                        nonbranchingtandem = S[k - 1: k + (2 * Dv) - 1]
                        nonbranching.add((k, nonbranchingtandem))
                        k -= 1

    return list(branching), list(nonbranching)


def dfs_preprocess(suffixtree):
    ''' returns a list of all leaf nodes as they are discovered
        by a depth-first search through the tree. Also mutates
        intermediate nodes in the suffix tree by adding start-
        and end-properties specifying intervals in the returned
        list which defines the leaflist of this particular node '''
    dfs = []

    def dfs_recursive_traverse(aNode):
        # depth-first, from left to right
        if len(aNode.children) == 0:
            # leaf discovered, insert in dfs and
            # point to self in dfs with leaflist-properties
            aNode.leaflist_start = aNode.leaflist_end = len(dfs)
            dfs.append(aNode)
        else:
            # intermediate node, add start- and end-properties
            # start points at next leaf discovered in subtree
            aNode.leaflist_start = len(dfs)
            for child in aNode.children:
                dfs_recursive_traverse(child)
            # end points at last leaf discovered in subtree
            aNode.leaflist_end = len(dfs) - 1
    dfs_recursive_traverse(suffixtree.root)
    return dfs


def optimized_tandemrepeat(aTree):
    dfs = dfs_preprocess(aTree)

    branching = set()
    nonbranching = set()

    all_treenodes = []
    aTree.traverse(lambda node: all_treenodes.append(node))
    for v in all_treenodes:
        if v.is_leaf():
            # leaf node, we're only interested in internal nodes for now
            continue

        # step 1: mark node v
        v.marked = True

        # step 2a: collect LL'(v)
        # LL'(v) = LL(v) - LL(v')
        LLv = (v.leaflist_start, v.leaflist_end)  # indexes in dfs
        LLv_actual = dfs[LLv[0]:LLv[1] + 1]       # corresponding actual nodes

        # gather leaflist of all children
        LLvm = [(c.leaflist_start,
                 c.leaflist_end,
                 c.leaflist_end - c.leaflist_start + 1)
                for c in v.children]
        # find largest leaflist spanning the most nodes among children nodes
        LLvm = max(LLvm, key=lambda x: x[2])
        # grab the nodes contained in this largest leaf set
        LLvm = LLvm[0:2]

        # find elements in LLv but not in LLvm
        LLmv = list(set(range(LLv[0], LLv[1] + 1)) -
                    set(range(LLvm[0], LLvm[1] + 1)))
        # convert from lsit of dfs indexes to list of actual nodes
        LLmv = [dfs[i] for i in LLmv]

        Dv = len(v.path)
        S = aTree.input
        for i in LLmv:
            j = i.id + Dv
            test1 = any(n.id == j for n in LLv_actual)

            if test1:
                test2 = S[i.id - 1] != S[i.id + (2 * Dv) - 1]

                if test1 and test2:
                    branching.add((i.id, S[i.id - 1: i.id + (2 * Dv) - 1]))

                    k = i.id - 1
                    while S[k - 1] == S[k + (2 * Dv) - 1]:
                        # found non-branching tandem repeat!
                        nonbranching.add((k, S[k - 1: k + (2 * Dv) - 1]))
                        k -= 1

        for j in LLmv:
            i = j.id - Dv
            test1 = any(n.id == i for n in LLv_actual)

            if test1:
                test2 = S[i - 1] != S[i + (2 * Dv) - 1]

                if test1 and test2:
                    branching.add((i, S[i - 1: i + (2 * Dv) - 1]))

                    k = i - 1
                    while S[k - 1] == S[k + (2 * Dv) - 1]:
                        # found non-branching tandem repeat!
                        nonbranching.add((k, S[k - 1: k + (2 * Dv) - 1]))
                        k -= 1

    return list(branching), list(nonbranching)


def exp():
    N = 10000000
    s = set()
    l = []
    pl = [None] * N
    rng = range(0, N)
    start_time = time.time()
    for i in rng:
        pass
    end = time.time()
    print("--- %s seconds ---" % (end - start_time))
    start_time = time.time()
    for i in rng:
        s.add(i)
    end = time.time()
    print("--- %s seconds ---" % (end - start_time))
    start_time = time.time()
    for i in rng:
        l.append(i)
    end = time.time()
    print("--- %s seconds ---" % (end - start_time))
    start_time = time.time()
    for i in rng:
        pl[i] = i
    end = time.time()
    print("--- %s seconds ---" % (end - start_time))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--basic', action='store_true',
                        help='use the basic algorithm instead of the '
                             'optimized one')
    parser.add_argument('-v', '--visualize', type=str,
                        metavar='FILE',
                        help='draws the suffix tree to the file specified')
    parser.add_argument('file',
                        help='file in which to find tandem repeats')
    args = parser.parse_args()

    inputfile = args.file
    alg_choice = args.basic
    visualize_choice = args.visualize

    # input = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    # input = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    input = suffix.read_input(inputfile)
    tree = suffix.Tree(input)

    if alg_choice:
        branching, nonbranching = basic_tandemrepeat(tree)
        print('%i %i' % (len(branching), len(nonbranching)))
    else:
        branching, nonbranching = optimized_tandemrepeat(tree)
        print('%i %i' % (len(branching), len(nonbranching)))

    if visualize_choice:
        vst.visualize(tree.root).write_png(visualize_choice)


if __name__ == '__main__':
    main()
