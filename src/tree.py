from treeplotter.tree import Node, Tree
root = Node(value=1.0, name=None)


child1 = Node(value=0.5, name=None)
child2 = Node(value=1.0, name=None)
child3 = Node(value=3.0, name="A")

root.children = {child1, child2, child3}
