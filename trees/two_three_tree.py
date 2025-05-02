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
        self.size = 0

    def is_leaf(self):
        return len(self.children) == 0

    def is_full(self):
        return len(self.keys) == 2

    def update_size(self):
        self.size = len(self.keys)
        for child in self.children:
            self.size += child.size

    def label(self):
        return "[" + ",".join(str(k) for k in self.keys) + "]"


def _add_to_node(node, key, left, right):
    keys = node.keys + [key]
    keys.sort()
    if node.is_leaf():
        if len(keys) <= 2:
            node.keys = keys
            return node

    # Internal node
    children = node.children.copy()
    if left and right:
        # Determine proper place to insert new children
        insert_pos = 0
        while insert_pos < len(node.keys) and key > node.keys[insert_pos]:
            insert_pos += 1
        children.pop(insert_pos)
        children.insert(insert_pos, left)
        children.insert(insert_pos + 1, right)

    if len(keys) <= 2:
        node.keys = keys
        node.children = children
        return node

    # Split logic
    mid_index = 1
    mid_key = keys[mid_index]

    left_node = TwoThreeNode(
        keys=[keys[0]],
        children=children[:2] if children else []
    )
    right_node = TwoThreeNode(
        keys=[keys[2]],
        children=children[2:] if children else []
    )

    node.update_size()
    return mid_key, left_node, right_node


def _min_node(node):
    while not node.is_leaf():
        node = node.children[0]
    return node


