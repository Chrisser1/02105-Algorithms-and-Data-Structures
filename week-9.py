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

N,M = [int(i) for i in input().split()]
edges = []

for i in range(M):
    i, j, p = [int(k) for k in input().split()]
    edges.append((p, i, j))

u = UnionFind(N)

edges.sort()

edges_added = 0
cost = 0

for k in range(M):
    p, i, j = edges[k]

    if u.connected(i, j):
        continue

    u.union(i, j)
    cost += p
    edges_added += 1

    if edges_added == N - 1:
        break

print(cost)
