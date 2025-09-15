s = [0]*9

for i in range(3):
    s[i*3], s[i*3+1], s[i*3+2] = map(int, input().split())

    for j in range(3):
        if s[i*3+j] == 0:
            pos = i*3 + j

if pos > 2:         # 1. if ____: 조건식 채우기. 0 위치가 맨 윗줄이 아니면 올릴 수 있도록 채우라고 하는 문제.
    s[pos], s[pos-3] = s[pos-3], s[pos]     # 2. s[pos], s[____] = s[____], s[pos] 0 위치와 바꿀 위치 채우고 이유 설명하기 서술형 문제.

    for i in range(3):
        for j in range(3):
            print(s[i*3+j], end=' ')
        print()
    print()

else:
    print("Impossible")

# 3. 설명 없이 코드만 주고, 이 코드의 목적에 대해 설명하도록 하는 서술형 문제