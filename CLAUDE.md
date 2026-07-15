# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Python 교육 자료 아카이브. 모든 강의/문제 자료는 레거시로 `legacy/` 폴더에 정리되어 있다.

## Directory Structure

```
legacy/
  notebooks/                         # 강의 노트북 (도메인/난이도별)
    01-basic/                        # Python 기초 (변수, 리스트, 조건문, 반복문, 함수)
    02-intermediate/                 # 자료구조/알고리즘 (스택, DFS, 재귀, 트리, 시간복잡도)
    03-design-patterns/              # OOP/디자인패턴 (클래스, Composite, Factory, Builder 등)
    04-machine-learning/             # 머신러닝 (회귀, SVM, KNN, 의사결정트리, 클러스터링, NN)
    05-rne-statistics/               # R&E 통계분석 (단변량~다변량)
  references/                        # 참고 자료 (읽기 전용)
    problem-renderer/                # HTML 기반 문제 출제/렌더링 시스템
    codes/                           # Python 소스코드 예제
    cnsh-122/                        # CNSH-122 과정 문서, 샘플코드, 문제 XML
    documents/                       # PDF, HTML 등 기타 자료
```

## Problem Renderer (Legacy)

`legacy/references/problem-renderer/`에 위치한 HTML 기반 연습문제 생성 시스템.

```bash
# 실행 (problem-renderer 디렉토리에서)
python -m http.server 8000
# http://localhost:8000 접속
```

### XML template files

- `legacy/references/documents/cpml-template.xml`: 문제 XML 기본 템플릿
- `legacy/references/problem-renderer/problem-xmls/template-config.xml`: config XML 템플릿
- `legacy/references/problem-renderer/problem-xmls/template-problems.xml`: problems XML 템플릿

## 문제 출제 기준

- `DIFFICULTY-FILLBLANK.md`: 빈칸채우기 문제 난이도 프레임워크
- `SCOPE-CURRENT.md`: 현재 학생 학습 범위 (출제 범위 필터)

## License

Creative Commons Attribution-NonCommercial 4.0 + Permission Required.
비영리 목적만 허용, 사용 전 허가 필요.

