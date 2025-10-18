T=dict()
S=input()
a,b=map(str,input().split())

p=0
ans=0
for i in S:
    if i != '-':
        T[i]=p # 각 알파벳의 키를 만드는 중(인덱스 번호 저장)
    p+=1

# 여기까지 딕셔너리를 만들어서 A,B,C,D,E를 키, 인덱스 번호를 값으로 저장함 

while T[a] != T[b]:
    if T[a] > T[b]:
        a=S[T[a]//2]
    else:
        b=S[T[b]//2]
    ans += 1

print(ans)
