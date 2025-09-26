import queue

a = [36, 4, 77, 6, 128, 25, 9, 7]
s0 = queue.LifoQueue()
s1 = queue.LifoQueue()
for i in a:
    if i%2==0:              # 3. if _______:로 조건식을 비워두고, 출력이 36, 6, 9, 4, 77, 128, 25, 7이 되도록 코드를 완성하시오.
        s0.put(i)
    else:
        s1.put(i)
while not s0.empty():
    print(s0.get(), end=' ')
while not s1.empty():
    print(s1.get(), end=' ')

# 1. LifoQueue()의 동작 방식에 대하여 서술하고, 위 코드를 실행했을 때의 출력을 쓰시오.
# 2. 위 코드에서 s0, s1에 LifoQueue() 대신 Stack을 사용했을 때의 출력을 쓰시오.
