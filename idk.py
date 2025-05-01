from collections import deque

N,M,a,b = [int(value) for value in input().split()]

graph = [[] for i in range(N)]

for _ in range(M):
	x, y = [int(i) for i in input().split()]
	graph[x].append(y)
	graph[y].append(x)

visited = [False for i in range(N)]

def bfs(graph, a):
	cue = deque()
	cue.append(a)
	visited[a] = True
	while cue:
		at = cue.popleft()
		for neighbor in graph[at]:
			if not visited[neighbor]:
				visited[neighbor] = True
				cue.append(neighbor)

bfs(graph, a)
if visited[b]:
	print("TRUE")
else:
	print("FALSE")
