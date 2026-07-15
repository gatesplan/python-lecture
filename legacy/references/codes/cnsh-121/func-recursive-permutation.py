def permutation(n, r):
    if r == 0:
        return 1
    return n * permutation(n-1, r-1)   # 1. 재귀함수 동작하도록 return ________ 채우기

# 2. permutation(5, 3) 출력값 계산과정 서술하기
# 5P3
# 5*4P2
# 5*(4*3P1)
# 5*(4*(3*2P0))
# 5*(4*(3*1))
# 5*(4*3)
# 5*12
# 60

# 호출순서, 콜스택, 동작이 재귀호출에 대해 선행인지 후행인지