V, E = map(int, input().split())
M = [[] for i in range(V)]
visited = [0]*V
ok = False

for i in range(E):
    u, v = map(int, input().split())
    M[u].append(v)
    M[v].append(u)

def f(x, y, z):
    global V, visited, ok, M

    if ok: return

    if y == V:
        ok = True
        for i in z:
            print(i, end=' ')
        return

    visited[x] = True

    for u in M[x]:
        if not visited[u]:
            z.append(u)
            f(u, y+1, z)
            z.pop()

    visited[x] = False
    return

# 1. 16번라인 if _______: 조건식 비우고, 22번라인 visited[x] = ________ 비우고, 27번라인 f(__, ___, ___) 파라메터 비워두고 채우라고 요구하기.

# 2. 각 파라메터 x, y, z의 역할에 대해 설명 서술하기

# 3. 입력예시 주고 출력 경로 구하기
# 7 11
# 0 1
# 0 2
# 0 3
# 0 6
# 1 2
# 2 6
# 3 4
# 3 5
# 3 6
# 4 5
# 5 6
# 실행은 f(3, 1, [3]) -> 출력시 3 0 1 2 6 5 4 출력됨