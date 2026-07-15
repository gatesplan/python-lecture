def even_sum(n):
    result = 0
    for i in range(n+1):    # 1. range(__) 파라메터 채우기 문제
        if i % 2 == 0:
            result += i     # 2. 이 한 줄 비워두고, 짝수합을 구하도록 채우기 문제
    return result

# 3. 위 코드를 한 줄로 바꾸기 문제
# 4. 짝수합을 재귀함수로 구현하기 문제
# 5. while문으로 구현하기 문제