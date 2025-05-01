import matplotlib.pyplot as plt
import networkx as nx

def hierarchy_pos(G, root, width=1.0, vert_gap=0.3, vert_loc=0, xcenter=0.5):
    pos = {root: (xcenter, vert_loc)}
    children = list(G.successors(root))
    if not children:
        return pos
    dx = width / len(children)
    nextx = xcenter - width/2 - dx/2
    for child in children:
        nextx += dx
        pos.update(hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                 vert_loc=vert_loc - vert_gap, xcenter=nextx))
    return pos

class TwoThreeNode:
    id_counter = 0

    def __init__(self, keys=None, children=None):
        self.keys = keys or []
        self.children = children or []
        self.id = TwoThreeNode.id_counter
        TwoThreeNode.id_counter += 1

    def is_leaf(self):
        return len(self.children) == 0

    def is_full(self):
        return len(self.keys) == 2

    def label(self):
        return "[" + ",".join(str(k) for k in self.keys) + "]"


def _add_to_node(node, key, left, right):
    keys = node.keys + [key]
    keys.sort()
    if node.is_leaf():
        if len(keys) <= 2:
            node.keys = keys
            return node
    if len(node.keys) == 1:
        index = 0 if key < node.keys[0] else 1
        node.keys.insert(index, key)
        node.children.pop(index)
        node.children.insert(index, left)
        node.children.insert(index + 1, right)
        return node
    else:
        # Split node
        keys = node.keys + [key]
        keys.sort()
        children = node.children.copy()
        if left and right:
            index = 0 if key < keys[0] else (2 if key > keys[1] else 1)
            children.pop(index)
            children.insert(index, left)
            children.insert(index + 1, right)
        mid_key = keys[1]
        left_node = TwoThreeNode(keys=[keys[0]], children=children[:2])
        right_node = TwoThreeNode(keys=[keys[2]], children=children[2:])
        return mid_key, left_node, right_node


class TwoThreeTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = TwoThreeNode(keys=[key])
        else:
            result = self._insert(self.root, key)
            if isinstance(result, tuple):  # root was split
                new_key, left_child, right_child = result
                self.root = TwoThreeNode(keys=[new_key], children=[left_child, right_child])

    def _insert(self, node, key):
        if node.is_leaf():
            return _add_to_node(node, key, None, None)
        # Traverse to correct child
        if key < node.keys[0]:
            child_index = 0
        elif len(node.keys) == 1 or (len(node.keys) == 2 and key < node.keys[1]):
            child_index = 1
        else:
            child_index = 2
        child = node.children[child_index]
        result = self._insert(child, key)
        if isinstance(result, tuple):  # child split
            new_key, left_child, right_child = result
            return _add_to_node(node, new_key, left_child, right_child)
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return False
        if key in node.keys:
            return True
        if node.is_leaf():
            return False
        if key < node.keys[0]:
            return self._search(node.children[0], key)
        elif len(node.keys) == 1 or (len(node.keys) == 2 and key < node.keys[1]):
            return self._search(node.children[1], key)
        else:
            return self._search(node.children[2], key)

    def display(self):
        if not self.root:
            print("Empty tree.")
            return
        G = nx.DiGraph()
        labels = {}

        def _add_edges(node):
            node_id = node.id
            G.add_node(node_id)
            labels[node_id] = node.label()
            for child in node.children:
                G.add_node(child.id)
                G.add_edge(node_id, child.id)
                _add_edges(child)

        _add_edges(self.root)
        pos = hierarchy_pos(G, self.root.id)
        nx.draw(G, pos, with_labels=True, labels=labels,
                node_size=1500, node_color="lightgreen", font_size=10)
        plt.show()

        _add_edges(self.root)
        pos = hierarchy_pos(G, self.root.id)
        nx.draw(G, pos, with_labels=True, labels=labels,
                node_size=1500, node_color="lightgreen", font_size=10)
        plt.show()

if __name__ == "__main__":
    tree = TwoThreeTree()
    for key in [5, 2, 6, 9, 4, 10, 1]:
        tree.insert(key)
        tree.display()
