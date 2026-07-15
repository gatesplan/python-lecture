def gcd_while(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    if a == 0: return b         # 종료조건 두 줄을 비우고 이 함수가 바르게 동작하도록 채우라는 문항
    if b == 0: return a

    while b != 0:
        a, b = b, a % b         # 이 줄 비우고 최대공약수를 구하는 함수를 완성하라는 문항

    return a

# 이 함수를 주고 같은 기능을 재귀함수로 구현하라는 문항
