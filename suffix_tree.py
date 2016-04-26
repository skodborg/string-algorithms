#!/usr/bin/env python
from itertools import count
import os.path
import argparse
import time


# TODO: parentEdge should be pointers into input string instead
class Tree:
    def _commonprefix(self, str1, str2):
        return os.path.commonprefix([str1, str2])

    def _findchildwithLCP(self, aNode, aString):
        for child in aNode.children:
            curr_parentEdge = child.parentEdge
            this_prefix = self._commonprefix(curr_parentEdge, aString)

            if this_prefix:
                return child, this_prefix
        return None, ''

    def _constructsuffixtree(self):
        # iterate through each suffix of the string and insert each one
        last_idx = len(self.input)
        for i in range(len(self.input)):
            suffix_str_idx = i + 1
            curr_suffix = self.input[i:last_idx]
            curr_node = self.root

            child, shared_prefix = self._findchildwithLCP(curr_node, curr_suffix)

            while shared_prefix and shared_prefix == child.parentEdge:
                curr_suffix = curr_suffix[len(shared_prefix):]
                curr_node = child
                child, shared_prefix = self._findchildwithLCP(child, curr_suffix)

            if not shared_prefix:
                # no common prefix found, insert this prefix below root
                new_child = Node(suffix_str_idx, curr_node, curr_suffix)
                curr_node.add_child(new_child)
            else:
                # splitting up existing edge where new suffix is to branch
                head = shared_prefix
                tail = child.parentEdge[len(head):]

                # create and insert intermediate node
                new_node = Node(0, curr_node, head)
                curr_node.add_child(new_node)
                curr_node.remove_child(child)
                new_node.add_child(child)

                # update old child to point to new intermediate node
                child.parent = new_node
                child.parentEdge = tail

                # create and insert new leaf node with the new suffix
                new_leaf = Node(suffix_str_idx, new_node, curr_suffix[len(head):])
                new_node.add_child(new_leaf)

    def find_leaf_descendants(self, aNode):
        leafnode_list = []
        if len(aNode.children) == 0:
            # base case; aNode has no children, return itself as it is a leaf
            return [aNode]
        else:
            # rec. case; aNode has children, return all their leaf descendants
            for c in aNode.children:
                recursive_leafnodes_list = self.find_leaf_descendants(c)
                leafnode_list.append(recursive_leafnodes_list)
            # flatten before return; should not be list-of-lists, just a list
            flat_leaf_list = [i for sublist in leafnode_list for i in sublist]
            return flat_leaf_list

    def search_pattern(self, aPattern):
        ''' returns a list of indices at which the given pattern can be found
            in the string the suffix tree is based upon, or an empty list if
            the pattern does not occur anywhere '''

        def recursive_node_traversal(aNode, aPattern):
            for child in aNode.children:
                shared_prefix = self._commonprefix(aPattern, child.parentEdge)
                if len(shared_prefix) == 0:
                    # this child and its subtree does not contain our search
                    continue
                elif aPattern == shared_prefix:
                    # Pattern is matched! All leaf nodes below this child
                    # contains the searched pattern; return id of these
                    leaf_nodes = self.find_leaf_descendants(child)
                    leaf_node_indices = [node.id for node in leaf_nodes]
                    return leaf_node_indices

                elif len(shared_prefix) < len(aPattern):
                    # part of the pattern was matched, keep looking recursively
                    # for the remaining pattern
                    remaining_pattern = aPattern[len(shared_prefix):]
                    leaf_nodes_indices = recursive_node_traversal(child, remaining_pattern)
                    return leaf_nodes_indices
            # pattern was never fully matched, return empty list
            return []

        # traverse tree from root node, looking for aPattern
        result = recursive_node_traversal(self.root, aPattern)
        # sort results before return
        result.sort()
        return result

    def __init__(self, aInput):
        self.root = Node(0, None)
        self.input = aInput + "$"
        # construct tree
        self._constructsuffixtree()

    def __str__(self):
        return str(self.root)


def read_input(aFile):
    f = open(aFile, 'r', encoding='latin1')
    return f.read()


def write_output(aFile, aString):
    f = open(aFile, 'w')
    f.write(aString)


def print_list(aList):
    ''' given a list of ints, print the integer elements
        separated by spaces '''
    print(' '.join(map(str, aList)))


class Node:
    _ids = count(0)

    def add_child(self, new_child):
        self.children.append(new_child)

    def remove_child(self, old_child):
        self.children.remove(old_child)

    def is_leaf(self):
        return len(self.children) == 0

    def __init__(self, aId, aParent, aParentEdge=''):
        self.graphid = next(self._ids)
        self.id = aId
        self.parent = aParent
        self.parentEdge = aParentEdge
        self.children = []


def main():
    parser = argparse.ArgumentParser()
    input_helptxt = "File containing text to build a suffix tree over"
    searchterm_helptxt = "Character sequence to search for in the input text"
    parser.add_argument("input", help=input_helptxt)
    parser.add_argument("searchterm", help=searchterm_helptxt)
    args = parser.parse_args()

    inputfile = args.input
    searchterm = args.searchterm
    # outputfile = inputfile.replace('.txt', '.out')

    input_str = read_input(inputfile)
    start_time = time.time()
    tree = Tree(input_str)
    print('construction time: %s' % (time.time() - start_time))
    start_time = time.time()
    search_result = tree.search_pattern(searchterm)
    print('searching time: %s' % (time.time() - start_time))
    # write_output(outputfile, search_result)

    # print(tree.search_pattern(searchterm))
    print_list(search_result)

if __name__ == '__main__':
    main()
