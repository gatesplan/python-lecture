"""
p187 소수 구하기 - 상태 공간 배제 (더 효율적인 방법)

최적화 기법:
- k가 소수인지 찾을 때 int(k**0.5)까지만 약수인지 확인하면 됨
- 이유: k = a × b에서 a ≤ √k ≤ b이므로, √k까지만 확인하면 모든 약수 쌍을 찾을 수 있음

시간복잡도: O(n × √n)
"""

# k가 소수인지 찾는 기능의 구현
def is_prime(k):
    """
    k가 소수인지 판별하는 함수
    시간복잡도: O(√k)
    """
    for i in range(2, int(k**0.5) + 1):
        if (k % i) == 0:
            return False
    return True


# 위 코드를 참고하여 1부터 n까지 소수 개수 세기
# 동적프로그래밍: k가 소수인지 찾을 때 이전에 찾은 소수 활용 가능
ans = 0
n = 1000

for i in range(2, n+1):
    cnt = 0
    for j in range(2, i):
        if (i % j) == 0:
            cnt = cnt + 1

    if cnt == 0:
        ans += 1

print(ans)

# 더 효율적인 버전 (is_prime 함수 활용)
ans_optimized = 0
for i in range(2, n+1):
    if is_prime(i):
        ans_optimized += 1

print(f"최적화 버전: {ans_optimized}")
