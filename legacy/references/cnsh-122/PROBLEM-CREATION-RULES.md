# Problems XML 파일 제작 규칙

**작성일**: 2025-11-09
**목적**: 일관된 품질의 문제 XML 파일 제작을 위한 표준 규칙

---

## 📋 기본 원칙

### 1. 학습 철학
- ❌ **힌트를 주지 않는다** - 공부용이므로 스스로 생각하게 함
- ✅ **해설에서만 설명** - solution 필드에 자세한 주석 제공
- ✅ **점진적 난이도** - 쉬운 문제부터 어려운 문제로
- ✅ **반복 학습** - 유사한 패턴을 여러 문제로 강화

### 2. 코드 스타일
- **함수명**: `f` (단순화)
- **변수명**: `n`, `k`, `x`, `y`, `a`, `b`, `i`, `j` 등 1-2글자
- **전역변수**: 필요시 `ans`, `visited`, `M` 등 의미 있는 이름 허용
- **주석**: 문제 코드에는 주석 없음 (solution에만)
- **들여쓰기**: 4칸 스페이스

---

## 🏗️ XML 구조

### 기본 템플릿
```xml
<?xml version="1.0" encoding="UTF-8"?>
<problems>
  <!-- 문제 1: 간단한 설명 -->
  <problem>
    <description>문제 설명 (한글)</description>
    <code><![CDATA[코드 내용]]></code>
    <input><![CDATA[입력 예시 (선택)]]></input>
    <output><![CDATA[출력 예시 (선택)]]></output>
    <solution><![CDATA[정답 코드 + 주석 설명]]></solution>
  </problem>

  <!-- 문제 2: ... -->
  <!-- ... -->
</problems>
```

### 필드별 규칙

#### `<description>` (필수)
- **목적**: 문제 지문
- **규칙**:
  - 한글로 작성
  - 1-3문장 정도로 간결하게
  - 무엇을 완성해야 하는지 명확히 명시
  - 예: "다음 코드는 소수를 판별하는 함수입니다. if문의 조건부를 완성하세요."
  - 예: "계단을 한 번에 1칸 또는 2칸씩 내려갈 수 있을 때, n칸 계단을 내려가는 방법의 수를 재귀함수로 구현하세요."

#### `<code>` (필수)
- **목적**: 문제 코드
- **규칙**:
  - 항상 `<![CDATA[...]]>` 사용
  - 주석 없음 (절대 금지)
  - 빈칸은 `____` (언더스코어 4개)
  - 전체 작성 문제는 `pass` 사용
  - 들여쓰기 정확하게

**빈칸 채우기 예시**:
```python
def f(n):
    if ____:  # 여기를 채우세요
        return 1
    return f(n-1) + f(n-2)
```

**전체 작성 예시**:
```python
def f(n):
    pass  # 여기를 채우세요
```

**블록 채우기 예시**:
```python
for i in range(2, n+1):
    # 여기를 채우세요
```

#### `<input>` (선택)
- **목적**: 테스트 케이스 입력
- **규칙**:
  - `<![CDATA[...]]>` 사용
  - 실행 가능한 파이썬 코드
  - 보통 `print(f(...))` 형태
  - 여러 테스트 케이스 가능
  - 없으면 빈 태그: `<input></input>`

**예시**:
```xml
<input><![CDATA[print(f(4))
print(f(3))]]></input>
```

#### `<output>` (선택)
- **목적**: 예상 출력
- **규칙**:
  - `<![CDATA[...]]>` 사용
  - 실제 실행 결과와 일치해야 함
  - 여러 줄 가능
  - 없으면 빈 태그: `<output></output>`

**예시**:
```xml
<output><![CDATA[5
3]]></output>
```

#### `<solution>` (필수)
- **목적**: 정답 코드 + 설명
- **규칙**:
  - `<![CDATA[...]]>` 사용
  - **여기에만 주석 허용** (해설 역할)
  - 빈칸의 정답은 주석으로 명시: `# 정답: ...`
  - 코드 전체 + 설명 주석
  - 왜 그런지 간단히 설명

**빈칸 정답 예시**:
```xml
<solution><![CDATA[def f(n):
    if n == 1:  # 정답: n == 1
        return 1
    return f(n-1) + f(n-2)]]></solution>
```

**서술형 정답 예시**:
```xml
<solution><![CDATA[# 파라미터 의미:
# k: 현재까지 탐색한 인덱스
# s: 현재까지 선택한 숫자들의 합
# j: 현재까지 선택한 숫자의 개수 (깊이)]]></solution>
```

**전체 작성 정답 예시**:
```xml
<solution><![CDATA[def f(n):
    # 기저 조건: n이 1이면 1 반환
    if n == 1:
        return 1
    if n == 2:
        return 2
    # 재귀: f(n-1) + f(n-2)
    return f(n-1) + f(n-2)]]></solution>
```

