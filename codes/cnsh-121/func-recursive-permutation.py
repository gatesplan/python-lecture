def permutation(n, r):
    if r == 0:
        return 1
    return n * permutation(n-1, r-1)   # 1. 재귀함수 동작하도록 return ________ 채우기

# 2. permutation(5, 3) 출력값 계산과정 서술하기

