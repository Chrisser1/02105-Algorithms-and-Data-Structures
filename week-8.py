class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # Weighted union
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return

        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]

    def connected(self, x, y):
        return self.find(x) == self.find(y)

def process_network():
    import sys
    input = sys.stdin.read
    data = input().splitlines()

    # Parse input
    N, M = map(int, data[0].split())
    uf = UnionFind(N)

    results = []

    for line in data[1:]:
        parts = line.split()
        op, a, b = parts[0], int(parts[1]), int(parts[2])

        if op == 'A':
            uf.union(a, b)
        elif op == 'C':
            results.append("Yes" if uf.connected(a, b) else "No")

    # Print output for CONNECTED queries
    for result in results:
        print(result)

process_network()
