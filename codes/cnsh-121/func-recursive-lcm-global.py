def lcm(a, b):
    global n, m
    if a == b:
        return a
    if a > b:
        return lcm(a, b+n)      # 1. return ____ 올바르게 동작하도록 재귀함수 호출 채우기 문항
    if a < b:       # 2. 이 라인의 if 제어문이 없이 바로 return lcm(a+m, b)만으로도 동작하는데, 이유를 서술하는 문제
        return lcm(a+m, b)

# 3. 난독화 된 함수 코드를 보고 lcm(3, 8) 출력값 구하기 문항
# 4. while문으로 재구현하기
# a, b = m, n
# while a != b:
#     if a > b:
#         b += n
#     else:
#         a += m
# return a
