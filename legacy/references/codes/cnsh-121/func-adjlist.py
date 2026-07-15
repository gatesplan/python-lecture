V, E = map(int, input().split())
adj = [[] for _ in range(V)]

for i in range(E):
    u, v = map(int, input().split())    # 1. for문 내부 구현을 다 비우고, 인접리스트를 만들도록 구현하는 문제
    adj[u].append(v)
    adj[v].append(u)

print(adj)

# 2. 입력을 4 3 -> 0 1 -> 2 0 -> 3 2 순으로 주었을 때 만들어지는 인접리스트를 구하는 문제