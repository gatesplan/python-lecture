# 학교 수업 노트북 정리 - 개념/예제 모음

프로젝트 루트의 2~13차시 노트북에서 내신 대비에 쓸만한 내용만 차시 순으로 정리.
기초 입출력/사칙연산 수준은 제외하고, 개념 확인·실행결과 예측·응용 코드 위주.

---

## 2차시. 입력과 출력

### print() 구분자/종결자

```python
print("A", "B", "C", sep="*")   # A*B*C
print("hello", end=' ')
print("world")                  # hello world
```

### 중요사항
- `sep`는 여러 인자 사이 구분자(기본 공백), `end`는 출력 끝에 붙일 문자(기본 `\n`).
- `input()`의 반환값은 항상 문자열. 사칙연산 하려면 `int()`/`float()` 변환 필수.
- `\n`은 문자열 안에서 줄바꿈. `print()`는 기본적으로 자동 줄바꿈됨.

---

## 3차시. 연산자 1 (산술/대입)

### 복합 대입연산자 값 추적

```python
a = 10
b = 30
c = 15
d = 0

a *= 7       # a = 70
b += a       # b = 100
c *= d       # c = 0
d = a        # d = 70
d **= 2      # d = 4900
b = d + c + a    # b = 4970
c //= 2      # c = 0
a %= 2       # a = 0

print(a, b, c, d)   # 0 4970 0 4900
```

### 중요사항
- `//`는 정수 나눗셈(소수점 버림), `%`는 나머지, `**`는 거듭제곱.
- `a *= 7`은 `a = a * 7`의 축약형. `+= -= *= /= //= %= **=` 모두 동일 원리.
- 순서대로 실행하며 **직전 연산 결과를 다음 줄에 반영**해야 한다. 대입연산자 문제의 핵심.

---

## 4차시. 연산자 2 (비교/논리)

### 실행결과 예측 패턴

```python
a = 2
b = 3
c = a ** b                          # c = 8
print((c - a) > b and not (c > (a + b)))
# (6 > 3) and not (8 > 5)
# True     and not True
# True     and False
# False
```

### 논리연산자 조합

```python
a = 10
b = 5
print(a >= 5 and b < 10)    # True
print(a <= 5 and b > 10)    # False
print(a >= 5 or b > 10)     # True
print(not (a < 5))          # True
```

### 중요사항
- 우선순위: 산술 > 비교 > `not` > `and` > `or`. 헷갈리면 괄호로 묶기.
- `and`는 둘 다 참일 때만 참, `or`는 하나라도 참이면 참, `not`은 참/거짓 뒤집기.
- 비교 결과값은 `True`/`False` (대소문자 주의).
- `==`(같은지 비교)와 `=`(대입)을 혼동하지 말 것.

---

## 5차시. 조건문 1 (if / else)

### 윤년 판별 (복합 조건)

```python
year = int(input("연도: "))

if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print("윤년")
else:
    print("평년")
```

### 범위 조건 (사탕 QC)

```python
weight = float(input("사탕 무게(g): "))

# 범위 벗어남을 or로 먼저 판정
if weight < 10 or weight > 20:
    print("불량품(REJECT)")
else:
    print("합격(PASS)")
```

### 중첩 if (입장 조건 + 예외)

```python
age = int(input("나이: "))
energy = int(input("에너지: "))

if age >= 15 or energy > 100:
    if age >= 100:
        print("입장 거부")
    else:
        print("포탈 가동")
else:
    print("입장 거부")
```

### 중요사항
- `if` 조건 뒤 반드시 콜론(`:`), 실행 코드는 **들여쓰기**로 구분. 파이썬은 들여쓰기가 문법.
- "이거나"는 `or`, "그리고"는 `and`. 한국어 표현을 정확히 매핑해야 논리 오류를 막는다.
- 범위 체크는 `10 <= x <= 20`처럼 연속 비교도 가능. `x >= 10 and x <= 20`과 동등.
- 조건 순서에 따라 결과가 달라질 수 있다. 예외/특수 케이스를 먼저 걸러내는 패턴 기억.

---

## 6차시. 조건문 2 (elif)

### 학점 세분화 + 입력값 검증

