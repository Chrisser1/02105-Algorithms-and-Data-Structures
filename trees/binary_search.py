import matplotlib.pyplot as plt
import networkx as nx

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        def _insert(node, key):
            if not node:
                return Node(key)
            if key < node.key:
                node.left = _insert(node.left, key)
            elif key > node.key:
                node.right = _insert(node.right, key)
            return node
        self.root = _insert(self.root, key)

    def delete(self, key):
        def _delete(node, key):
            if not node:
                return node
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                temp = self._min_value_node(node.right)
                node.key = temp.key
                node.right = _delete(node.right, temp.key)
            return node

        self.root = _delete(self.root, key)

    def search(self, key):
        def _search(node, key):
            if not node or node.key == key:
                return node
            if key < node.key:
                return _search(node.left, key)
            return _search(node.right, key)
        return _search(self.root, key)

    def inorder_traversal(self):
        result = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return result

    def to_networkx(self):
        G = nx.DiGraph()

        def _add_edges(node):
            if not node:
                return
            if node.left:
                G.add_edge(node.key, node.left.key)
                _add_edges(node.left)
            if node.right:
                G.add_edge(node.key, node.right.key)
                _add_edges(node.right)

        _add_edges(self.root)
        return G

    def display(self):
        G = self.to_networkx()
        pos = hierarchy_pos(G, self.root.key)
        nx.draw(G, pos, with_labels=True, arrows=False, node_size=1500, node_color="lightblue", font_size=12)
        plt.show()

# Helper function to position nodes like a tree
def hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = {root: (xcenter, vert_loc)}
    children = list(G.successors(root))
    if len(children) != 0:
        dx = width / 2
        nextx = xcenter - width / 2
        for child in children:
            nextpos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                    vert_loc=vert_loc - vert_gap, xcenter=nextx + dx / 2)
            pos.update(nextpos)
            nextx += dx
    return pos

if __name__ == "__main__":
    bst = BinarySearchTree()
    keys = [9, 7, 2, 1, 8, 17, 13, 10, 18]
    for key in keys:
        bst.insert(key)

    bst.display()
    print("Inorder Traversal:", bst.inorder_traversal())
