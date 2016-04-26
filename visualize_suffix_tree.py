import pydotplus as pydot
import argparse
import suffix_tree


def visualize(aTree):
    def traverse(aNode, graph):
        node_lbl = aNode.id if aNode.id > 0 else ''
        graph.add_node(pydot.Node(aNode.graphid, label=node_lbl))

        if aNode.parent is not None:
            edge = pydot.Edge(aNode.parent.graphid,
                              aNode.graphid,
                              label=aNode.parentEdge)
            graph.add_edge(edge)

        for c in aNode.children:
            traverse(c, graph)

    graph = pydot.Dot(graph_type='graph')
    traverse(aTree, graph)
    return graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("string", help="String to build suffix tree over")
    parser.add_argument("output", help="Name of file to output graph image to")
    args = parser.parse_args()

    input_string = args.string
    output_file = args.output

    tree = suffix_tree.Tree(input_string)
    graph = visualize(tree.root)
    graph.write_png('%s.png' % output_file)

if __name__ == '__main__':
    main()
