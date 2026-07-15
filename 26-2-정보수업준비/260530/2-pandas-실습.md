# pandas 데이터 분석 실습 (260530)

이번 주 실습(note2.ipynb)을 교사용으로 정리한 자료. 1차시 "공공데이터 불러오기와 기초 탐색".

- **주제**: 서울특별시 지하철 호선별/역별/시간대별 승하차 인원 데이터 분석
- **환경**: Google Colab, 데이터 파일 `seoul.csv` (공공데이터포털)

## 교사 참고 (수업 전 확인)

- **데이터 준비**: `seoul.csv`는 폴더에 없음. 공공데이터포털 "서울특별시 지하철 호선별 역별 시간대별 승하차 인원 정보_20210405"를 내려받아 `seoul.csv`로 저장해 두어야 실습이 돌아간다.
- **Colab 전용 셀**: 노트북 앞부분의 `google.colab.drive` 마운트 셀은 Colab에서만 동작. 로컬 주피터로 진행할 때는 이 셀을 빼고, 파일 경로만 맞추면 된다.
- **의도된 빈칸**: "결측치를 평균값으로 채우기" 셀이 비어 있다. 학생 실습용 공란이다. 정답 예시는 아래 4번의 [빈칸 정답] 참고.
- **시험 예고 메모**: 노트북 첫머리 교사 메모에 "딕셔너리 + 조건문 많이 해보기 / 중간처럼 나올 것"이라고 적혀 있다. 즉 딕셔너리와 조건문이 중간고사처럼 출제될 예정이므로 별도 연습을 권장한다.

## 1. 라이브러리 준비

```python
import pandas as pd                # 표(Table) 형태 데이터를 읽고 다루는 라이브러리
import matplotlib.pyplot as plt    # 그래프(시각화) 라이브러리

# 그래프에서 한글이 깨지지 않도록 나눔 폰트 설치 (Colab 기준)
!sudo apt-get install -y fonts-nanum
!fc-cache -fv
```

```python
# 설치한 폰트를 matplotlib 기본 폰트로 지정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False   # 마이너스 기호 깨짐 방지
```

## 2. CSV 불러오기 (인코딩 예외 처리)

한글 CSV는 파일마다 인코딩이 달라(utf-8 또는 cp949) 에러가 날 수 있다. `try/except`로 두 경우를 모두 처리한다.

```python
file_path = 'seoul.csv'

try:
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='cp949')
```

설명: 먼저 utf-8로 읽어 보고, 실패하면(`UnicodeDecodeError`) cp949로 다시 읽는다. `try`가 if, `except`가 else 역할을 한다고 보면 된다.

## 3. 기초 탐색

| 코드 | 의미 |
|---|---|
| `df.shape` | (행 수, 열 수). 데이터 전체 크기 |
| `df.head(n)` | 위에서 n개 행 미리 보기 (기본 5개) |
| `df.info()` | 컬럼 목록, 결측치 여부(Non-Null), 자료형(Dtype) |
| `df.describe()` | 숫자 컬럼의 기초 통계(개수, 평균, 표준편차, 최소/최대, 사분위수) |

```python
print("행/열 크기:", df.shape)
print(df.head())
df.info()
print(df.describe())
```

**교사 참고**: `info()`에서 숫자여야 할 컬럼이 `object`(문자열)로 나오면 계산/시각화가 안 되므로 자료형 변환이 필요하다는 점을 짚어 주면 좋다.

## 4. 결측치 처리

```python
# 1) 결측치가 어디에 몇 개 있는지 확인
print(df.isnull().sum())

# 2-1) 결측치(빈칸)가 있는 행을 통째로 제거
df_clean = df.dropna()
```

- `df.isnull()`: 각 칸이 비었으면 True, 아니면 False
- `.sum()`: True를 1로 세어 컬럼별 결측치 개수를 합산
- `df.dropna()`: 빈칸이 하나라도 있는 행을 제거한 새 데이터프레임 반환

**[빈칸 정답] 결측치를 평균값으로 채우기 (의도된 공란 셀)**

```python
# 행을 지우는 대신, 빈칸을 그 컬럼의 평균값으로 채우는 방법
df_filled = df.fillna(df.mean(numeric_only=True))
```

`numeric_only=True`를 주면 숫자 컬럼에 대해서만 평균을 계산한다(문자열 컬럼이 섞여 있어도 에러가 안 남). 특정 컬럼만 채울 때는 `df['컬럼'] = df['컬럼'].fillna(df['컬럼'].mean())` 형태로 쓴다.

## 5. 컬럼 선택

분석에 필요한 컬럼만 골라 새 데이터프레임을 만든다.

```python
subway_cols = ['날짜', '호선명', '지하철역',
               '07시-08시 승차인원', '07시-08시 하차인원',
               '08시-09시 승차인원', '08시-09시 하차인원']

df_subway_use = df_clean[subway_cols].copy()
```

- `df_clean[리스트]`: 리스트에 적은 컬럼들만 잘라 가져옴
- `.copy()`: 원본과 분리된 복사본을 만든다. 안 붙이면 원본을 건드릴 위험이 있다

## 6. 파생 컬럼 만들기

기존 컬럼을 조합해 새로운 의미의 컬럼을 만든다. 리스트 컴프리헨션으로 '승차'/'하차'가 들어간 컬럼명을 자동으로 모은다.

```python
# 1) '승차' / '하차' 가 들어간 컬럼명만 추출
on_cols  = [col for col in df_subway_use.columns if '승차' in col]
off_cols = [col for col in df_subway_use.columns if '하차' in col]

# 2) 승차 합계, 하차 합계 컬럼 만들기 (행 방향 합산)
df_subway_use['승차합계'] = df_subway_use[on_cols].sum(axis=1)
df_subway_use['하차합계'] = df_subway_use[off_cols].sum(axis=1)

print(df_subway_use[['지하철역', '승차합계', '하차합계']].head())
```

- 리스트 컴프리헨션 `[col for col in ... if '승차' in col]`: 컬럼 이름에 '승차'가 들어간 것만 골라 리스트로 만든다
- `sum(axis=1)`: 행(가로) 방향으로 더한다. 즉 한 역의 여러 시간대 승차 인원을 한 줄로 합산

## 7. 저장

```python
df_subway_use.to_csv('seoul_clean.csv', index=False, encoding='utf-8-sig')
print("저장 완료! seoul_clean.csv")
```

- `index=False`: 자동 붙는 행 번호를 저장하지 않음
- `encoding='utf-8-sig'`: 엑셀에서 한글이 깨지지 않도록 BOM을 붙인 utf-8로 저장

## 오늘 배운 흐름 정리

1. 라이브러리 불러오기 (pandas, matplotlib)
2. CSV 불러오기 (인코딩 예외 처리)
3. 기초 탐색 (shape, head, info, describe)
4. 결측치 처리 (isnull, dropna / 평균 채우기)
5. 컬럼 선택 (대괄호, copy)
6. 파생 컬럼 만들기 (리스트 컴프리헨션, sum)
7. 저장 (to_csv)
