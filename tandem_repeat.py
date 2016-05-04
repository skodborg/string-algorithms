import suffix_tree as suffix
import visualize_suffix_tree as vst
import time


def basic_tandemrepeat(aTree):
    branching = []
    nonbranching = []

    all_treenodes = []
    aTree.traverse(lambda x: all_treenodes.append(x))
    S = aTree.input
    for v in all_treenodes:
        # step 1: mark node v
        v.marked = True

        # step 2a:
        start_time = time.time()
        v_leaflist = v.leaflist()

        # step 2b:
        print('\nbasic step 2b')
        start_time = time.time()
        Dv = len(v.path)  # D(v), the string-depth of v
        for i in v_leaflist:
            j = i.id + Dv
            # test whether leaf j is in v_leaflist
            # i.e. whether any of the nodes in v's leaflist has an id == j
            test1 = any(n.id == j for n in v_leaflist)
            
            if test1:
                # print('%i:  %s is a tandem repeat!' % (i.id, Lv + Lv))
                test2 = S[i.id - 1] != S[i.id + (2 * Dv) - 1]

                if test1 and test2:
                    # found branching tandem repeat!
                    start_idx = i.id - 1
                    tandem_length = 2 * Dv
                    branchingtandem = S[start_idx: start_idx + tandem_length]
                    branching.append(branchingtandem)

                    k = i.id - 1
                    while S[k - 1] == S[k + (2 * Dv) - 1]:
                        # found non-branching tandem repeat!
                        start_idx = k - 1
                        tandem_length = 2 * Dv
                        nonbranchingtandem = S[k - 1: k + (2 * Dv) - 1]
                        nonbranching.append(nonbranchingtandem)
                        k -= 1
        print("--- %s seconds ---" % (time.time() - start_time))

    print('%i %i' % (len(branching), len(nonbranching)))
    # print(str([s for s in branching]) + str([s for s in nonbranching]))


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
            # leaf discovered, insert in dfs
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
    
    # just counting, as saving requires a linked-list impl. for constant time
    branching = set()
    nonbranching = set()

    all_treenodes = []
    aTree.traverse(lambda node: all_treenodes.append(node))
    for v in all_treenodes:
        if not hasattr(v, 'leaflist_start'):
            # leaf node, we're only interested in internal nodes for now
            continue

        # step 1: mark node v
        v.marked = True
        
        print('\noptimized step 2a')
        start_time = time.time()
        # step 2a: collect LL'(v)
        # LL'(v) = LL(v) - LL(v')
        LLv = (v.leaflist_start, v.leaflist_end)
        LLv_actual = dfs[LLv[0]:LLv[1]+1]   
        # print(str(LLv) + '   ' + str([n.id for n in LLv_actual]))

        LLvm = [(c.leaflist_start, c.leaflist_end, c.leaflist_end - c.leaflist_start + 1) for c in v.children if hasattr(c, 'leaflist_start') and c]
        if not LLvm:
            # LLvm = LLv_actual[0]
            LLmv = LLv_actual[1:len(v.children)]
            # LLmv = LLv_actual[0:len(v.children)]
        else:
            LLvm = max(LLvm, key=lambda x: x[2]) if LLvm else []
            LLvm = LLvm[0:2]
            
            LLmv = list(set(range(LLv[0], LLv[1]+1)) - set(range(LLvm[0], LLvm[1]+1)))
            LLmv = [dfs[i] for i in LLmv]

        print("--- %s seconds ---" % (time.time() - start_time))

        print('\noptimized step 2b')
        Dv = len(v.path)
        S = aTree.input
        for i in LLmv:
            j = i.id + Dv
            test1 = any(n.id == j for n in LLv_actual)
            
            if test1:
                test2 = S[i.id - 1] != S[i.id + (2 * Dv) - 1]
                
                if test1 and test2:
                    branching.add((i.id, S[i.id - 1: i.id + (2*Dv)-1]))
                    
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
                    branching.add((i, S[i - 1: i + (2*Dv)-1]))
                    
                    k = i - 1
                    while S[k - 1] == S[k + (2 * Dv) - 1]:
                        # found non-branching tandem repeat!
                        nonbranching.add((k, S[k - 1: k + (2 * Dv) - 1]))
                        k -= 1
        print("--- %s seconds ---" % (time.time() - start_time))
                
    print('%i %i' % (len(branching), len(nonbranching)))
    
    
