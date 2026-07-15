# 새로운 문제 유형 제안

**작성일**: 2025-11-09
**목적**: 기존 4가지 유형을 넘어서는 창의적이고 효과적인 문제 유형 개발

---

## 🆕 제안하는 새 유형

### 1. 디버깅 문제 ⭐⭐⭐ (강력 추천)
**난이도**: 중~상
**학습 효과**: ★★★★★
**시험 적합성**: ★★★★★

#### 개념
잘못된 코드를 찾아서 고치는 문제. 실무에서 가장 많이 하는 작업이며, 코드 이해도를 정확히 평가할 수 있음.

#### 예시 1: 논리 오류
```xml
<problem>
  <description>다음 소수 판별 함수에는 논리적 오류가 있습니다. 잘못된 부분을 찾아 올바르게 고치세요.</description>
  <code><![CDATA[def f(k):
    for i in range(2, k):
        if (k%i) != 0:
            return False
    return True]]></code>
  <input><![CDATA[print(f(7))
print(f(9))]]></input>
  <output><![CDATA[False
False]]></output>
  <solution><![CDATA[def f(k):
    for i in range(2, k):
        if (k%i) == 0:  # 오류: != 0이 아니라 == 0이어야 함
            return False
    return True

# 잘못된 부분: if (k%i) != 0 → if (k%i) == 0
# 이유: 나누어떨어지면 소수가 아니므로 == 0일 때 False 반환]]></solution>
</problem>
```

#### 예시 2: 재귀 오류
```xml
<problem>
  <description>다음 팩토리얼 함수는 무한 재귀에 빠집니다. 오류를 찾아 고치세요.</description>
  <code><![CDATA[def f(n):
    if n == 1:
        return 1
    return n * f(n)]]></code>
  <solution><![CDATA[def f(n):
    if n == 1:
        return 1
    return n * f(n-1)  # 오류: f(n)이 아니라 f(n-1)이어야 함

# 잘못된 부분: f(n) → f(n-1)
# 이유: n을 감소시키지 않으면 무한 재귀]]></solution>
</problem>
```

#### 장점
- ✅ 실제 코딩에서 가장 중요한 능력
- ✅ 알고리즘 이해도를 정확히 평가
- ✅ 단순 암기가 아닌 사고력 평가
- ✅ 난이도 조절이 쉬움 (오류 종류 조절)

---

### 2. 트레이싱 문제 (실행 과정 추적) ⭐⭐⭐
**난이도**: 중
**학습 효과**: ★★★★★
**시험 적합성**: ★★★★☆

#### 개념
코드 실행 과정을 단계별로 따라가며 중간값이나 최종 결과를 예측하는 문제. 재귀 함수 이해에 특히 효과적.

#### 예시 1: 재귀 트레이싱
```xml
<problem>
  <description>다음 재귀 함수 f(3)을 실행할 때, f 함수가 총 몇 번 호출되는지 구하세요.</description>
  <code><![CDATA[def f(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return f(n-1) + f(n-2)]]></code>
  <input></input>
  <output></output>
  <solution><![CDATA[# f(3) 호출 추적:
# f(3) = f(2) + f(1)
#   f(2) = f(1) + f(0)
#     f(1) = 1
#     f(0) = 0
#   f(1) = 1
#
# 총 호출: f(3), f(2), f(1), f(0), f(1) = 5번
# 정답: 5번]]></solution>
</problem>
```

#### 예시 2: 변수 추적
```xml
<problem>
  <description>다음 코드를 실행한 후 x, y의 값을 구하세요.</description>
  <code><![CDATA[x, y = 10, 15
a, b = min(x, y), max(x, y)

while a != b:
    if a > b:
        a = a - b
    else:
        b = b - a

x = a
y = b]]></code>
  <solution><![CDATA[# 실행 과정:
# 초기: x=10, y=15, a=10, b=15
# 1회: a=10, b=5 (b = 15-10)
# 2회: a=5, b=5 (a = 10-5)
# 종료: a=5, b=5
# 최종: x=5, y=5
#
# 정답: x=5, y=5 (최대공약수)]]></solution>
</problem>
```

#### 장점
- ✅ 재귀 함수 이해에 필수적
- ✅ 논리적 사고력 강화
- ✅ 알고리즘 동작 원리 파악
- ✅ 백트래킹 학습에 효과적

---

### 3. 출력 예측 문제 ⭐⭐⭐
**난이도**: 하~중
**학습 효과**: ★★★★☆
**시험 적합성**: ★★★★★

#### 개념
완성된 코드를 보고 실행 결과를 예측. 빠르게 풀 수 있고 이해도 확인에 효과적.

#### 예시 1: 단순 예측
```xml
<problem>
  <description>다음 코드의 출력 결과를 쓰세요.</description>
  <code><![CDATA[def f(n):
    if n <= 1:
        return 1
    return n * f(n-1)

print(f(4))]]></code>
  <input></input>
  <output><![CDATA[24]]></output>
  <solution><![CDATA[# f(4) = 4 * f(3)
#      = 4 * 3 * f(2)
#      = 4 * 3 * 2 * f(1)
#      = 4 * 3 * 2 * 1
#      = 24
#
# 정답: 24]]></solution>
</problem>
```

