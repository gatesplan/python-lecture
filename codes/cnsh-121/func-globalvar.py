s = 0               # 이 변수를 없애고 실행시 무슨 일이 벌어지는지 서술하라는 문항

def f(n):
    global s
    k=0
    while k<n:
        k = k+1
        s = s+k
