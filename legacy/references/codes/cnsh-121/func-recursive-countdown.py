def printnums(n):
    if n < 1:
        return
    printnums(n-1)  # 재귀호출
    print(n)  # 후행 = 역순

# printnums(3)
#   printnums(2)
#      printnums(1)
#         printnums(0)
#         if n<1: return
#      print(1)
#   print(2)
# print(3)

def printnums(n):
    if n < 1:
        return
    print(n)  # 선행 : 정순
    printnums(n-1)  # 재귀호출

# printnums(3)
# print(3)
#     printnums(2)
#     print(2)
#         printnums(1)
#         print(1)
#             printnums(0)
#

def printnums(n):
    print(n)  # 선행 : 정순
    if n < 1:
        return
    printnums(n-1)  # 재귀호출

# printnums(3)
# print(3)
#     printnums(2)
#     print(2)
#         printnums(1)
#         print(1)
#             printnums(0)
#             print(0)

# 스택/큐
# 콜스택
# 1. print(5)의 출력값 예상하여 쓰기
# 2. 4번, 5번 라인을 순서를 바꾸면 출력이 어떻게 바뀔지 콜 스택 용어를 사용해 설명하기 (서술형)