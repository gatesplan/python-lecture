"""
스스로 해 보기 3 (p182)
자연수 n, k가 주어질 때 1부터 n까지 중 k와 서로소인 개수

알고리즘:
- 두 수가 서로소인지 확인하는 방법: GCD = 1일 때 서로소
- 최대공약수(GCD) 알고리즘: 유클리드 호제법 (while문 응용 버전)

유클리드 호제법:
- GCD(a, b) = GCD(b, a mod b)
- 반복적으로 빼는 방법: a > b이면 a = a - b, 아니면 b = b - a
- a == b가 되면 그 값이 GCD
"""

n, k = 1000, 168

# 최대공약수 찾기 알고리즘: 유클리드 호제법 while문 응용 버전
# 예제: a, b = 10, 60
# while a != b:
#     if a > b:
#         a = a - b
#     else:
#         b = b - a

ans = 0
for i in range(1, n+1):
    a, b = k, i

    # 유클리드 호제법으로 GCD 구하기
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a

    # GCD가 1이면 서로소
    if a == 1:
        ans += 1

print(ans)

# 시간복잡도: O(n × log(max(k, n)))
