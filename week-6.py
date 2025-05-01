from collections import deque

N, M = [x for x in input().split()]

N, M = int(N), int(M)

graph = [[] for _ in range(N)]
for _ in range(M):
    i, j = [x for x in input().split()]
    i, j = int(i), int(j)
    graph[j].append(i)

def topo_sort(G):
    N = len(G)
    q = deque()
    in_degree = [0] * N
    order = []
    index = 0

    for i in range(N):
        for j in G[i]:
            in_degree[j] += 1

    for i in range(N):
        if in_degree[i] == 0:
            q.append(i)

    while q:
        current = q.popleft()

        for j in G[current]:
            in_degree[j] -= 1
            if in_degree[j] == 0:
                q.append(j)


        order.append(current)

    return order

def longest_distance(G, order):
    N = len(G)
    distance = [1] * N

    for i in order:
        for j in G[i]:
            distance[j] = max(distance[j], distance[i] + 1)

    return max(distance)

order = topo_sort(graph)
print(longest_distance(graph, order))
