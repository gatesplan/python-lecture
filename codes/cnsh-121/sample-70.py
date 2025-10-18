import queue

q0 = queue.Queue()
q1 = queue.Queue()
a = [36, 4, 77, 6, 128, 25, 9, 7, 1, 62, 99]
p = 1
while p < 256:          # 1. while 조건문을 p <= ____ 로 할 때, 빈칸에 들어갈 가능한 최소값을 쓰고, 동작 과정을 포함하여 이유를 설명하시오.
    b = []
    for i in a:
        if (p&i)==0:    # 2. p&i==0 일 때와 그렇지 않을 때, p와 i 사이 관계를 설명하시오.
            q0.put(i)
        else:
            q1.put(i)
    while not q0.empty():
        b.append(q0.get())
    while not q1.empty():
        b.append(q1.get())

    a=b
    p<<=1               # 3. 이 줄을 비워두고 올바르게 동작하도록 채우는 문항.

for i in a:
    print(i, end=' ')

# 4. 출력 결과를 물어보는 문항
