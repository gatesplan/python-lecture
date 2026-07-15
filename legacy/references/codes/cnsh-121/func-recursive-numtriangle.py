def numtriangle(n):
    if n < 1:
        return
    numtriangle(n-1)        # 1. 재귀함수 동작하도록 numtriangle(___) 파라메터 올바르게 채우기

    for i in range(1, n+1): # 2. 예상 출력대로 올바르게 동작하도록 range(_____) 파라메터 채우기
        print(i, end=' ')

    print()         # 3. 이 print()가 없으면 출력값이 어떻게 변하는지 설명하시오.

# 4. 이중 for문으로 재구현하기