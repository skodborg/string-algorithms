from itertools import count
import os.path
import pydotplus as pydot

TESTSTRING = "Mississippi"
TEST = "tatat"


class Tree:
    def visualize(self):
        self.graph = pydot.Dot(graph_type='graph')
        self.root.visualize(self.graph)
        self.graph.write_png('example1_graph.png')
    
    def common_prefix(self, str1, str2):
        return os.path.commonprefix([str1, str2])

    def find_child_with_common_prefix(self, aNode, aString):
        for child in aNode.children:
            curr_parentEdge = child.parentEdge
            this_prefix = self.common_prefix(curr_parentEdge, aString)
            if this_prefix:
                return child, this_prefix
        return None, ''

    def construct_suffix_tree(self):
        # iterate through each suffix of the string and insert each one
        last_idx = len(self.input)
        for i in range(len(self.input)):
            curr_suffix = self.input[i:last_idx]
            curr_node = self.root
            
            child, shared_prefix = self.find_child_with_common_prefix(curr_node, curr_suffix)

            if not shared_prefix:
                # no common prefix found, insert this prefix below root
                new_child = Node(self.root, curr_suffix)
                curr_node.add_child(new_child)

            # TODO: HANDLE SHARED PREFIX WITH AN EXISTING CHILD

    def __init__(self, aInput):
        self.root = Node(None)
        self.input = aInput + "$"
        # construct tree
        self.construct_suffix_tree()

    def __str__(self):
        return str(self.root)


class Node:
    _ids = count(0)

    def add_child(self, new_child):
        self.children.append(new_child)

    def remove_child(self):
        print("TODO")

    def is_leaf(self):
        return len(self.children) == 0

    def __init__(self, parent, parentEdge=''):
        self.id = next(self._ids)
        self.parent = parent
        self.parentEdge = parentEdge
        self.children = []

    def __str__(self):
        # return "NODE-%i   parent:%s   p.Edge:%s   children:%s" % (self.id, \
        #     self.parent, self.parentEdge, self.children)
        result = ''
        for c in self.children:
            result += c.parentEdge + ' - '
        return result
    
    def visualize(self, graph):
        if self.parent is not None:
            edge = pydot.Edge(self.parent.id, self.id, label=self.parentEdge)
            graph.add_edge(edge)
            
        for c in self.children:
            c.visualize(graph)


# def construct_suffix_tree(aString):
#     """ returns a suffix tree of the given string,
#         constructed naively in time O(n^2) """
#     # iterate through each suffix of the string and insert each one
#     last_idx = len(aString)
#     for i in range(len(aString)):
#         curr_suffix = aString[i:last_idx]
#         print(curr_suffix)


def main():
    # initialize suffix tree
    tree = Tree(TEST)
    
    print(tree)
    tree.visualize()

if __name__ == '__main__':
    main()
