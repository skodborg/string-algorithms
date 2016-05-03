import suffix_tree as suffix
import visualize_suffix_tree as vst


def basic_tandemrepeat(aTree):
    all_treenodes = []
    aTree.traverse(lambda x: all_treenodes.append(x))
    for v in all_treenodes:
        # step 1: mark node v
        v.marked = True

        # step 2a:
        v_leaflist = v.leaflist()

        # step 2b:
        Lv = v.path()  # L(v), the path-label of v, labels concat'ed from root
        Dv = len(Lv)  # D(v), the string-depth of v
        for i in v_leaflist:
            j = i.id + Dv
            # test whether leaf j is in v_leaflist
            # i.e. whether any of the nodes in v's leaflist has an id == j
            test1 = any(n.id == j for n in v_leaflist)

            if test1:
                # print('%i:  %s is a tandem repeat!' % (i.id, Lv + Lv))
                S = aTree.input
                test2 = S[i.id - 1] != S[i.id + (2 * Dv) - 1]

                if test1 and test2:
                    print("branching tandem repeat at %i: %s" % (i.id, S[i.id-1:i.id+2*Dv-1]))



def main():
    input = 'mississippi'
    tree = suffix.Tree(input)
    # ll = tree.root.leaflist()
    # for c in ll:
    #     print(c.id)
    # print('len: %i' % len(ll))
    # tree.traverse(lambda x: print('%i: %s' % (x.id, x.path())))
    basic_tandemrepeat(tree)
    # vst.visualize(tree.root).write_png('tandem.png')

if __name__ == '__main__':
    main()