---

## 🎯 문제 유형

### 1. 빈칸 채우기 (가장 많이 사용)
**난이도**: 하~중
**비율**: 40-50%

**패턴**:
- if 조건식 채우기
- 연산자 채우기 (`+`, `*`, `%` 등)
- 변수명 채우기
- 재귀 호출 파라미터 채우기

**예시**:
```xml
<problem>
  <description>소수를 판별하는 함수입니다. if문의 조건부를 완성하세요.</description>
  <code><![CDATA[def f(k):
    for i in range(2, int(k**0.5)+1):
        if ____:
            return False
    return True]]></code>
  <input><![CDATA[print(f(13))
print(f(15))]]></input>
  <output><![CDATA[True
False]]></output>
  <solution><![CDATA[def f(k):
    for i in range(2, int(k**0.5)+1):
        if (k%i) == 0:  # 정답: (k%i) == 0 또는 k%i == 0
            return False
    return True]]></solution>
</problem>
```

### 2. 블록 채우기
**난이도**: 중
**비율**: 20-30%

**패턴**:
- for 내부 블록 작성
- if 내부 블록 작성
- 재귀 호출 전후 처리

**예시**:
```xml
<problem>
  <description>최대공약수를 구하는 코드입니다. for 반복문 내부를 완성하세요.</description>
  <code><![CDATA[x, y = 10, 15
a, b = min(x, y), max(x, y)
gcd = 1

for i in range(2, a+1):
    # 여기를 채우세요

print(gcd)]]></code>
  <solution><![CDATA[x, y = 10, 15
a, b = min(x, y), max(x, y)
gcd = 1

for i in range(2, a+1):
    if a%i == 0 and b%i == 0:
        gcd = i

print(gcd)]]></solution>
</problem>
```

### 3. 전체 함수 작성
**난이도**: 중~상
**비율**: 20-30%

**패턴**:
- `def f(...):\n    pass`로 시작
- 함수 전체를 구현
- description에 자세한 설명

**예시**:
```xml
<problem>
  <description>주어진 수 k가 소수인지 판별하는 함수를 작성하세요. 2부터 k의 제곱근까지 확인하여 나누어떨어지는 수가 없으면 True, 있으면 False를 반환합니다.</description>
  <code><![CDATA[def f(k):
    pass  # 여기를 채우세요]]></code>
  <input><![CDATA[print(f(29))
print(f(30))]]></input>
  <output><![CDATA[True
False]]></output>
  <solution><![CDATA[def f(k):
    for i in range(2, int(k**0.5)+1):
        if (k%i) == 0:
            return False
    return True]]></solution>
</problem>
```

### 4. 서술형 (개념 확인)
**난이도**: 하~중
**비율**: 5-10%

**패턴**:
- 파라미터 의미 서술
- 코드 목적 서술
- 알고리즘 설명
- 시간복잡도 분석

**예시**:
```xml
<problem>
  <description>다음 재귀 함수 f의 세 파라미터 k, s, j가 각각 무엇을 의미하는지 서술하세요.</description>
  <code><![CDATA[def f(k, s, j):
    if j == 3:
        if (s%3) == 0:
            global ans
            ans = max(ans, s)
        return

    for i in range(k+1, 8):
        f(i, s+A[i], j+1)]]></code>
  <input></input>
  <output></output>
  <solution><![CDATA[# 파라미터 의미:
# k: 현재까지 탐색한 인덱스 (마지막으로 선택한 원소의 인덱스)
# s: 현재까지 선택한 숫자들의 합
# j: 현재까지 선택한 숫자의 개수 (깊이)]]></solution>
</problem>
```

---

## 📊 파일당 구성

### 문제 개수
- **권장**: 6-8개
- **최소**: 4개
- **최대**: 10개

### 난이도 분포 (파일 내)
```
쉬움 (30%): 빈칸 1개, 단순 조건
보통 (40%): 빈칸 2-3개, 블록 채우기
어려움 (30%): 전체 작성, 복잡한 로직
```

### 문제 순서
1. **워밍업**: 가장 쉬운 문제 (빈칸 1개)
2. **기본**: 점진적으로 난이도 증가
3. **응용**: 전체 작성 또는 복잡한 변형
4. **심화**: 서술형 또는 최고 난이도

**예시 구성** (소수 판별 파일):
1. if 조건 1개 채우기
2. for 범위 + if 조건 채우기
3. 전체 함수 작성
4. 최적화 버전 (√n) 작성
5. 시간복잡도 비교 서술
6. 응용 (n 이하 소수 개수)

---

## ⚠️ 금지 사항

