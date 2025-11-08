"""
숫자 덧셈 순열 문제
- 재귀 함수를 이용한 순열 계산
- 종료조건과 재귀 처리의 관계 이해
"""

# 숫자 덧셈 순열
# 종료조건
# 처리 + 재귀 vs 재귀 + 처리
def f(n):
    # 종료조건
    if n == 0:
        return 1

    # 처리
    cnt = 0
    for i in range(n):  # i = 0, 1, 2, 3, .. n-1
        cnt = cnt + f(i)
        print(cnt)

    return cnt

# 실행 예제
# f(3)
# cnt + f(0) = cnt + 1
# cnt + f(1)
#       return cnt + 1 = 1
# cnt + 3

n = int(input())
print(f(n))
