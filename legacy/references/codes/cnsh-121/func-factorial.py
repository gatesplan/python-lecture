def factorial(n):
    result = 1
    for i in range(n, 0, -1):       # 1. 팩토리얼 값이 나오도록 range() 세 파라메터 바르게 채우기 문제
        result *= i                 # 2. 팩토리얼 값이 나오도록 이 한 줄 채우기 문제

    return result

# 3. 재귀함수로 factorial 함수 다시 구현하기 문제