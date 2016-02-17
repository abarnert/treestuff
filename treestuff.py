import collections
from operator import attrgetter, itemgetter

# Most tree algorithms can be written as higher-order functions.
# For example, any top-down traversal just needs a function to go
# from a node to an iterable of its children. And that's true
# whether you write the traversal recusively:

def postorder(node, children_func):
    for child in children_func(node):
        yield from postorder(child, children_func)
    yield node

# ... or iteratively:
        
def preorder(node, children_func):
    s = [node]
    while s:
        node = s.pop()
        yield node
        s.extend(reversed(list(children_func(node))))

# ... and of course it works just as well for BFS as fro DFS:

def levelorder(node, children_func):
    q = collections.deque([node])
    while q:
        node = q.popleft()
        yield node
        q.extend(children_func(node))

# Doing things this way means we can use completely different
# structures and APIs for trees, depending on what we need, and
# use the same generic functions.

# For example, this tree is just a tuple of tuples:
simpletree = (1, ((2, ((4, ()), (5, ()))), (3, ())))

# Its "children" function is just lambda node: node[1]--or, more simply:
for node in levelorder(simpletree, itemgetter(1)):
    print(node[0], end=' ')
print()

# But the same functions work on something more complicated:
from xml.etree import ElementTree as ET
xdoc = ET.fromstring("""
<node value="1">
    <node value="2">
        <node value="4"/>
        <node value="5"/>
    </node>
    <node value="3"/>
</node>
""")
for node in levelorder(xdoc, iter):
    print(node.get('value'), end=' ')
print()

# You can even write a higher-order printing function that takes
# the traversal function as an argument:

def print_tree(node, value_func, children_func, traversal_func):
    for node in traversal_func(node, children_func):
        print(value_func(node), end=' ')
    print()

print_tree(simpletree, itemgetter(0), itemgetter(1), preorder)
print_tree(simpletree, itemgetter(0), itemgetter(1), postorder)
print_tree(simpletree, itemgetter(0), itemgetter(1), levelorder)

print_tree(xdoc, lambda node: node.get('value'), iter, preorder)
print_tree(xdoc, lambda node: node.get('value'), iter, postorder)
print_tree(xdoc, lambda node: node.get('value'), iter, levelorder)

# Just to verify that it's flexible enough: what if I wanted a tree
# that didn't directly hold its children, but instead used a next-sibling
# pointer?
Node = collections.namedtuple('Node', 'value first_child next_sibling')
node3 = Node(3, None, None)
node5 = Node(5, None, None)
node4 = Node(4, None, node5)
node2 = Node(2, node4, node3)
root = Node(1, node2, None)

# Now the children function isn't quite trivial enough to write as a
# lambda in the function call, but still, pretty simple:
def children(node):
    node = node.first_child
    while node:
        yield node
        node = node.next_sibling

print_tree(root, attrgetter('value'), children, preorder)
print_tree(root, attrgetter('value'), children, postorder)
print_tree(root, attrgetter('value'), children, levelorder)