#### 예시 2: 트리 순회 출력
```xml
<problem>
  <description>다음 전위 순회 코드의 출력 결과를 쓰세요. (배열 s = "-ABC-EFG")</description>
  <code><![CDATA[s = "-ABC-EFG"

def f(node):
    if node >= len(s) or s[node] == '-':
        return
    print(s[node], end=' ')
    f(node * 2)
    f(node * 2 + 1)

f(1)]]></code>
  <output><![CDATA[A B E F C G]]></output>
  <solution><![CDATA[# 전위 순회: 루트 → 왼쪽 → 오른쪽
# s = "-ABC-EFG"
#     A(1)
#    / \
#  B(2) C(3)
#  / \  / \
# E(4)F(5)G(6)
#
# 순서: A → B → E → F → C → G
# 정답: A B E F C G]]></solution>
</problem>
```

#### 장점
- ✅ 빠른 문제 해결 (객관식 가능)
- ✅ 시험 시간 효율적
- ✅ 명확한 정답
- ✅ 자동 채점 가능

---

### 4. 코드 비교 문제 ⭐⭐
**난이도**: 중~상
**학습 효과**: ★★★★☆
**시험 적합성**: ★★★☆☆

#### 개념
두 개 이상의 코드를 비교하여 차이점, 효율성, 정확성을 판단.

#### 예시 1: 효율성 비교
```xml
<problem>
  <description>다음 두 소수 판별 함수 중 더 효율적인 것은? 그 이유는?</description>
  <code><![CDATA[# 코드 A
def f(k):
    for i in range(2, k):
        if (k%i) == 0:
            return False
    return True

# 코드 B
def f(k):
    for i in range(2, int(k**0.5)+1):
        if (k%i) == 0:
            return False
    return True]]></code>
  <solution><![CDATA[# 정답: 코드 B가 더 효율적
#
# 이유:
# - 코드 A: O(n) - 2부터 k-1까지 모두 확인
# - 코드 B: O(√n) - 2부터 √k까지만 확인
#
# k = 100일 때:
# - 코드 A: 98번 확인
# - 코드 B: 8번 확인 (√100 = 10)
#
# 약수는 √k를 기준으로 대칭이므로 √k까지만 확인하면 충분]]></solution>
</problem>
```

#### 예시 2: 동작 차이
```xml
<problem>
  <description>다음 두 코드의 차이점을 설명하세요.</description>
  <code><![CDATA[# 코드 A
def f(n):
    if n == 0:
        return 1
    return n * f(n-1)

# 코드 B
def f(n):
    if n <= 0:
        return 1
    return n * f(n-1)]]></code>
  <solution><![CDATA[# 차이점: 기저 조건이 다름
#
# 코드 A: n == 0
# - f(0) = 1
# - f(-1)은 무한 재귀 (오류)
#
# 코드 B: n <= 0
# - f(0) = 1
# - f(-1) = 1 (안전)
#
# 결론: 코드 B가 더 안전 (음수 입력 처리)]]></solution>
</problem>
```

#### 장점
- ✅ 비판적 사고력 향상
- ✅ 최적화 감각 습득
- ✅ 실무적 능력

#### 단점
- ⚠️ 채점이 주관적일 수 있음
- ⚠️ 시간이 많이 걸림

---

### 5. 조건 역추론 문제 ⭐⭐
**난이도**: 중~상
**학습 효과**: ★★★☆☆
**시험 적합성**: ★★★☆☆

#### 개념
원하는 출력을 만들기 위한 입력값이나 조건을 찾는 문제.

#### 예시
```xml
<problem>
  <description>다음 함수에서 f(n) = 21이 되도록 하는 n의 값을 구하세요.</description>
  <code><![CDATA[def f(n):
    if n <= 1:
        return 1
    return n * f(n-1)]]></code>
  <solution><![CDATA[# f(n) = 21을 만족하는 n 찾기
#
# 팩토리얼 계산:
# f(1) = 1
# f(2) = 2
# f(3) = 6
# f(4) = 24
#
# 하지만 21은 팩토리얼 값이 아님
# 정답: 없음 (팩토리얼은 1, 2, 6, 24, ...만 가능)]]></solution>
</problem>
```

---

### 6. 순서 맞추기 문제 ⭐
**난이도**: 중
**학습 효과**: ★★★☆☆
**시험 적합성**: ★★☆☆☆

#### 개념
뒤섞인 코드 줄을 올바른 순서로 배열.

