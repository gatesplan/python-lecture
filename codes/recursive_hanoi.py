def f(n, s, t, w):
    if n >= 1:
        f(n-1, s, w, t)
        print(n, s, t)
        f(n-1, w, t, s)
    else:
        print(n, s, t)
