# 전역 변수 선언
M = []          # 그래프 (인접 리스트)
ans = 0         # 최소 비용
visited = []    # 방문 여부
V, E = 0, 0     # 노드 개수, 간선 개수


def init_graph():
    """그래프와 방문 배열을 초기화한다"""
    global M, visited, ans
    M = [[] for i in range(11)]
    visited = [False for i in range(11)]
    ans = 123456789987654321


def add_edge(u, v, w):
    """그래프에 양방향 간선을 추가한다"""
    global M
    M[u].append((v, w))
    M[v].append((u, w))


def read_input():
    """그래프 정보를 입력받는다"""
    global V, E
    V, E = map(int, input().split())

    for i in range(E):
        u, v, w = map(int, input().split())
        add_edge(u, v, w)


def update_ans(d):
    """현재 비용 d가 최솟값보다 작으면 ans를 업데이트한다"""
    global ans
    if ans > d:
        ans = d


def f(x, y, z, d):
    """
    해밀토니안 경로를 재귀적으로 탐색한다

    x: 현재 방문 중인 노드
    y: 지금까지 방문한 노드 개수
    z: 현재까지의 경로 리스트
    d: 현재까지의 비용 합계
    """
    global V, M, visited

    # 모든 노드를 방문했으면 최솟값 업데이트
    if y == V:
        update_ans(d)
        return

    # 현재 노드 방문 표시
    visited[x] = True

    # 인접한 노드들을 탐색
    for u, w in M[x]:
        if visited[u] == False:
            z.append(u)              # 경로에 추가
            f(u, y+1, z, d+w)        # 재귀 호출
            z.pop()                  # 백트래킹: 경로에서 제거

    # 백트래킹: 방문 표시 해제
    visited[x] = False


def find_min_cost():
    """모든 시작점에서 해밀토니안 경로를 탐색한다"""
    global V

    for v in range(V + 1):
        f(v, 1, [v], 0)


def main():
    """메인 실행 함수"""
    global ans

    # 초기화
    init_graph()

    # 입력 받기
    read_input()

    # 최소 비용 해밀토니안 경로 찾기
    find_min_cost()

    # 결과 출력
    print(ans)


if __name__ == "__main__":
    main()
