T=dict()
S=input()
a,b=map(str,input().split())

p=0
ans=0
for i in S:
    if i != '-':
        T[i]=p 
    p+=1

#박현진 ver.

'''
def f(a,b):
    global T
    global ans

    if T[a] == T[b]:
        return
    if T[a] == T[b]:
        a=S[T[a]//2]
    else:
        b=S[T[b]//2]

    f(a,b)

f(a,b)
print(ans)
'''

def k(a,b,cnt):
    global S,T
    if T[a]==T[b]:
        return cnt

    if T[a] > T[b]:
        return k(S[T[a]//2],b,cnt+1)
    else:
        return k(a,S[T[b]//2],cnt+1)
    


