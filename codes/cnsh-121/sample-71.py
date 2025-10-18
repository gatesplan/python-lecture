import queue
t = [10, 3, 7, 4, 6, 2, 8, 5, 1, 9]
s = queue.LifoQueue()
for i in t :
    while not s.empty():
        k = s.get()
        if i > k:
            print(k)
        else:
            s.put(k)
            break
    s.put(i)
while not s.empty():
    print(s.get())

# 1. 위 코드의 출력 결과를 쓰시오.
# 2. t = [1, 3, 5, 7, 6, 4, 2]일 때, 세 번째로 print 함수가 실행되어 출력되는 값을 쓰시오.
# 3. 위 코드에서 s에 LifoQueue() 대신 Queue()를 사용했을 때, 출력 결과를 쓰시오.
