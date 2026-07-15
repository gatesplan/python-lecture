# CNSH-122 기말고사 대비 자료 (2025)

이 폴더는 CNSH-122 과정의 기말고사 대비를 위한 학습 자료 모음입니다.

## 📚 폴더 구조

```
25-CNSH-122/
├── lectures/           # 강의 노트북 (4개: Lecture 4, 5, 6 + Backtracking)
├── sample-codes/       # 샘플 코드 (18개: 교과서 예제 14개 + CNSH 4개)
├── problem-xmls/       # 연습문제 XML 파일들 (7개)
└── README.md          # 이 파일 (학습 가이드)
```

## 📖 학습 범위

### 1. Lecture 4 - Recursive Hanoi Tower (재귀 함수 설계)
**파일**: `lectures/Python Apprentice Lecture 4 - Recursive Hanoi Tower.ipynb`

**주요 내용**:
- 재귀 함수 설계 방법
- 하노이 탑 문제
- 정렬 알고리즘 (선택, 버블, 퀵, 삽입)
- 재귀 함수의 기저 조건과 반복 패턴

**핵심 개념**:
- 재귀함수 설계 2단계: 반복되는 동작 찾기 + 기저 조건 찾기
- 콜스택 시각화

---

### 1-1. CNSH - Backtracking 이해 (백트래킹과 해밀토니안 경로)
**파일**: `lectures/CNSH - Backtracking 이해.ipynb`

**주요 내용**:
- 백트래킹 알고리즘의 이해
- 해밀토니안 경로 (Hamiltonian Path) 문제
- 전역 변수 vs 파라미터 설계
- 재귀 함수의 파라미터 역할 분석
- 함수 분해와 리팩토링

**핵심 개념**:
- 백트래킹 패턴: 선택 → 진행 → 되돌리기
- `visited` 배열 관리 (True/False 쌍)
- 경로 리스트 관리 (append/pop 쌍)
- 가중치가 있는 그래프에서 최소 비용 경로 찾기

---

### 2. Lecture 5 - BTree Traversing (이진 트리 순회)
**파일**: `lectures/Python Apprentice Lecture 5 - BTree Traversing.ipynb`

**주요 내용**:
- 이진 트리의 개념과 종류
- 트리 순회 알고리즘 (전위, 중위, 후위, 레벨 순서)
- LCA (최소 공통 조상)
- 두 노드 사이의 거리 계산
- 트리의 직경

**핵심 개념**:
- 전위 순회: 루트 → 왼쪽 → 오른쪽
- 중위 순회: 왼쪽 → 루트 → 오른쪽
- 후위 순회: 왼쪽 → 오른쪽 → 루트
- 레벨 순서: BFS (너비 우선 탐색)
- 배열 표현에서 부모-자식 관계: `parent = i//2`, `left = 2*i`, `right = 2*i+1`

---

### 3. Lecture 6 - Time Complexity and Big-O Notation (시간복잡도)
**파일**: `lectures/Python Apprentice Lecture 6 - Time Complexity and Big-O Notation.ipynb`

**주요 내용**:
- 시간복잡도의 필요성
- 빅O 표기법
- 주요 복잡도 클래스 (O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ))
- 코드 분석 방법
- 정렬 알고리즘의 시간복잡도 비교

**핵심 개념**:
- O(1): 상수 시간 (배열 접근, 딕셔너리 조회)
- O(log n): 로그 시간 (이진 탐색, 절반씩 줄이기)
- O(n): 선형 시간 (단일 반복문)
- O(n log n): 선형로그 시간 (병합 정렬, 퀵 정렬 평균)
- O(n²): 이차 시간 (중첩 반복문)
- O(2ⁿ): 지수 시간 (재귀 피보나치)

---

## 🧪 연습문제 (config-cnsh122-1102.xml)

### Section 1: Stair Down (계단 내려가기 - 재귀/for 변환)
**문제 파일**: `problems-cnsh122-stairdown.xml`
- 재귀 함수와 반복문 변환 연습

### Section 2: Is Prime (소수 판별)
**문제 파일**: `problems-cnsh122-isprime.xml`
- 소수 판별 알고리즘

### Section 3: Count Primes (소수 개수 세기)
**문제 파일**: `problems-cnsh122-countprimes.xml`
- 범위 내 소수 개수 세기

### Section 4: GCD (최대공약수)
**문제 파일**: `problems-cnsh122-gcd.xml`
- 유클리드 호제법
- 최대공약수 구하기

### Section 5: Find Coprime (서로소 찾기)
**문제 파일**: `problems-cnsh122-findcoprime.xml`
- 서로소 관계 찾기
- GCD 응용

### Section 6: Recursive Select 3 (재귀 조합)
**문제 파일**: `problems-cnsh122-recursive-select3.xml`
- 재귀를 이용한 조합 선택

---

## 💻 샘플 코드

`sample-codes/` 폴더에는 실습 및 참고용 코드들이 포함되어 있습니다.

### 교과서 예제 코드 (Test.ipynb에서 추출)

#### 재귀 및 조합 문제
1. **`01-number-addition-permutation.py`** - 숫자 덧셈 순열 (재귀)
   - 재귀 함수의 기저 조건과 재귀 호출 이해

2. **`02-fibonacci-path-count.py`** - 피보나치 경로 개수 (p176)
   - 0에서 출발하여 1 또는 2를 더해 n에 도달하는 경우의 수

#### 소수 관련 알고리즘
3. **`03-count-primes-basic.py`** - 소수 개수 세기 기본 (p181)
   - 시간복잡도: O(n²)