def _fix_underflow(node, idx):
    # Try redistribution or merging
    if idx > 0 and len(node.children[idx - 1].keys) > 1:
        # Borrow from left sibling
        left = node.children[idx - 1]
        child = node.children[idx]
        borrow_key = node.keys[idx - 1]
        node.keys[idx - 1] = left.keys.pop()
        child.keys.insert(0, borrow_key)
        if left.children:
            child.children.insert(0, left.children.pop())
    elif idx < len(node.children) - 1 and len(node.children[idx + 1].keys) > 1:
        # Borrow from right sibling
        right = node.children[idx + 1]
        child = node.children[idx]
        borrow_key = node.keys[idx]
        node.keys[idx] = right.keys.pop(0)
        child.keys.append(borrow_key)
        if right.children:
            child.children.append(right.children.pop(0))
    else:
        # Merge with sibling
        if idx > 0:
            left = node.children[idx - 1]
            child = node.children[idx]
            merge_key = node.keys.pop(idx - 1)
            left.keys.append(merge_key)
            left.keys.extend(child.keys)
            if child.children:
                left.children.extend(child.children)
            node.children.pop(idx)
        else:
            child = node.children[idx]
            right = node.children[idx + 1]
            merge_key = node.keys.pop(idx)
            child.keys.append(merge_key)
            child.keys.extend(right.keys)
            if right.children:
                child.children.extend(right.children)
            node.children.pop(idx + 1)
    node.update_size()
    return node


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
        node.update_size()
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

    def delete(self, key):
        if not self.root:
            return
        self.root = self._delete(self.root, key)
        if self.root and not self.root.keys and self.root.children:
            self.root = self.root.children[0]  # root collapsed

    def _delete(self, node, key):
        if node.is_leaf():
            if key in node.keys:
                node.keys.remove(key)
            return node if node.keys else None  # return None if node is empty
        # Internal node
        if key in node.keys:
            key_index = node.keys.index(key)
            # Replace key with successor
            successor_node = _min_node(node.children[key_index + 1])
            successor_key = successor_node.keys[0]
            node.keys[key_index] = successor_key
            node.children[key_index + 1] = self._delete(node.children[key_index + 1], successor_key)
        else:
            # Determine correct child
            if key < node.keys[0]:
                idx = 0
            elif len(node.keys) == 1 or (len(node.keys) == 2 and key < node.keys[1]):
                idx = 1
            else:
                idx = 2
            child = self._delete(node.children[idx], key)
            if child:
                node.children[idx] = child
            else:
                # Handle underflow: merge or redistribute
                node = _fix_underflow(node, idx)
        if not node.keys and node.children:
            return node.children[0]  # collapse root
        node.update_size()
        return node

    def predecessor(self, k):
        return self._predecessor(self.root, k, None)

    def _predecessor(self, node, k, best):
        if not node:
            return best
        for key in node.keys:
            if key == k:
                return key
            elif key < k:
                best = key
        if k < node.keys[0]:
            return self._predecessor(node.children[0] if node.children else None, k, best)
        elif len(node.keys) == 1 or k < node.keys[1]:
            return self._predecessor(node.children[1] if node.children else None, k, best)
        else:
            return self._predecessor(node.children[2] if len(node.children) > 2 else None, k, best)

    def rangereport(self, k1, k2):
        result = []
        self._rangereport(self.root, k1, k2, result)
        return result

    def _rangereport(self, node, k1, k2, result):
        if not node:
            return
        if len(node.keys) == 1:
            k = node.keys[0]
            if k1 < k:
                self._rangereport(node.children[0] if node.children else None, k1, k2, result)
            if k1 <= k <= k2:
                result.append(k)
            if k < k2:
                self._rangereport(node.children[1] if node.children else None, k1, k2, result)
        else:
            k1_node, k2_node = node.keys
            if k1 < k1_node:
                self._rangereport(node.children[0] if node.children else None, k1, k2, result)
            if k1 <= k1_node <= k2:
                result.append(k1_node)
            if k1 < k2_node:
                self._rangereport(node.children[1] if node.children else None, k1, k2, result)
            if k1 <= k2_node <= k2:
                result.append(k2_node)
            if k2_node < k2:
                self._rangereport(node.children[2] if len(node.children) > 2 else None, k1, k2, result)

    def rangecount(self, k1, k2):
        return self._rank(self.root, k2) - self._rank(self.root, k1 - 1)

    def _rank(self, node, k):
        if not node:
            return 0
        if len(node.keys) == 1:
            if k < node.keys[0]:
                return self._rank(node.children[0] if node.children else None, k)
            else:
                left_size = node.children[0].size if node.children else 0
                return left_size + 1 + self._rank(node.children[1] if node.children else None, k)
        else:
            if k < node.keys[0]:
                return self._rank(node.children[0] if node.children else None, k)
            elif k < node.keys[1]:
                left_size = node.children[0].size if node.children else 0
                return left_size + 1 + self._rank(node.children[1] if node.children else None, k)
            else:
                left_size = node.children[0].size if node.children else 0
                mid_size = node.children[1].size if node.children else 0
                return left_size + mid_size + 2 + self._rank(node.children[2] if len(node.children) > 2 else None, k)

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

def test_delete():
    tree = TwoThreeTree()
    keys_to_insert = [5, 2, 6, 9, 4, 10, 1, 3, 7, 11]
    for key in keys_to_insert:
        tree.insert(key)

    print("Initial tree:")
    tree.display()

    keys_to_delete = [10, 6, 2, 5, 1]  # Try deleting in various scenarios
    for key in keys_to_delete:
        print(f"\nDeleting key: {key}")
        tree.delete(key)
        tree.display()

def test_queries():
    tree = TwoThreeTree()
    for key in [5, 2, 6, 9, 4, 10, 1, 3, 7, 11]:
        tree.insert(key)

    tree.display()
    print("\nPREDECESSOR tests:")
    for k in [3, 7, 6, 8, 12]:
        print(f"PREDECESSOR({k}) → {tree.predecessor(k)}")

    print("\nRANGEREPORT(3, 8):", tree.rangereport(3, 8))
    print("RANGECOUNT(3, 8):", tree.rangecount(3, 8))


if __name__ == "__main__":
    # tree = TwoThreeTree()
    # for key in [5, 2, 6, 9, 4, 10, 1, 3, 7, 6, 11]:
    #     tree.insert(key)
    # tree.display()
    test_delete()
    # test_queries()
