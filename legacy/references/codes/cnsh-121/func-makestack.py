stack = []
goal = [2, 1, 3, 4]

def push(x):
    global stack
    stack.append(x)

def pop():
    global stack
    return stack.pop()

now = 0
for i in range(1, 5):
    push(i)
    while len(stack)>0 and stack[-1] == goal[now]:
        print(pop())
        now += 1

# 1. while 조건이 잘 동작하도록 while len(stack) > 0 and _____________: 조건식 부분 채우기
# 2. for문에 의한 각 i값의 순서에 따라 while 조건식의 동작 과정과 stack의 변화 과정을 서술하기