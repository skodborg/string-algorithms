from itertools import count
import os.path
import pydotplus as pydot

TESTSTRING = "mississippi"
# TESTSTRING = 'adabadcade'



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

            while shared_prefix and shared_prefix == child.parentEdge:
                curr_suffix = curr_suffix[len(shared_prefix):]
                curr_node = child
                child, shared_prefix = self.find_child_with_common_prefix(child, curr_suffix)


            if not shared_prefix:
                # no common prefix found, insert this prefix below root
                new_child = Node(curr_node, curr_suffix)
                curr_node.add_child(new_child)
            else:
                # splitting up existing edge where new suffix is to branch
                head = shared_prefix
                tail = child.parentEdge[len(head):]

                # create and insert intermediate node
                new_node = Node(curr_node, head)
                curr_node.add_child(new_node)
                curr_node.remove_child(child)
                new_node.add_child(child)

                # update old child to point to new intermediate node
                child.parent = new_node
                child.parentEdge = tail

                # create and insert new leaf node with the new suffix
                new_leaf = Node(new_node, curr_suffix[len(head):])
                new_node.add_child(new_leaf)


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

    def remove_child(self, old_child):
        self.children.remove(old_child)

    def is_leaf(self):
        return len(self.children) == 0

    def __init__(self, parent, parentEdge=''):
        self.id = next(self._ids)
        self.parent = parent
        self.parentEdge = parentEdge
        self.children = []

    def __str__(self):
        return "NODE-%i   parent:%s   p.Edge:%s   children:%s" % (self.id, \
            self.parent, self.parentEdge, self.children)
    
    def visualize(self, graph):
        if self.parent is not None:
            edge = pydot.Edge(self.parent.id, self.id, label=self.parentEdge)
            graph.add_edge(edge)
            
        for c in self.children:
            c.visualize(graph)


def main():
    # initialize suffix tree
    tree = Tree(TESTSTRING)

    tree.visualize()

if __name__ == '__main__':
    main()
