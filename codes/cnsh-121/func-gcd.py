def gcd(a, b):
    while a != 0:           # 1. 유클리드 호제법에 따라 동작하도록 while ____ : 조건식 완성하기
        a, b = b % a, a     # 2. while문 실행부분 a, b = _________ 동작하도록 채우기
    return b

# 3. 재귀함수로 재구현하기