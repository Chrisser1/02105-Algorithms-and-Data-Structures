
class TwoThreeTree:
    def __init__(self):
        self.root = None

    class Node:
        def __init__(self, keys=None, children=None):
            self.keys = keys if keys is not None else []
            self.children = children if children is not None else []

    def insert(self, key):
        if self.root is None:
            self.root = self.Node([key])
        else:
            new_key, new_child = self._insert(self.root, key)
            if new_child:
                new_root = self.Node([new_key], [self.root, new_child])
                self.root = new_root

    def _insert(self, node, key):
        if len(node.keys) == 3:  # Node is full
            mid_key = node.keys[1]
            left_child = self.Node(node.keys[:1], node.children[:2])
            right_child = self.Node(node.keys[2:], node.children[2:])
            node.keys = [mid_key]
            node.children = [left_child, right_child]

        if len(node.children) == 0:  # Leaf node
            node.keys.append(key)
            node.keys.sort()
            return (None, None)

        # Non-leaf node
        if key < node.keys[0]:
            new_key, new_child = self._insert(node.children[0], key)
        elif len(node.keys) == 1 or key < node.keys[1]:
            new_key, new_child = self._insert(node.children[1], key)
        else:
            new_key, new_child = self._insert(node.children[2], key)

        if new_child:  # Child was split
            node.keys.append(new_key)
            node.keys.sort()
            return (node.keys[0], new_child)
        return (None, None)