# Python Basic Learning Steps

이 문서는 lecture-basic 디렉토리의 문제 파일들을 학습 순서대로 정리한 목록입니다.

## 1. 출력 및 기본 문법

### 1.1 변수 선언과 기본 출력
- **problems-print.xml** (10문제)
  - 변수 선언 및 기본 print() 함수 사용
  - `print(변수명)`, `print(a, b)` 등 기초 출력

### 1.2 출력 파라미터 - sep
- **problems-print-sep.xml** (10문제)
  - print() 함수의 sep 파라미터 활용
  - 다양한 구분자로 값들 연결하여 출력

### 1.3 출력 파라미터 - end
- **problems-print-end.xml** (10문제)
  - print() 함수의 end 파라미터 활용
  - 줄바꿈 제어 및 연속 출력

## 2. 문자열 포맷팅

### 2.1 f-string 문법
- **problems-fstring.xml** (20문제)
  - f"문자열 {변수}" 기본 문법
  - 변수를 문자열에 삽입하여 출력

### 2.2 format() 메서드
- **problems-format.xml** (20문제)
  - "문자열 {}".format(변수) 문법
  - f-string과 동일한 결과를 format으로 구현

## 3. 문자열 메서드

### 3.1 대소문자 변환 메서드
- **problems-strmethod-upper.xml** (15문제)
  - string.upper() 메서드로 소문자→대문자 변환

- **problems-strmethod-lower.xml** (15문제)
  - string.lower() 메서드로 대문자→소문자 변환

- **problems-strmethod-capitalize.xml** (15문제)
  - string.capitalize() 메서드로 첫 글자만 대문자 변환

### 3.2 공백 처리 메서드
- **problems-strmethod-strip.xml** (15문제)
  - string.strip() - 양쪽 공백 제거
  - string.lstrip() - 왼쪽 공백 제거
  - string.rstrip() - 오른쪽 공백 제거

### 3.3 문자열 치환 메서드
- **problems-strmethod-replace.xml** (15문제)
  - string.replace(old, new) 메서드로 문자열 치환

## 4. 문자열 슬라이싱

### 4.1 기본 슬라이싱
- **problems-string-slicing.xml** (20문제)
  - 단일 참조: `str[i]`
  - 기본 슬라이싱: `str[start:end]`
  - 시작점 생략: `str[:end]`
  - 끝점 생략: `str[start:]`

### 4.2 스텝 슬라이싱
- **problems-string-stepslicing.xml** (15문제)
  - 스텝 문법: `str[start:end:step]`
  - 문자열 뒤집기: `str[::-1]`
  - 간격 건너뛰기: `str[::2]` 등

---

## 학습 순서 권장사항

1. **기초 출력 단계**: problems-print → problems-print-sep → problems-print-end
2. **문자열 포맷팅 단계**: problems-fstring → problems-format
3. **문자열 메서드 단계**: upper/lower/capitalize → strip → replace
4. **문자열 슬라이싱 단계**: problems-string-slicing → problems-string-stepslicing

각 단계는 이전 단계의 내용을 복습하면서 새로운 개념을 학습하도록 구성되어 있습니다.

## 총 문제 수
- **총 180문제**
- 랜덤 추출 방식으로 매번 다른 문제 조합 제공