```python
score = int(input("점수: "))

if score < 0 or score > 100:
    print("데이터 오류")
elif score >= 95:
    print("A+")
elif score >= 90:
    print("A")
elif score >= 85:
    print("B+")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("F")
```

### 삼각형 종류 판별 (다중 값 입력)

```python
a, b, c = map(int, input("세 변: ").split())

if a == b == c:
    print("정삼각형")
elif a == b or b == c or a == c:
    print("이등변삼각형")
else:
    print("부등변삼각형")
```

### 중요사항
- `elif`는 **위에서부터** 검사하다가 처음으로 참이 되는 블록 하나만 실행. 나머지는 스킵.
- 등급/구간 분기는 **가장 엄격한 조건부터** 써야 한다. 반대로 쓰면 모두 `>= 70`에 걸려 A+이 안 나옴.
- 입력값 유효성 검사(`score < 0 or score > 100`)는 맨 위에 배치.
- `map(int, input().split())`은 공백으로 구분된 정수 여러 개 입력받는 표준 패턴.

---

## 7차시. 튜플과 딕셔너리

### 튜플 기본

```python
colors = ('red', 'blue')
print(colors[0])            # red
print(colors[1] * 2)        # blueblue
a, b = colors               # 언패킹
# colors[0] = 'green'       # 에러: 튜플은 수정 불가
new = colors + ('green',)   # 새 튜플 생성
```

### 변수 스왑 (튜플 원리)

```python
a = 10
b = 20
a, b = b, a   # 한 줄로 교환
print(a, b)   # 20 10
```

### 튜플 연산 결과 예측

```python
a = (1,)
b = (2, 3)
print((a + b) * 2)   # (1, 2, 3, 1, 2, 3)
```

### 딕셔너리 기본

```python
stu = {"name": "Alice", "age": 20}
stu["grade"] = "A"       # 키 추가
print(stu["name"])       # Alice
del stu["age"]           # 키 삭제
print("grade" in stu)    # True (존재 확인)
```

### get()으로 안전 조회

```python
stu = {"name": "Alice", "age": 20}
print(stu.get("height"))           # None (에러 없음)
print(stu.get("height", "없음"))   # 없음 (기본값 반환)
# print(stu["height"])             # KeyError 발생
```

### 중요사항
- 튜플은 `()`, 리스트는 `[]`, 딕셔너리는 `{키:값}`.
- 요소 1개짜리 튜플은 반드시 쉼표: `(5,)`. `(5)`는 그냥 숫자 5.
- 딕셔너리에 없는 키를 `[]`로 접근하면 `KeyError`. `get()`은 에러 대신 `None` 또는 지정한 기본값.
- 딕셔너리의 키는 중복 불가. 같은 키에 새 값을 대입하면 **덮어쓰기**.
- `a, b = b, a` 스왑은 우변이 튜플로 먼저 묶인 뒤 언패킹되는 원리.

---

## 8차시. for 반복문

### range 패턴

```python
for i in range(1, 100, 2):    # 1,3,5,...,99
    print(i)

for i in range(100, 0, -4):   # 100,96,92,...,4
    print(i)

for i in range(1, 10):        # 구구단 7단
    print(f"7 x {i} = {7*i}")
```

### 홀수합 / 짝수합 분리

```python
n = int(input())
hol = 0
zzak = 0

for i in range(1, n + 1):
    if i % 2 == 0:
        zzak += i
    else:
        hol += i

print(hol, zzak)
```

### 튜플/문자열 순회

```python
crews = ("Captain", "Doctor", "Engineer")
for name in crews:
    print(name)

for ch in "PYTHON":
    print(ch)    # 한 글자씩
```

### 딕셔너리 items() 순회

```python
planets = {"수성": 3.7, "지구": 9.8, "화성": 3.7, "목성": 24.7}

for name, gravity in planets.items():
    print(f"{name}: {gravity}")
```

### 중요사항
- `range(stop)`은 0부터 stop-1까지. `range(start, stop)`도 stop **미포함**.
- `range(start, stop, step)`에서 step이 음수면 감소. 감소할 때는 start > stop이어야 한다.
- 리스트/튜플/문자열/딕셔너리 모두 `for` 대상이 될 수 있다(Iterable).
- 딕셔너리 순회 기본은 키. 값만은 `.values()`, 키+값은 `.items()`.
- 합계 누적 변수는 **반복문 밖에서 0으로 초기화** 해야 한다.

