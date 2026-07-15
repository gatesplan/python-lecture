def gcd_recursive(a, b):
    a, b = abs(a), abs(b)
    if b == 0:                      # 조건식 부분을 비워두고 종료조건을 올바르게 채우라는 문항
        return a
    return gcd_recursive(b, a % b)  # 괄호 내부를 비워두고 동작하도록 채우라는 문항

# gcd(10, 8)
#  gcd(8, 2)
#   gcd(2, 0)
#   if b == 0가 참
#     return 2
#   2
# 2
# 이 함수를 주고 같은 기능을 while 문으로 구현하라는 문항