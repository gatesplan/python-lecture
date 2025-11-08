def f(x,y,z,d):
    global V, visited, ok , ans
    if ok :
        return
    if y == V :
        if ans > d :
            ans = d
        return

    visited[x] = True

    for u, w in M[x]:
        if visited[u] == False:
            z.append(u)
            f(u, y+1, z, d+w)
            z.pop()

    visited[x] = False
    return

M = [[] for i in range(11)]
ans = 123456789987654321
visited = [0 for i in range(11)]
ok = False
V, E = map(int, input().split())

for i in range(E):
    u, v, w = map(int, input().split())
    M[u].append((v,w))
    M[v].append((u,w))

for v in range(0, V+1):
    f(v, 1, [v],0)

print(ans)

    
