"""
서로소 판별 (간단한 방법)

서로소(Coprime):
- 두 수의 최대공약수(GCD)가 1인 경우
- 1 이외의 공약수가 없는 두 수

방법:
- 2부터 min(x, y)까지 공약수가 있는지 확인
"""

x, y = 10, 13

a, b = min(x, y), max(x, y)

# 2부터 작은 수까지 공약수 찾기
for i in range(2, a+1):
    if a % i == 0 and b % i == 0:
        print('서로소 아님')
        break
else:
    print('서로소')

# 시간복잡도: O(min(a, b))