---

## 9차시. while 반복문

### 특정 단어로 종료 (break)

```python
while True:
    food = input("먹고 싶은 재료 (끝: 종료): ")
    if food == "끝":
        print("배부르다!")
        break
    print(f"{food}을(를) 추가합니다!")
```

### 합계 초과까지 입력 + 횟수 카운트

```python
count = 0
total = 0

while True:
    n = int(input("점수: "))
    total += n
    count += 1

    if total >= 30:
        print(f"{count}번 만에 합계 {total} 도달")
        break
```

### continue로 특정 값 스킵

```python
reservations = ("김철수", "노쇼", "이영희", "박지성", "노쇼", "손흥민")
i = 0

while i < len(reservations):
    if reservations[i] == "노쇼":
        i += 1
        continue
    print(reservations[i])
    i += 1
```

### 중요사항
- `for`는 **횟수 중심**(몇 번 돌지 미리 알 때), `while`은 **조건 중심**(언제 끝날지 모를 때).
- `while True:`는 무한 루프. `break` 없이는 빠져나올 수 없다.
- `break`는 반복문 **완전 종료**, `continue`는 **현재 회차만 건너뜀**(조건 검사로 복귀).
- `continue` 쓸 때 증감식(`i += 1`)을 빠뜨리지 않도록 주의. 무한루프 원인 1순위.
- `while` 조건이 처음부터 거짓이면 단 한 번도 실행 안 됨.

---

## 10차시. 리스트 1 (선언/인덱싱/슬라이싱)

### 다양한 선언 방식

```python
arr1 = [1, 2, 3, 4, 5, 6, 7]
arr2 = [2] * 6              # [2,2,2,2,2,2]
arr3 = list(range(6))       # [0,1,2,3,4,5]
arr4 = []                   # 빈 리스트
arr5 = [None] * 6           # [None,None,...]
```

### 반복문으로 값 채우기

```python
# 크기 고정 후 인덱스로 할당
multi = [0] * 10
for i in range(10):
    multi[i] = 3 * (i + 1)
print(multi)   # [3, 6, 9, ..., 30]

# 빈 리스트에 append 방식
result = []
for i in range(5):
    result.append((i + 1) * 10)
print(result)  # [10, 20, 30, 40, 50]
```

### 슬라이딩 윈도우

```python
data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

for i in range(5):
    print(data[i:i+3])
# [10, 20, 30]
# [20, 30, 40]
# ...
# [50, 60, 70]
```

### 음수 인덱스 / 슬라이싱

```python
arr = ['A', 'B', 'C', 'D', 'E']
print(arr[-1])    # 'E' (마지막)
print(arr[-2])    # 'D'
print(arr[0:2])   # ['A', 'B'] (끝 미포함)
print(arr[2:])    # ['C', 'D', 'E']
print(arr[:3])    # ['A', 'B', 'C']
```

### 중요사항
- 인덱스는 0부터 시작. 음수는 뒤에서부터 -1, -2, ...
- 슬라이싱 `[시작:끝]`에서 **끝 인덱스는 포함 안 됨**(미만).
- 빈 리스트 `[]`에는 인덱스 할당 불가(`arr[0] = x` 에러). `append()`나 `+`로만 추가.
- `[None] * 5`처럼 미리 크기 잡아두면 `arr[i] = ...` 할당 가능.
- `[10] * 5`는 값 복제, `list(range(5))`는 0~4. 자주 헷갈림.

---

## 11차시. 리스트 2 (메서드)

### 추가/삽입/삭제

```python
arr = [1, 2, 3]
arr.append(4)           # [1, 2, 3, 4] - 맨 뒤 추가
arr.insert(1, 99)       # [1, 99, 2, 3, 4] - 인덱스 1에 끼우기
arr.remove(99)          # [1, 2, 3, 4] - 값 99를 찾아 삭제(첫 번째만)
last = arr.pop()        # last=4, arr=[1,2,3] - 맨 뒤 꺼내기
mid = arr.pop(0)        # mid=1, arr=[2,3]   - 인덱스로 꺼내기
arr.clear()             # [] - 전체 비우기
```

