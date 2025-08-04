# Python Exercise Problem Renderer

HTML 기반 연습문제 생성 도구입니다. XML 데이터에서 문제를 랜덤으로 추출하여 A4 프린트용 HTML 문서를 생성합니다.

## 🚀 빠른 시작

### 방법 1: 자동 실행 (추천)
1. `start.bat` 파일을 더블클릭
2. 브라우저가 자동으로 열립니다
3. 문제가 생성된 것을 확인하세요

### 방법 2: 수동 실행
1. 터미널에서 이 폴더로 이동
2. `python -m http.server 8000` 실행
3. 브라우저에서 `http://localhost:8000` 접속

## 📁 파일 구조

```
problem-renderer/
├── index.html          # 메인 HTML 페이지
├── style.css           # A4 프린트용 CSS 스타일
├── script.js           # JavaScript 로직
├── start.bat          # 자동 실행 스크립트
├── README.md          # 사용법 안내
└── problem-xmls/       # XML 문제 데이터
    ├── config.xml              # 문서 구성 설정
    ├── problems-basic.xml      # 기초 문제들
    └── problems-advanced.xml   # 응용 문제들
```

## ⚙️ 설정 방법

### 1. 문서 제목과 섹션 설정 (`problem-xmls/config.xml`)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<exercise>
  <title>Exercise 7. Dictionary and While</title>
  <sections>
    <section title="Section 7.1 - 기초 연습" file="problems-basic.xml" count="3"/>
    <section title="Section 7.2 - 응용 연습" file="problems-advanced.xml" count="2"/>
  </sections>
</exercise>
```

### 2. 문제 데이터 작성 (`problem-xmls/problems-*.xml`)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<problems>
  <problem>
    <description>문제 설명</description>
    <code><![CDATA[# 코드 블록 (옵셔널)
print("Hello World")]]></code>
    <input><![CDATA[입력 예시 (옵셔널)]]></input>
    <output><![CDATA[출력 예시 (옵셔널)]]></output>
    <hint>힌트 (옵셔널)</hint>
    <solution><![CDATA[# 해설 코드 (옵셔널)
# 주석으로 설명
print("정답 코드")]]></solution>
  </problem>
</problems>
```

## 🎯 주요 기능

- **랜덤 문제 추출**: 각 섹션별로 지정된 개수만큼 랜덤 선택
- **A4 프린트 최적화**: 흑백 출력용 스타일링
- **옵셔널 필드**: 코드, 입력/출력 예시, 힌트, 해설 선택적 포함
- **연속 번호 매기기**: 전체 문서에서 문제 번호 자동 부여
- **CDATA 지원**: 코드 블록의 특수문자와 들여쓰기 안전 보관

## 🖨️ 프린트 방법

1. 브라우저에서 `Ctrl + P` (또는 `Cmd + P`)
2. 프린터를 "PDF로 저장" 또는 실제 프린터 선택
3. 용지 크기: A4 선택
4. 인쇄 실행

## 📝 새 문제 추가 방법

1. 해당 난이도의 XML 파일 열기 (예: `problems-basic.xml`)
2. `<problem>` 태그 내에 새로운 문제 추가
3. 페이지 새로고침으로 즉시 반영

## 🔧 문제해결

### "Failed to fetch" 오류가 발생하는 경우
- **원인**: 브라우저의 CORS 정책으로 로컬 파일 접근 차단
- **해결**: 반드시 로컬 서버를 사용하세요 (`start.bat` 실행)

### 문제가 표시되지 않는 경우
- XML 파일의 문법 오류 확인
- 브라우저 개발자 도구(F12) → Console에서 오류 메시지 확인

## 📋 요구사항

- Python 3.x (로컬 서버용)
- 최신 브라우저 (Chrome, Firefox, Edge 등)

## 📄 라이선스

이 프로젝트는 교육 목적으로 자유롭게 사용 가능합니다.