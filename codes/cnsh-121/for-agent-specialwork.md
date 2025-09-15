# cnsh-121 예시 코드 기반 Problems XML 생성 작업 규칙

## 작업 개요
- cnsh-121 폴더의 예시 코드 파일들을 기반으로 problems-*.xml 파일 생성
- 각 예시 코드 파일당 하나의 problems XML 파일 생성
- 파일명 규칙: `problems-cnsh121-[파일명].xml` (예: `problems-cnsh121-8puzzle.xml`)

## 예시 코드 파일 구조
- 각 파일에는 주석으로 문제 구성 방식이 명시되어 있음
- 형태: `# 번호. 문제 구성 방식 ...`
- 예시:
  - `# 1. 올바른 라이브러리 임포트 채우기 문제`
  - `# 2. distance() 메서드 - 거리 나오도록 구현하기 문제`
  - `# 조건식 부분을 비워두고 종료조건을 올바르게 채우라는 문항`

## Problems XML 구조
```xml
<problems>
  <problem>
    <description>문제 설명</description>
    <code><![CDATA[코드]]></code>
    <input><![CDATA[입력 예시]]></input>
    <output><![CDATA[출력 예시]]></output>
    <hint></hint>
    <solution><![CDATA[해설 코드]]></solution>
  </problem>
</problems>
```

## 태그별 작성 규칙

### description
- 문제의 주 질의부
- 문제 설명을 명확히 기술

### code
- **반드시 CDATA 사용**
- **순수 정의 코드만 포함** (실행부/예시/주석 제외)
- 클래스나 함수 정의만 포함
- 주석, 실행 코드, 예시 코드는 절대 포함하지 않음

### input
- 실행부분이나 입력값 예시
- **반드시 CDATA 사용**
- 코드에서 제거된 실행부분이나 테스트 코드

### output
- 예상 출력 결과
- **반드시 CDATA 사용**
- **출력이 뭐냐고 묻는 문제에서는 비워둠**

### hint
- **절대 사용하지 않음**
- 항상 빈 태그로 유지: `<hint></hint>`

### solution
- 해설 코드
- **반드시 CDATA 사용**
- 완전한 정답 코드와 설명 주석 포함

## 작업 원칙
1. 예시 코드 파일의 주석을 기반으로 문제 유형 파악
2. 각 주석이 하나의 problem 태그가 됨
3. 코드와 실행부를 명확히 분리
4. 모든 CDATA 태그 필수 사용
5. hint 태그는 절대 사용하지 않음

## cnsh-121 예시 코드 파일 목록 및 작업 현황

### 클래스 관련 파일
- class-8puzzle.py - 문제 작성됨
- class-distance.py - 문제 작성됨
- class-movie.py - 문제 작성됨
- class-student.py - 문제 작성됨

### 함수 관련 파일
- func-8puzzle-moveup.py - 문제 작성됨
- func-adjlist.py - 문제 작성됨
- func-adjmatrix.py - 문제 작성됨
- func-countdown.py - 문제 작성됨
- func-evensum.py - 문제 작성됨
- func-factorial.py - 문제 작성됨
- func-gcd.py - 문제 작성됨
- func-globalvar.py - 문제 작성됨
- func-makestack.py - 문제 작성됨
- func-minmax.py - 문제 작성됨

### 재귀 함수 관련 파일
- func-recursive-countdown.py - 문제 작성됨
- func-recursive-factorial.py - 문제 작성됨
- func-recursive-gcd.py - 문제 작성됨
- func-recursive-lcm-global.py - 문제 작성됨
- func-recursive-numtriangle.py - 문제 작성됨
- func-recursive-permutation.py - 문제 작성됨
- func-recursive-stars.py - 문제 작성됨
- func-recursive-startriangle.py - 문제 작성됨
- func-recursive-sum.py - 문제 작성됨

### 기타 파일
- func-sum-using-global.py - 문제 작성됨
- func-while-gcd.py - 문제 작성됨
- lib-use-queue.py - 문제 작성됨

**총 26개 파일 - 모두 문제 작성 완료**