### 정렬/뒤집기

```python
arr = [4, 3, 2, 6, 8, 1]
arr.sort()                  # [1, 2, 3, 4, 6, 8] 오름차순
arr.sort(reverse=True)      # [8, 6, 4, 3, 2, 1] 내림차순
arr.reverse()               # 현재 순서 그대로 뒤집기 (정렬 아님)
```

### 정보 조회

```python
arr = [4, 2, 2, 6, 8, 1, 2]
print(len(arr))         # 7 (길이)
print(arr.count(2))     # 3 (값 2가 몇 번 등장)
print(arr.index(6))     # 3 (값 6이 처음 나오는 인덱스)
```

### 복합 조작 (대기 명단)

```python
waiting = ["김철수", "이영희"]

waiting.append("박지성")       # 맨 뒤에 추가
waiting.insert(1, "손흥민")    # 1번 자리에 끼움
waiting.remove("이영희")       # 이영희 삭제
print(len(waiting))            # 현재 인원수
```

### 중요사항
- `remove(값)`은 값으로 삭제, `pop(인덱스)`는 위치로 삭제하면서 **값을 반환**.
- `sort()`는 리스트 자체를 바꿈(반환값 없음). `sorted(arr)`은 새 리스트 반환.
- `reverse()`와 `sort(reverse=True)`는 다르다. 전자는 현재 순서 뒤집기, 후자는 정렬하면서 내림차순.
- `index(값)`은 값이 없으면 에러. 사용 전 `in`으로 존재 확인 권장.
- `len()`만 내장함수 형태(`len(arr)`), 나머지는 전부 `arr.메서드()` 형태.

---

## 12차시. 리스트 3 (고급 팁 / 2차원)

### 슬라이싱 일괄 수정

```python
nums = [1, 2, 3, 4, 5]
nums[1:4] = [20, 30, 40]
print(nums)   # [1, 20, 30, 40, 5]
```

### 리스트 복사의 함정 (중요)

```python
# 잘못된 복사 - 같은 리스트를 가리킴
original = [1, 2, 3]
copy1 = original       # 주소 공유
copy1[0] = 99
print(original)   # [99, 2, 3]  <- 원본도 바뀜!
print(copy1)      # [99, 2, 3]

# 올바른 복사 - 슬라이싱으로 새 리스트 생성
original = [1, 2, 3]
copy2 = original[:]    # 값 복사
copy2[0] = 99
print(original)   # [1, 2, 3]   <- 원본 유지
print(copy2)      # [99, 2, 3]
```

### 공백/쉼표 구분 다중 입력

```python
# 공백으로 구분된 두 정수
a, b = map(int, input().split())

# 쉼표로 구분
c, d = map(int, input().split(','))

# 개수 모르는 다중 정수를 리스트로
arr = list(map(int, input().split()))
```

### 점수 관리 종합

```python
scores = []

for i in range(5):
    scores.append(int(input(f"{i+1}번 점수: ")))

print("입력된 점수:", scores)
print("최고:", max(scores))
print("최저:", min(scores))

scores.remove(min(scores))
print("최저 제거 후 합계:", sum(scores))
```

### 2차원 리스트 선언/접근

```python
scores = [
    [80, 90, 85],    # 0번 학생
    [70, 65, 75],    # 1번 학생
    [100, 95, 90],   # 2번 학생
]

print(scores[1][1])   # 65 (1번 학생의 1번 과목)
print(scores[2])      # [100, 95, 90] (행 전체)
```

### 2차원 리스트 순회 (중첩 for)

```python
for row in scores:
    for value in row:
        print(value, end=" ")
    print()
```

### 단위행렬 생성 (중첩 for + 조건)

```python
n = 3
matrix = [[0] * n for _ in range(n)]

for i in range(n):
    for j in range(n):
        if i == j:
            matrix[i][j] = 1

print(matrix)   # [[1,0,0], [0,1,0], [0,0,1]]
```

