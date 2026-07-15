V, E = map(int, input("입력: 점 선 개수").split())
adj = [[0]*V for _ in range(V)]

for i in range(E):
    u, v = map(int, input('연결할 두 점의 번호').split())
    adj[u][v] = adj[v][u] = 1

print(adj)

# 1. 입력을 4 3 -> 0 1 -> 2 0 -> 3 2 순으로 주었을 때 만들어지는 인접행렬을 구하는 문제