#### 예시
```xml
<problem>
  <description>다음 소수 판별 함수의 줄들을 올바른 순서로 배열하세요. (1-5번)</description>
  <code><![CDATA[1. return True
2. for i in range(2, int(k**0.5)+1):
3. def f(k):
4. if (k%i) == 0:
5. return False]]></code>
  <solution><![CDATA[# 올바른 순서: 3 → 2 → 4 → 5 → 1
#
# def f(k):
#     for i in range(2, int(k**0.5)+1):
#         if (k%i) == 0:
#             return False
#     return True]]></solution>
</problem>
```

#### 단점
- ⚠️ 제작이 번거로움
- ⚠️ XML 형식에 맞추기 어려움

---

### 7. 복잡도 분석 문제 ⭐⭐⭐ (강력 추천)
**난이도**: 중~상
**학습 효과**: ★★★★★
**시험 적합성**: ★★★★★

#### 개념
주어진 코드의 시간복잡도를 분석. Lecture 6 내용과 직접 연결.

#### 예시 1: 단순 분석
```xml
<problem>
  <description>다음 코드의 시간복잡도를 Big-O 표기법으로 나타내세요.</description>
  <code><![CDATA[def f(n):
    for i in range(n):
        for j in range(n):
            print(i, j)]]></code>
  <solution><![CDATA[# 분석:
# - 외부 루프: n번 반복
# - 내부 루프: 각각 n번 반복
# - 총 연산: n × n = n²
#
# 정답: O(n²)]]></solution>
</problem>
```

#### 예시 2: 재귀 복잡도
```xml
<problem>
  <description>다음 피보나치 함수의 시간복잡도를 구하세요.</description>
  <code><![CDATA[def f(n):
    if n <= 1:
        return n
    return f(n-1) + f(n-2)]]></code>
  <solution><![CDATA[# 분석:
# - 매번 2개의 재귀 호출
# - 트리 높이: n
# - 노드 개수: 약 2^n
#
# 정답: O(2^n)
#
# 참고: 메모이제이션 사용 시 O(n)으로 개선 가능]]></solution>
</problem>
```

#### 장점
- ✅ Lecture 6과 직접 연결
- ✅ 알고리즘 선택 능력 배양
- ✅ 실무 필수 능력
- ✅ 명확한 정답

---

## 📊 유형별 종합 평가

| 유형 | 난이도 | 학습효과 | 시험적합 | 제작난이 | 추천도 |
|------|-------|---------|---------|---------|-------|
| **디버깅** | 중~상 | ★★★★★ | ★★★★★ | 중 | ⭐⭐⭐ |
| **트레이싱** | 중 | ★★★★★ | ★★★★☆ | 중 | ⭐⭐⭐ |
| **출력예측** | 하~중 | ★★★★☆ | ★★★★★ | 하 | ⭐⭐⭐ |
| **코드비교** | 중~상 | ★★★★☆ | ★★★☆☆ | 중상 | ⭐⭐ |
| **조건역추론** | 중~상 | ★★★☆☆ | ★★★☆☆ | 중 | ⭐⭐ |
| **순서맞추기** | 중 | ★★★☆☆ | ★★☆☆☆ | 상 | ⭐ |
| **복잡도분석** | 중~상 | ★★★★★ | ★★★★★ | 중 | ⭐⭐⭐ |

---

## 💡 적용 제안

### 최우선 도입 (강력 추천)
1. **디버깅 문제** - 각 파일마다 1-2개
2. **출력 예측** - 워밍업용으로 1개씩
3. **복잡도 분석** - Level 6 파일에 집중 배치

### 선택적 도입
4. **트레이싱** - 재귀 파일(01, 07, 16)에 적합
5. **코드 비교** - 소수/정렬 최적화 파일에 적합

### 보류
- **조건 역추론** - 제작 시간 대비 효과 낮음
- **순서 맞추기** - XML 형식에 부적합

---

## 🎯 파일별 적용 예시

### problems-cnsh122-03-isprime.xml
```
1. 빈칸 채우기 (if 조건)
2. 출력 예측 ⭐ NEW
3. 전체 함수 작성
4. 디버깅 (논리 오류) ⭐ NEW
5. 코드 비교 (최적화) ⭐ NEW
6. 복잡도 분석 ⭐ NEW
```

### problems-cnsh122-16-hamiltonian.xml
```
1. 파라미터 의미 서술
2. 출력 예측 (경로) ⭐ NEW
3. 빈칸 채우기 (visited 관리)
4. 트레이싱 (경로 추적) ⭐ NEW
5. 디버깅 (백트래킹 오류) ⭐ NEW
6. 전체 함수 작성
```

---

## 🔧 제작 가이드라인

### 디버깅 문제 만들 때
- 학생들이 자주 하는 실수 활용
- 논리 오류 > 문법 오류
- 너무 명백한 오류는 지양

### 출력 예측 만들 때
- 간단한 입력으로
- 손으로 추적 가능한 범위
- 객관식 선택지 추가 가능

### 복잡도 분석 만들 때
- 연산 횟수를 구체적으로 설명
- O(1), O(log n), O(n), O(n²), O(2^n) 위주
- 최선/평균/최악 구분

---

**작성**: 2025-11-09
**버전**: 1.0