### 중요사항
- `b = a`는 주소 복사(두 변수가 같은 리스트를 가리킴). 진짜 복사하려면 `b = a[:]` 또는 `b = list(a)`.
- `map(int, input().split())`은 입력 공백 분할 + 각 토막을 정수 변환. `list()`로 감싸면 리스트.
- 2차원 리스트는 `[행][열]` 순서로 접근. `arr[1][2]`는 1행 2열.
- 2차원 초기화 시 `[[0]*n]*n`은 **같은 행을 n번 참조**하는 함정이 있음. `[[0]*n for _ in range(n)]` 권장.
- `max()`, `min()`, `sum()`은 리스트/튜플 등 Iterable에 바로 적용 가능.

---

## 13차시. f-string / 함수

### f-string 기본과 내부 연산

```python
name = "파이썬"
age = 30
print(f"이름은 {name}, 나이는 {age}살")

# 딕셔너리 값, 연산도 중괄호 안에서 가능
menu_pan = {'떡볶이': 5000, '라면': 3000}
menu = '떡볶이'
count = 3
print(f"{menu} {count}인분 가격: {menu_pan[menu] * count}원")
```

### 사용자 정의 함수 (매개변수 + 반환값)

```python
def total(number):
    s = 0
    for i in range(1, number + 1):
        s += i
    return s

num = int(input("숫자: "))
result = total(num)
print(f"1부터 {num}까지의 합은 {result}")
```

### 약수 개수 탐지

```python
def divisor_count(n):
    cnt = 0
    for i in range(1, n + 1):
        if n % i == 0:
            cnt += 1
    return cnt

print(divisor_count(10))   # 4 (1, 2, 5, 10)
```

### 홀짝 판별 (문자열 반환)

```python
def check_even_odd(num):
    if num % 2 == 0:
        return "짝수"
    else:
        return "홀수"

print(check_even_odd(7))    # 홀수
print(check_even_odd(12))   # 짝수
```

### 지역/전역 변수 (global)

```python
apple = 10   # 전역

def eat_apple():
    global apple
    apple = 3
    print("함수 안:", apple)   # 3

eat_apple()
print("함수 밖:", apple)       # 3 (global 때문에 바뀜)

# global 없이 함수 안에서 apple = 3 하면
# 지역변수로 새로 만드는 것이라 밖의 apple은 10 유지
```

### 내장 함수 / 외장 함수

```python
print(abs(-15))            # 15 (절댓값)
print(divmod(10, 3))       # (3, 1) (몫, 나머지)
print(max([1, 2, 3, 4, 5]))
print(min([1, 2, 3, 4, 5]))
print(sum([1, 2, 3, 4, 5]))

import random
print(random.randint(1, 6))    # 1~6 무작위 정수
```

### 종합: 분식집 주문 프로그램

```python
total = 0
menu_pan = {'떡볶이': 5000, '라면': 3000, '순대': 4000, '콜라': 1500}

def show_menu():
    print('====<메뉴판>====')
    for name, price in menu_pan.items():
        print(f'{name}: {price}원')

def order():
    global total
    while True:
        m = input('메뉴 선택(n: 종료): ')
        if m == 'n':
            break
        if m in menu_pan:
            print(f'{m} 주문, {menu_pan[m]}원 추가')
            total += menu_pan[m]
        else:
            print('없는 메뉴')

def pay():
    print(f'총 {total}원')

while True:
    print('1.메뉴판  2.주문  3.결제  4.종료')
    a = int(input('선택: '))
    if a == 1:
        show_menu()
    elif a == 2:
        order()
    elif a == 3:
        pay()
    elif a == 4:
        break
```

### 중요사항
- f-string은 `f"..."` 형태. 중괄호 안에 변수·연산·딕셔너리 조회 모두 가능.
- 함수 정의는 `def 이름(매개변수):`, 반환은 `return 값`. `return` 없으면 `None` 반환.
- 매개변수(parameter)는 함수 정의 시, 인자(argument)는 호출 시 넘기는 값.
- **지역변수**는 함수 내부에서만 생존. **전역변수**는 함수 밖에서 선언, 안에서 읽기만 할 때는 그냥 사용 가능하지만 **값을 바꾸려면 `global` 선언** 필요.
- 내장함수: `len(), abs(), max(), min(), sum(), divmod(), print(), input(), int(), str(), list(), range(), map()`.
- 외장함수는 `import 모듈` 후 `모듈.함수()` 형태로 사용(`random.randint()` 등).
