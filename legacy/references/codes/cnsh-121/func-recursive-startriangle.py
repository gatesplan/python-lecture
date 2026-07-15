def f(n):
    if n <= 1:              # 조건 비워놓고 채우기
        print('*')
    else:                   # else: 하부 목적에 맞게 채우기
        f(n-1)              # 한 줄 비워놓고 채우기
        print('*'*n)        # print( 내부 채우기 )
