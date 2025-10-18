def printnums(n):
    if n < 1:
        return
    printnums(n-1)
    print(n)

# 1. print(5)의 출력값 예상하여 쓰기
# 2. 4번, 5번 라인을 순서를 바꾸면 출력이 어떻게 바뀔지 콜 스택 용어를 사용해 설명하기 (서술형)