4. **`04-count-primes-optimized.py`** - 소수 개수 세기 최적화 (p187)
   - 제곱근까지만 확인, 시간복잡도: O(n × √n)

#### 서로소와 GCD
5. **`05-check-coprime-simple.py`** - 서로소 판별 (간단한 방법)
   - 공약수 존재 여부 확인

6. **`06-count-coprimes-euclidean.py`** - 서로소 개수 세기 (p182)
   - 유클리드 호제법 활용

#### 조합 및 백트래킹
7. **`07-max-sum-divisible-by-3.py`** - 3개 더해서 3의 배수 최댓값 (p183)
   - 재귀적 조합 탐색

8. **`08-count-sum-divisible-by-3.py`** - 3개 더해서 3의 배수 경우의 수 (p184)
   - 조합 경우의 수 계산

#### 분기 한정법 (Branch and Bound)
9. **`09-partition-count-branch-and-bound.py`** - 자연수 합 순열 개수 (p190)
   - 분기 한정법으로 가지치기 최적화

10. **`10-subset-sum-count.py`** - 부분집합 합 경우의 수 (p191)
    - 주어진 숫자들로 특정 합 만들기

#### 동전 문제 (동적계획법 vs 탐욕법)
11. **`11-coin-change-backtracking.py`** - 동전 최소 개수 (백트래킹, p195)
    - 모든 경우의 수 탐색 + 가지치기

12. **`12-coin-change-greedy.py`** - 동전 최소 개수 (탐욕법)
    - 큰 동전부터 최대한 사용, O(k)

#### 기타 알고리즘
13. **`13-sum-of-divisors.py`** - 약수의 합
    - 기본 방법 O(n), 최적화 방법 O(√n)

#### 해밀토니안 경로 (Hamiltonian Path) - 백트래킹
14. **`14-hamiltonian-path-detailed.py`** - 해밀토니안 경로 (상세 설명 버전)
    - 모든 노드를 한 번씩 방문하는 경로 찾기
    - 가중치 합이 최소인 경로 구하기
    - 백트래킹 알고리즘: 선택 → 진행 → 되돌리기
    - `visited` 배열과 경로 리스트 관리
    - 시간복잡도: O(V!)

### CNSH 샘플 코드
- **`1413-LJ-075.py`** - 샘플 코드 75
- **`1413-LJ-076.py`** - 샘플 코드 76
- **`1413-LJ-077.py`** - 해밀토니안 경로 (가중치 있는 버전)
- **`1413-LJ-077-refactored.py`** - 해밀토니안 경로 (리팩토링 버전)

---

## 📝 학습 방법

1. **강의 노트북 복습** (lectures/)
   - Lecture 4, 5, 6을 순서대로 복습
   - 각 코드 예제를 직접 실행하며 이해

2. **연습문제 풀이** (problem-xmls/)
   - config-cnsh122-1102.xml의 각 섹션별 문제 풀이
   - 문제를 보려면 problem-renderer 사용

3. **샘플 코드 분석** (sample-codes/)
   - 제공된 샘플 코드 분석 및 이해

---

## 🎯 중요 체크포인트

### 재귀 함수 (Lecture 4)
- [ ] 재귀 함수의 기저 조건과 재귀 호출 이해
- [ ] 하노이 탑 문제 해결 과정 이해
- [ ] 재귀 정렬 알고리즘 (선택, 버블, 삽입, 퀵) 구현 가능

### 이진 트리 (Lecture 5)
- [ ] 배열 표현에서 부모-자식 인덱스 관계 이해
- [ ] 4가지 순회 방법 (전위, 중위, 후위, 레벨) 구현 가능
- [ ] LCA 알고리즘 이해 및 구현
- [ ] 두 노드 사이 거리 계산 가능

### 시간복잡도 (Lecture 6)
- [ ] 코드를 보고 시간복잡도 분석 가능
- [ ] 주요 복잡도 클래스 구별 가능
- [ ] 정렬 알고리즘의 시간복잡도 이해
- [ ] 빅O 표기법의 규칙 이해 (상수 무시, 최고차항)

### 연습문제 주제
- [ ] 재귀/반복문 변환
- [ ] 소수 판별 및 개수 세기
- [ ] GCD (최대공약수) 및 서로소
- [ ] 재귀 조합 선택

### 샘플 코드 주제
- [ ] 재귀 함수 설계 (순열, 피보나치)
- [ ] 소수 판별 (기본 O(n²) vs 최적화 O(n√n))
- [ ] 유클리드 호제법 (GCD, 서로소)
- [ ] 백트래킹 (조합, 분기 한정법)
- [ ] 동전 문제 (백트래킹 vs 탐욕법)
- [ ] 약수 계산 (기본 O(n) vs 최적화 O(√n))
- [ ] 해밀토니안 경로 (백트래킹, 가중치 있는 그래프)

---

## 🔗 관련 자료

### Problem Renderer 사용법
```bash
cd "C:\Projects\python-lecture\lecture-basic\problem-renderer"
start.bat
# 브라우저에서: http://localhost:8000?config=config-cnsh122-1102
```

### 원본 파일 위치
- 강의 노트북: `lecture-apprentice/`
- 샘플 코드: `codes/cnsh-sample/`
- 문제 XML: `lecture-basic/problem-renderer/problem-xmls/`

---

**작성일**: 2025-11-09
**과목**: CNSH-122 Python Programming
**목적**: 기말고사 대비 학습 자료 통합
