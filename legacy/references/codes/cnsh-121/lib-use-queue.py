import queue        # 1. 코드가 올바르게 동작하도록 import ______ 채우기

q = queue.Queue()
for i in range(1, 4):   # 2. 출력값이 5 4 3 2 1이 되도록 range(_____) 채우기
    q.put(i)
while not q.empty():
    print(q.get(), sep=' ')

# 2. 출력값이 어떻게 되는지 서술하기
# 3. q.empty()가 True일 때와 False일 때는 각각 어떤 상황인지 서술하기