def exp():
    N = 10000000
    s = set()
    l = []
    pl = [None] * N
    rng = range(0,N)
    start_time = time.time()
    for i in rng:
        # s.add(i)
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
    
    input = 'mississippi'
    # input = 'abaababaabaababaababaabaababaabaababaababaabaababaababaabaababaabaababaababaabaababaabaab'
    # input = 'cagaatgacatcccaggattacataaactgtcagaggcagccgaagagttcacaagtgtgaagcctggaagccggcgggtgccgctgtgtaggaaagaagctaaagcacttccagagcctgtccggagctcagaggttcggaagacttatcgaccatggtgagtgtagggtcttggggtcgaacgcgtgccactcgggagccacaggggttggatggggcctcctagacctctgctctctccccaggagcgcgcgtcctgcttgttgctgctgctgctgccgctggtgcacgtctctgcgaccacgccagaaccttgtgagctggacgatgaagatttccgctgcgtctgcaacttctccgaacctcagcccgactggtccgaagccttccagtgtgtgtctgcagtagaggtggagatccatgccggcggtctcaacctagagccgtttctaaagcgcgtcgatgcggacgccgacccgcggcagtatgctgacacggtcaaggctctccgcgtgcggcggctcacagtgggagccgcacaggttcctgctcagctactggtaggcgccctgcgtgtgctagcgtactcccgcctcaaggaactgacgctcgaggacctaaagataaccggcaccatgcctccgctgcctctggaagccacaggacttgcactttccagcttgcgcctacgcaacgtgtcgtgggcgacagggcgttcttggctcgccgagctgcagcagtggctcaagccaggcctcaaggtactgagcattgcccaagcacactcgcctgccttttcctacgaacaggttcgcgccttcccggcccttaccagcctagacctgtctgacaatcctggactgggcgaacgcggactgatggcggctctctgtccccacaagttcccggccatccagaatctagcgctgcgcaacacaggaatggagacgcccacaggcgtgtgcgccgcactggcggcggcaggtgtgcagccccacagcctagacctcagccacaactcgctgcgcgccaccgtaaaccctagcgctccgagatgcatgtggtccagcgccctgaactccctcaatctgtcgttcgctgggctggaacaggtgcctaaaggactgccagccaagctcagagtgctcgatctcagctgcaacagactgaacagggcgccgcagcctgacgagctgcccgaggtggataacctgacactggacgggaatcccttcctggtccctggaactgccctcccccacgagggctcaatgaactccggcgtggtcccagcctgtgcacgttcgaccctgtcggtgggggtgtcgggaaccctggtgctgctccaaggggcccggggctttgcctaagatccaagacagaataatgaatggactcaaactgccttggcttcaggggagtcccgtcaggacgttgaggacttttcgaccaattcaaccctttgccccacctttattaaaatcttaaacaacggttccgtgtcattcatttaacagacctttattggatgtctgctatgtgctgggcacagtactggatggggaattc'
    # input = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    # input = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    input = 'ctgcgccctccggccgccggtggccctctgtgcggtgggggaaggggtcgacgtggctcagctttttggattcagggagctcgggggtgggaagagagaaatggagttccaggggcgtaaaggagagggagttcgccttccttcccttcctgagactcaggagtgactgcttctccaatcctcccaagcccaccactccacacgactccctcttcccggtagtcgcaagtgggagtttggggatctgagcaaagaacccgaagaggagttgaaatattggaagtcagcagtcaggcaccttcccgagcgcccagggcgctcagagtggacatggttggggaggcctttgggacaggtgcggttcccggagcgcaggcgcacacatgcacccaccggcgaacgcggtgaccctcgccccaccccatcccctccggcgggcaactgggtcgggtcaggaggggcaaacccgctagggagacactccatatacggcccggcccgcgttacctgggaccgggccaacccgctccttctttggtcaacgcaggggacccgggcgggggcccaggccgcgaaccggccgagggagggggctctagtgcccaacacccaaatatggctcgagaagggcagcgacattcctgcggggtggcgcggagggaatcgcccgcgggctatataaaacctgagcagagggacaagcggccaccgcagcggacagcgccaagtgaagcctcgcttcccctccgcggcgaccagggcccgagccgagagtagcagttgtagctacccgcccaggtagggcaggagttgggaggggacagggggacagggcactaccgaggggaacctgaaggactccggggcagaacccagtcggttcacctggtcagccccaggcctcgccctgagcgctgtgcctcgtctccggagccacacgcgctttaaaaaggaggcaagacagtcagcctctggaaattagacttctccaaatttttctctagccctttgggctcctttacctggcatgtaggatgtgcctagggagataaacggttttgctttagttgtcgccaaggcagttcccttccaaactagcgctagagcgaatgagcgagcagccaggaccaccattctgggtttccaacaggcgaaaaggccctttctgagtttgaaatgtcacagggttcctaacaggccactcttccctggatggggtgccaacgcctttcccatgggcatctccttccaccctcacgctggcccagcaagcaggcagtgctgaggccttatctccctaggtgacagatgtggtcagggaggcgcagagaggatgggcactagcgtccagctcctggaacaggtgtcaggcagggagggcagacaggtcttgggaacatgttcccctggctatgtggacagaggacttctcagtgggtctcgcgaccctgtgccccttttcctggttcagggcagccttagccggggcaaaggtcgagaagagaacccctggtcgccgccctggcagaatttgagtggctccggcaggagatgtccctaggttcctggggagggaggacgtcggggccagccaggcttacccccccctgccgctgagacttctgcgctgatgcacgcgcctcttcgcggtctccctgtccttgcagaaactagacacaatgtgcgacgaagacgagaccaccgccctcgtgtgcgacaatggctccggcctggtgaaagccggcttcgccggggatgacgcccctagggccgtgttcccgtccatcgtgggccgcccccgacaccaggtcaggctgcccctccgcagagggagccggctcggggtccccgcgtaagccagcctggtgccacccggagcggcgttaacgggtgcgtggtgtctcggctctgcagggcgtcatggtcggtatgggtcagaaagattcctacgtgggcgacgaggctcagagcaagagaggtatcctgaccctgaagtaccctatcgagcacggcatcatcaccaactgggatgacatggagaagatctggcaccacaccttctacaacgagcttcgcgtggctcccgaggagcaccccaccctgctcaccgaggcccccctcaatcccaaggccaaccgcgagaagatgacccagatcatgtttgagaccttcaacgtgcccgccatgtacgtggccatccaggccgtgctgtccctctacgcctccggaaggaccaccggtgagtgcccgctggcccccagtcccctcgtcccgcccccgcccccgcccccgcccccggccgctagcgctgagcgcctagcctcggcctcgcccccagccactcactctctcccgcgcgcgcacaggcatcgtgctggactccggcgacggcgtcacccacaacgtgcccatttatgagggctacgcgctgccgcacgccatcatgcgcctggacctggcgggccgcgatctcaccgactacctgatgaagatcctcactgagcgtggctactccttcgtgaccacaggtgcgcggcgcccctgcacccgggcggagggccgcggcggcctgagtgagggctcctctcctgcttctgccctccgcagctgagcgcgagatcgtgcgcgacatcaaggagaagctgtgctacgtggccctggacttcgagaacgagatggcgacggccgcctcctcctcctccctggaaaagagctacgagctgccagacgggcaggtcatcaccatcggcaacgagcgcttccgctgcccggagacgctcttccagccctccttcatcggtgagccccgctcgccctcgccccggcccccaggcccgcgccccccggcccgagcttctgctcacgctccccgccgcggtccccaggtatggagtcggcgggcattcacgagaccacctacaacagcatcatgaagtgtgacatcgacatcaggaaggacctgtatgccaacaacgtcatgtcggggggcaccacgatgtaccctgggatcgctgaccgcatgcagaaagagatcaccgcgctggcacccagcaccatgaagatcaaggtgggtggtggcctgcgcgggctgtcggcggggtgggctccagggtgaggtctccccacctcacgcgctgtcttgcagatcatcgccccgccggagcgcaaatactcggtgtggatcggcggctccatcctggcctcgctgtccaccttccagcagatgtggatcaccaagcaggagtacgacgaggccggcccttccatcgtccaccgcaaatgcttctagacacactccacctccagcacgcgacttctcaggacgacgaatcctctcaatgggggggcggctgagctccagccaccccgcagtcactttctttgtaacaactttccgttgctgccatcgtaaactgacacagtgtttataacgtgtacatacattaacttattacctcattttgttatttttcgaaacaaagccctgtggaagaaaatggaaaacttgaagaagcattaaagtcattctgttaagctgcgtaaagtggtcgtgtttatttgcttggggcgggagtggagcaggaagagggattcccatcccccacatcctcttaagtcacttttcacgataccccaaatgaatgggctccttggaagacaaaacttacatcttcccatgctccctgccggtttctgcagtggatcagatccattccagatcactggcagctagtggtggcctgacttgacctctggggtgtggcgaggcgagctttct'
    tree = suffix.Tree(input)
    start_time = time.time()
    basic_tandemrepeat(tree)
    end = time.time()
    basic_diff = end - start_time
    # print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    optimized_tandemrepeat(tree)
    end = time.time()
    opt_diff = end - start_time
    # print("--- %s seconds ---" % (time.time() - start_time))
    # vst.visualize(tree.root).write_png('tandem.png')
    print('--- basic: %s \n --- optimized: %s' % (basic_diff, opt_diff))
    

if __name__ == '__main__':
    main()