### 절대 하지 말 것
1. ❌ **힌트 필드 사용 금지** - `<hint></hint>` 항상 비움
2. ❌ **문제 코드에 주석 금지** - 학습을 방해함
3. ❌ **불필요한 설명 금지** - description은 간결하게
4. ❌ **모호한 지시 금지** - "적절히", "알맞게" 같은 표현 지양
5. ❌ **복잡한 변수명 금지** - `stairCount` → `n`, `current_sum` → `s`

### 주의 사항
- ⚠️ **CDATA 누락 주의** - 모든 코드는 CDATA로 감싸기
- ⚠️ **들여쓰기 주의** - 4칸 스페이스 일관되게
- ⚠️ **빈칸 개수 주의** - `____` (언더스코어 정확히 4개)
- ⚠️ **테스트 검증 필수** - input/output이 실제 실행 결과와 일치하는지 확인

---

## ✅ 품질 체크리스트

### 제작 전 확인
- [ ] 파일명이 규칙을 따르는가? `problems-cnsh122-{n}-{title}.xml`
- [ ] 주제가 명확한가?
- [ ] 난이도가 적절한가?
- [ ] 6-8개 문제를 구성할 수 있는가?

### 제작 중 확인
- [ ] 모든 코드가 CDATA로 감싸져 있는가?
- [ ] 문제 코드에 주석이 없는가?
- [ ] 빈칸이 `____`로 표시되어 있는가?
- [ ] 변수명이 단순화되어 있는가?
- [ ] 함수명이 `f`인가?

### 제작 후 확인
- [ ] 모든 문제가 XML 문법상 올바른가?
- [ ] solution에 정답 주석이 있는가?
- [ ] input/output이 실제 실행 결과와 일치하는가?
- [ ] description이 명확한가?
- [ ] 난이도 순서가 적절한가?

### 최종 검증
- [ ] Problem Renderer로 실제 렌더링 확인
- [ ] 각 문제를 직접 풀어보기
- [ ] 오타 및 문법 오류 확인
- [ ] 다른 문제와 중복되지 않는가?

---

## 🎨 예시: 완성된 문제 XML

### 좋은 예시 ✅
```xml
<?xml version="1.0" encoding="UTF-8"?>
<problems>
  <!-- 문제 1: if 조건 채우기 -->
  <problem>
    <description>팩토리얼을 구하는 재귀함수입니다. 기저 조건을 완성하세요.</description>
    <code><![CDATA[def f(n):
    if ____:
        return 1
    return n * f(n-1)]]></code>
    <input><![CDATA[print(f(5))
print(f(3))]]></input>
    <output><![CDATA[120
6]]></output>
    <solution><![CDATA[def f(n):
    if n == 0:  # 정답: n == 0 또는 n <= 0
        return 1
    return n * f(n-1)]]></solution>
  </problem>

  <!-- 문제 2: 재귀 호출 채우기 -->
  <problem>
    <description>팩토리얼을 구하는 재귀함수입니다. return 부분을 완성하세요.</description>
    <code><![CDATA[def f(n):
    if n == 0:
        return 1
    return ____]]></code>
    <input><![CDATA[print(f(4))
print(f(6))]]></input>
    <output><![CDATA[24
720]]></output>
    <solution><![CDATA[def f(n):
    if n == 0:
        return 1
    return n * f(n-1)  # 정답: n * f(n-1)]]></solution>
  </problem>
</problems>
```

### 나쁜 예시 ❌
```xml
<problems>
  <!-- 이건 나쁜 예시입니다 -->
  <problem>
    <description>다음 코드를 완성하세요.</description>  <!-- ❌ 너무 모호함 -->
    <code><![CDATA[def factorial(n):  # ❌ 함수명이 길고 명확함
    # n의 팩토리얼을 구합니다  ❌ 주석이 있음
    if n == 0:
        return 1
    return ____]]></code>
    <hint>재귀 호출을 사용하세요</hint>  <!-- ❌ 힌트 사용 금지 -->
    <solution><![CDATA[def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)]]></solution>  <!-- ❌ 주석 설명 없음 -->
  </problem>
</problems>
```

---

## 📚 참고: 기존 파일 분석 결과

### 통계
- **stairdown.xml**: 4문제 (재귀 기초)
- **isprime.xml**: 추정 4-6문제 (소수 판별)
- **gcd.xml**: 8문제 (최대공약수)
- **recursive-select3.xml**: 8문제 (조합 선택)

### 공통 패턴
1. 파라미터 의미 서술로 시작 (개념 확인)
2. 빈칸 1개 → 빈칸 2-3개 → 전체 작성
3. 같은 코드를 다른 부분 채우기로 반복
4. 마지막에 응용 문제

---

**작성**: 2025-11-09
**버전**: 1.0
**적용 범위**: problems-cnsh122-*.xml 모든 파일
