"""lecture-rne 노트북 빌더 - 실행 후 삭제해도 됨"""
import json

def _splitlines(source):
    """ipynb source는 각 줄 끝에 \\n이 있어야 한다 (마지막 줄 제외)."""
    lines = source.split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]] if lines else []

def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": _splitlines(source)}

def code(source):
    return {"cell_type": "code", "metadata": {}, "source": _splitlines(source),
            "outputs": [], "execution_count": None}

def notebook(cells):
    return {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.0"}
        },
        "cells": cells
    }

def save(name, cells):
    with open(name, "w", encoding="utf-8") as f:
        json.dump(notebook(cells), f, ensure_ascii=False, indent=1)
    print(f"  Created: {name} ({len(cells)} cells)")

# ============================================================
# 1편: One Feature (단변량 분석)
# ============================================================
def build_part1():
    cells = [
# ---- Intro ----
md("""# R&E 연구 검증 방법론 1편: One Feature (단변량 분석)

변수 **하나**를 골라서 "이 변수가 어떻게 생겼는가?"를 파악하는 단계.
모든 분석의 출발점이며, 논문에서는 보통 **Table 1 (기술통계)**에 해당한다.

```
1-Feature
|
|-- 수치형 (Numeric)
|     |-- 기초: 기술통계, 히스토그램, 박스플롯
|     |-- 검정: 정규성 검정 (Shapiro-Wilk)
|     |-- 고급: KDE, 이상치 탐지, 분포 적합, 부트스트랩
|
|-- 범주형 (Categorical)
|     |-- 빈도표, 비율, 막대그래프
|
|-- 시계열 (Time Series)
      |-- 추세 시각화, 이동평균
      |-- 정상성 검정 (ADF test)
      |-- 자기상관 (ACF/PACF)
      |-- 시계열 분해 (Trend + Seasonal + Residual)
```"""),

# ---- Setup ----
code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Colab에서도 바로 로드 가능한 데이터셋
df = sns.load_dataset('penguins').dropna()
print(f'데이터 수: {len(df)}')
df.head()"""),

# ---- Part 1-A: 수치형 기초 ----
md("""---
## 1-A. 수치형 변수: 기초 분석

수치형 변수 하나를 골랐을 때 가장 먼저 할 일.

| 방법 | 알 수 있는 것 | Python |
|------|-------------|--------|
| 기술통계 | 중심(mean, median), 퍼짐(std), 범위 | `df['col'].describe()` |
| 히스토그램 | 분포 모양, 치우침, 봉우리 수 | `plt.hist()` |
| 박스플롯 | 사분위수, 이상치 | `plt.boxplot()` |

### Agent 지시 예시
> "body_mass_g 변수의 기술통계를 구하고, 히스토그램과 박스플롯을 그려줘."
"""),

code("""# 기술통계
target = df['body_mass_g']
print('=== body_mass_g 기술통계 ===')
print(f'  평균(mean):     {target.mean():.1f}')
print(f'  중앙값(median): {target.median():.1f}')
print(f'  표준편차(std):  {target.std():.1f}')
print(f'  최솟값(min):    {target.min():.1f}')
print(f'  최댓값(max):    {target.max():.1f}')
print(f'  왜도(skew):     {target.skew():.3f}')  # 0에 가까우면 대칭
print(f'  첨도(kurtosis): {target.kurtosis():.3f}')  # 0이면 정규분포와 유사"""),

code("""# 히스토그램 + 박스플롯
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(target, bins=20, edgecolor='black', alpha=0.7)
axes[0].set_title('Histogram: body_mass_g')
axes[0].set_xlabel('Body Mass (g)')
axes[0].set_ylabel('Frequency')

axes[1].boxplot(target, vert=True)
axes[1].set_title('Boxplot: body_mass_g')
axes[1].set_ylabel('Body Mass (g)')

plt.tight_layout()
plt.show()"""),

# ---- 정규성 검정 ----
md("""---
## 1-B. 정규성 검정

많은 통계 검정(t-test, ANOVA, Pearson 상관 등)은 **"데이터가 정규분포를 따른다"**는 가정 위에 만들어졌다.
이 가정이 맞는지 먼저 확인해야 한다.

| 검정 | 특징 | Python |
|------|------|--------|
| Shapiro-Wilk | 소표본(n<5000)에 강력. 가장 많이 사용 | `stats.shapiro(x)` |
| D'Agostino-Pearson | 왜도+첨도 결합 검정 | `stats.normaltest(x)` |
| Kolmogorov-Smirnov | 큰 표본에 적합, 분포 비교 범용 | `stats.kstest(x, 'norm')` |
| Anderson-Darling | 꼬리 부분에 민감 | `stats.anderson(x)` |

**해석**: p < 0.05 -> 정규분포가 아니다 (비모수 검정 사용)

| 정규분포 O | 정규분포 X (비모수 대안) |
|-----------|----------------------|
| t-test | Mann-Whitney U |
| ANOVA | Kruskal-Wallis |
| Pearson r | Spearman rho |
"""),

code("""# 정규성 검정 3종
print('=== 정규성 검정: body_mass_g ===')
print()

# 1) Shapiro-Wilk (가장 많이 사용)
stat, p = stats.shapiro(target)
print(f'Shapiro-Wilk:       stat={stat:.4f}, p={p:.4f}')

# 2) D'Agostino-Pearson
stat2, p2 = stats.normaltest(target)
print(f"D'Agostino-Pearson: stat={stat2:.4f}, p={p2:.4f}")

# 3) Kolmogorov-Smirnov (정규분포와 비교)
# 표준화 후 표준정규분포와 비교
z = (target - target.mean()) / target.std()
stat3, p3 = stats.kstest(z, 'norm')
print(f'Kolmogorov-Smirnov: stat={stat3:.4f}, p={p3:.4f}')

print()
for name, pv in [('Shapiro-Wilk', p), ("D'Agostino", p2), ('K-S', p3)]:
    verdict = '정규분포 X' if pv < 0.05 else '정규분포 O'
    print(f'  {name:20s} -> {verdict} (p={pv:.4f})')"""),

# ---- KDE + 이상치 + 분포 적합 ----
md("""---
## 1-C. 고급 단변량: KDE, 이상치 탐지, 분포 적합

실제 연구에서는 히스토그램 너머의 분석이 필요하다.

| 방법 | 질문 | 핵심 |
|------|------|------|
| **KDE** (커널 밀도 추정) | 분포의 진짜 모양은? | 히스토그램의 연속 버전. 봉우리 수, 비대칭성 확인 |
| **이상치 탐지 (IQR)** | 비정상적 값이 있는가? | Q1-1.5*IQR ~ Q3+1.5*IQR 범위 밖 |
| **이상치 탐지 (Z-score)** | 평균에서 극단적으로 먼 값? | \\|z\\| > 3이면 이상치 의심 |
| **분포 적합** | 어떤 이론적 분포를 따르는가? | 정규, 로그정규, 감마 등에 fitting |
| **부트스트랩** | 추정치의 신뢰구간은? | 반복 재추출로 불확실성 계산 |

### Agent 지시 예시
> "body_mass_g의 KDE를 그리고, IQR과 Z-score로 이상치를 찾아줘.
> 정규분포, 로그정규분포, 감마분포 중 어느 것에 가장 잘 맞는지도 확인해줘."
"""),

md("""### 주요 확률 분포와 데이터의 성격

"내 데이터가 어떤 분포를 따르는가?"를 아는 것은 단순한 수학이 아니다.
**데이터가 어떤 분포를 따르는지는 그 데이터가 어떤 메커니즘으로 생성되었는지를 반영한다.**

---

#### 연속형 분포

| 분포 | 모양 | 어떤 데이터가 이 분포를 따르는가 | 실제 예시 |
|------|------|-------------------------------|----------|
| **정규분포** (Normal) | 좌우 대칭 종형 | 수많은 독립적 요인이 **더해져서** 만들어진 값. 중심극한정리에 의해 표본 평균은 항상 정규분포에 수렴 | 키, 체중, 시험 점수, 측정 오차, 제조 공차 |
| **로그정규분포** (Log-Normal) | 오른쪽 꼬리가 긴 비대칭 | 수많은 독립적 요인이 **곱해져서** 만들어진 값. log를 취하면 정규분포가 됨 | 소득 분포, 주가 수익률의 누적, 도시 인구, 세포 크기, 입자 크기 |
| **지수분포** (Exponential) | 0에서 시작해 급감소 | **다음 사건까지의 대기 시간**. 사건이 일정한 확률로 독립적으로 발생할 때 | 고장까지 시간, 고객 도착 간격, 방사성 붕괴, 전화 통화 간격 |
| **감마분포** (Gamma) | 오른쪽 꼬리, 유연한 모양 | 지수분포의 일반화. **K번째 사건까지의 대기 시간** 또는 양(+)의 연속 측정값 | 보험 청구 금액, 강우량, 대기 시간 합산, 서비스 시간 |
| **베타분포** (Beta) | 0~1 사이, 다양한 모양 | **비율, 확률, 비중** 등 0과 1 사이에 한정된 값 | 합격률, 전환율, 유전자 빈도, 야구 타율 |
| **균일분포** (Uniform) | 평평한 직사각형 | 모든 값이 **동등한 확률**로 나타남. 특별한 편향이 없는 무작위 | 난수 생성, 주사위(이산), 룰렛 |
| **와이블분포** (Weibull) | 감마와 유사, 유연 | **수명/생존 데이터**. 고장률이 시간에 따라 변할 수 있음 | 부품 수명, 재료 파괴 강도, 풍속 분포 |
| **코시분포** (Cauchy/t with df=1) | 매우 무거운 꼬리 | **극단값이 자주** 나타나는 데이터. 평균이 존재하지 않음 | 금융 위기 시 수익률, 공진 주파수, 비율 추정 |
| **t-분포** (Student's t) | 정규와 유사하나 꼬리 두꺼움 | **소표본**에서의 추정. 자유도가 커지면 정규분포에 수렴 | 소표본 평균 검정, 회귀 계수의 분포 |
| **파레토분포** (Pareto) | 극단적 꼬리 (멱법칙) | **소수가 대부분을 차지**하는 불균형 데이터. 80/20 법칙 | 부의 분포, 도시 크기, 웹 트래픽, 지진 규모 |

#### 이산형 분포

| 분포 | 어떤 데이터가 이 분포를 따르는가 | 실제 예시 |
|------|-------------------------------|----------|
| **이항분포** (Binomial) | n번 시행에서 **성공 횟수** (각 시행은 독립, 성공 확률 동일) | 불량품 수, 합격자 수, 동전 앞면 횟수 |
| **포아송분포** (Poisson) | 단위 시간/공간당 **사건 발생 횟수** (드물게 독립적으로 발생) | 시간당 방문자 수, 페이지당 오타, 연간 지진 횟수 |
| **기하분포** (Geometric) | **첫 번째 성공까지의 시행 횟수** | 첫 불량까지 검사 횟수, 첫 당첨까지 복권 구매 |
| **음이항분포** (Negative Binomial) | **K번째 성공까지의 시행 횟수**. 포아송보다 분산이 클 때 대안 | 과분산된 카운트 데이터, 유전자 발현량 |

---

#### 분포 선택의 실전 가이드

```
내 데이터의 성격은?
|
|-- 양수만 가능 (0 이상)
|     |-- 대기 시간, 수명 -> 지수분포, 와이블분포
|     |-- 금액, 크기 (오른쪽 꼬리) -> 로그정규분포, 감마분포
|     |-- 극단적 불균형 (소수가 대부분) -> 파레토분포
|     |-- 비율 (0~1 사이) -> 베타분포
|     |-- 횟수 (정수) -> 포아송분포, 이항분포
|
|-- 음수도 가능
|     |-- 대칭적, 합산 결과 -> 정규분포
|     |-- 소표본 -> t-분포
|     |-- 극단값 빈번 -> 코시분포
|
|-- 판단 방법
      |-- 히스토그램/KDE -> 모양 확인
      |-- QQ-plot -> 특정 분포와 비교
      |-- 분포 적합 (AIC, KS test) -> 정량적 비교
```

#### 핵심: 왜 분포를 아는 것이 중요한가?

1. **적절한 통계 검정 선택**: 정규분포가 아니면 비모수 검정을 써야 한다
2. **모델링 근거**: "왜 이 모델을 선택했는가?"에 이론적 답을 줄 수 있다
3. **이상치 판단 기준**: 분포를 알아야 "비정상적인 값"의 기준을 세울 수 있다
4. **시뮬레이션**: 분포를 알면 유사한 데이터를 인공으로 생성할 수 있다
5. **현상 이해**: 데이터의 생성 메커니즘에 대한 단서가 된다

> **연구에서 자주 만나는 패턴**:
> - "오른쪽으로 꼬리가 길다" -> 로그 변환 시도 -> 로그정규 가능성
> - "0 근처에 몰려있고 가끔 큰 값" -> 지수/감마
> - "종 모양이지만 꼬리가 두껍다" -> t-분포 (자유도 추정)
> - "수익률이 정규분포 가정보다 극단값이 잦다" -> 코시 또는 t-분포
"""),

code("""# QQ-Plot: 데이터가 특정 분포를 따르는지 시각적으로 확인
# 점들이 대각선에 가까울수록 해당 분포와 일치
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1) 정규분포 QQ-plot
stats.probplot(target, dist='norm', plot=axes[0])
axes[0].set_title('QQ-Plot: Normal')

# 2) 로그정규 확인 (log 변환 후 정규 QQ)
stats.probplot(np.log(target), dist='norm', plot=axes[1])
axes[1].set_title('QQ-Plot: Log(data) vs Normal')

# 3) 지수분포 QQ-plot
stats.probplot(target, dist='expon', plot=axes[2])
axes[2].set_title('QQ-Plot: Exponential')

plt.tight_layout()
plt.show()

print('QQ-Plot 읽는 법:')
print('  - 점들이 빨간 대각선에 가까움 -> 해당 분포와 잘 맞음')
print('  - 끝부분이 휘어짐 -> 꼬리가 이론 분포보다 두껍거나 얇음')
print('  - S자 형태 -> 왜도(skewness)가 있음')"""),

code("""# KDE: 분포의 연속적 모양
from scipy.stats import gaussian_kde

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1) KDE
kde = gaussian_kde(target)
x_range = np.linspace(target.min() - 200, target.max() + 200, 300)
axes[0].plot(x_range, kde(x_range), linewidth=2)
axes[0].fill_between(x_range, kde(x_range), alpha=0.3)
axes[0].set_title('KDE: body_mass_g')
axes[0].set_xlabel('Body Mass (g)')

# 2) 이상치: IQR
Q1, Q3 = target.quantile(0.25), target.quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
outliers_iqr = target[(target < lower) | (target > upper)]

axes[1].boxplot(target, vert=True)
if len(outliers_iqr) > 0:
    axes[1].scatter([1]*len(outliers_iqr), outliers_iqr, color='red', zorder=5, s=50)
axes[1].set_title(f'IQR Outliers: {len(outliers_iqr)}개')

# 3) 이상치: Z-score
z_scores = np.abs(stats.zscore(target))
outliers_z = target[z_scores > 3]
axes[2].hist(z_scores, bins=30, edgecolor='black', alpha=0.7)
axes[2].axvline(x=3, color='red', linestyle='--', label='|z| = 3')
axes[2].set_title(f'Z-score Outliers (|z|>3): {len(outliers_z)}개')
axes[2].legend()

plt.tight_layout()
plt.show()

print(f'IQR 정상 범위: [{lower:.0f}, {upper:.0f}]')
print(f'IQR 이상치: {len(outliers_iqr)}개')
print(f'Z-score 이상치 (|z|>3): {len(outliers_z)}개')"""),

code("""# 분포 적합 (Distribution Fitting)
# 데이터가 어떤 이론적 분포를 따르는지 비교

from scipy.stats import norm, lognorm, gamma

distributions = {
    'Normal': norm,
    'Log-Normal': lognorm,
    'Gamma': gamma
}

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(target, bins=25, density=True, alpha=0.4, edgecolor='black', label='Data')

print('=== 분포 적합 비교 (AIC 기준, 낮을수록 좋음) ===')
print()
results = []
for name, dist in distributions.items():
    params = dist.fit(target)
    # KS 검정: 적합도
    ks_stat, ks_p = stats.kstest(target, dist.cdf, args=params)
    # AIC 근사: -2*loglik + 2*k
    loglik = np.sum(dist.logpdf(target, *params))
    aic = -2 * loglik + 2 * len(params)
    results.append((name, aic, ks_p))

    x = np.linspace(target.min(), target.max(), 200)
    ax.plot(x, dist.pdf(x, *params), linewidth=2, label=f'{name} (AIC={aic:.0f})')
    print(f'  {name:12s}: AIC={aic:.1f}, KS p-value={ks_p:.4f}')

ax.legend()
ax.set_title('Distribution Fitting')
plt.tight_layout()
plt.show()

best = min(results, key=lambda x: x[1])
print(f'\\n  -> 가장 적합한 분포: {best[0]} (AIC={best[1]:.1f})')"""),

code("""# 부트스트랩 신뢰구간
# "평균이 정확히 4207g이다"보다 "95% 신뢰구간은 [4100, 4310]이다"가 더 과학적
np.random.seed(42)
n_boot = 10000
boot_means = [np.random.choice(target, size=len(target), replace=True).mean()
              for _ in range(n_boot)]

ci_lower = np.percentile(boot_means, 2.5)
ci_upper = np.percentile(boot_means, 97.5)

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(boot_means, bins=50, edgecolor='black', alpha=0.7)
ax.axvline(target.mean(), color='red', linewidth=2, label=f'Sample Mean: {target.mean():.1f}')
ax.axvline(ci_lower, color='orange', linestyle='--', label=f'95% CI Lower: {ci_lower:.1f}')
ax.axvline(ci_upper, color='orange', linestyle='--', label=f'95% CI Upper: {ci_upper:.1f}')
ax.legend()
ax.set_title('Bootstrap Distribution of Mean')
plt.tight_layout()
plt.show()

print(f'표본 평균: {target.mean():.1f}g')
print(f'95% 부트스트랩 신뢰구간: [{ci_lower:.1f}, {ci_upper:.1f}]g')"""),

# ---- 범주형 ----
md("""---
## 1-D. 범주형 변수

범주형 변수 하나를 골랐을 때 할 수 있는 것들.

| 방법 | 알 수 있는 것 |
|------|-------------|
| 빈도표 | 각 범주에 몇 개씩 있는가 |
| 비율 | 전체에서 각 범주의 비중 |
| 막대그래프 | 빈도의 시각적 비교 |
| 최빈값 (mode) | 가장 많은 범주 |

### Agent 지시 예시
> "species 변수의 빈도와 비율을 구하고, 막대그래프로 그려줘."
"""),

code("""# 범주형 분석
freq = df['species'].value_counts()
ratio = df['species'].value_counts(normalize=True)

summary = pd.DataFrame({
    '빈도': freq,
    '비율': ratio.map(lambda x: f'{x:.1%}')
})
print('=== species 빈도/비율 ===')
print(summary)
print()

plt.figure(figsize=(6, 4))
freq.plot(kind='bar', edgecolor='black', alpha=0.7)
plt.title('Species Frequency')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()"""),

# ---- 시계열 ----
md("""---
## 1-E. 시계열 단변량 분석

시간 축을 가진 수치형 변수 1개에 대한 분석.
**주가, 온도, 센서값** 등 시간에 따라 변하는 데이터에 적용한다.

| 방법 | 질문 | Python |
|------|------|--------|
| 시계열 플롯 + 이동평균 | 추세가 있는가? | `pd.Series.rolling().mean()` |
| ADF 검정 (정상성) | 통계적 성질이 시간에 따라 변하는가? | `from statsmodels.tsa.stattools import adfuller` |
| ACF / PACF | 과거 값과 자기 자신이 상관이 있는가? | `from statsmodels.graphics.tsaplots import plot_acf` |
| 시계열 분해 | 추세 + 계절성 + 잔차로 분리 | `from statsmodels.tsa.seasonal import seasonal_decompose` |

### 핵심 개념: 정상성 (Stationarity)
- **정상(stationary)**: 평균과 분산이 시간에 따라 일정 -> 분석/예측 가능
- **비정상(non-stationary)**: 추세나 계절성이 있음 -> 차분(differencing)으로 정상화 필요
- 대부분의 시계열 모델(ARIMA 등)은 정상성을 가정한다

### Agent 지시 예시
> "이 시계열 데이터의 추세를 시각화하고 20일 이동평균을 그려줘.
> ADF 검정으로 정상성을 확인하고, ACF/PACF 플롯도 그려줘.
> 비정상이면 1차 차분 후 다시 ADF 검정해줘."
"""),

code("""# 시계열 예시 데이터: 항공 승객 수
# Colab에서도 바로 사용 가능한 내장 데이터

# statsmodels에서 예시 데이터 로드
try:
    from statsmodels.datasets import co2
    ts = co2.load().data
    ts = ts.resample('ME').mean().dropna()  # 월별 평균
    ts_col = 'co2'
    ts_title = 'CO2 Concentration (Monthly)'
except:
    # 대안: 랜덤 시계열
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', periods=200, freq='D')
    trend = np.linspace(0, 10, 200)
    seasonal = 5 * np.sin(np.arange(200) * 2 * np.pi / 30)
    noise = np.random.normal(0, 1, 200)
    ts = pd.DataFrame({'value': trend + seasonal + noise}, index=dates)
    ts_col = 'value'
    ts_title = 'Synthetic Time Series'

fig, axes = plt.subplots(2, 1, figsize=(12, 6))

# 원본 + 이동평균
axes[0].plot(ts, alpha=0.5, label='Original')
axes[0].plot(ts.rolling(12).mean(), color='red', linewidth=2, label='12-period MA')
axes[0].set_title(ts_title)
axes[0].legend()

# 1차 차분
diff = ts.diff().dropna()
axes[1].plot(diff, alpha=0.7)
axes[1].set_title('1st Difference (Detrended)')

plt.tight_layout()
plt.show()"""),

code("""# ADF 정상성 검정
from statsmodels.tsa.stattools import adfuller

def adf_test(series, name=''):
    result = adfuller(series.dropna(), autolag='AIC')
    print(f'=== ADF Test: {name} ===')
    print(f'  ADF Statistic: {result[0]:.4f}')
    print(f'  p-value:       {result[1]:.4f}')
    print(f'  Critical Values:')
    for key, val in result[4].items():
        print(f'    {key}: {val:.4f}')
    if result[1] < 0.05:
        print('  -> 정상(Stationary): 추세 없음')
    else:
        print('  -> 비정상(Non-stationary): 추세 있음 -> 차분 필요')
    print()

# 원본
values = ts.iloc[:, 0] if hasattr(ts, 'iloc') else ts
adf_test(values, 'Original')

# 1차 차분 후
adf_test(values.diff().dropna(), '1st Difference')"""),

code("""# ACF / PACF
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

plot_acf(values.dropna(), lags=40, ax=axes[0])
axes[0].set_title('ACF (Autocorrelation)')

plot_pacf(values.dropna(), lags=40, ax=axes[1], method='ywm')
axes[1].set_title('PACF (Partial Autocorrelation)')

plt.tight_layout()
plt.show()

print('ACF 읽는 법:')
print('  - 천천히 감소 -> 비정상 (차분 필요)')
print('  - 특정 lag에서 급격히 끊김 -> MA(q) 모델 후보')
print()
print('PACF 읽는 법:')
print('  - 특정 lag에서 급격히 끊김 -> AR(p) 모델 후보')"""),

code("""# 시계열 분해: Trend + Seasonal + Residual
from statsmodels.tsa.seasonal import seasonal_decompose

decomp = seasonal_decompose(values.dropna(), model='additive', period=12)

fig, axes = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
decomp.observed.plot(ax=axes[0], title='Observed')
decomp.trend.plot(ax=axes[1], title='Trend')
decomp.seasonal.plot(ax=axes[2], title='Seasonal')
decomp.resid.plot(ax=axes[3], title='Residual')

plt.tight_layout()
plt.show()

print('분해 결과 해석:')
print('  - Trend: 장기적 방향 (상승? 하락? 일정?)')
print('  - Seasonal: 반복 패턴 (주기가 있는가?)')
print('  - Residual: 추세/계절성 제거 후 남은 잔차 (랜덤이면 좋음)')"""),

# ---- 요약 ----
md("""---
## 1편 요약: 단변량 분석 체크리스트

### 수치형 변수
1. **기술통계** (mean, median, std, min, max, skew, kurtosis)
2. **시각화** (히스토그램, 박스플롯, KDE)
3. **정규성 검정** (Shapiro-Wilk) -> 이후 검정 방법 결정
4. **이상치 탐지** (IQR 또는 Z-score) -> 제거 여부 판단
5. **분포 적합** (어떤 이론적 분포와 유사한가?)
6. **신뢰구간** (부트스트랩 또는 t-분포 기반)

### 범주형 변수
1. **빈도표** + **비율**
2. **막대그래프**

### 시계열 변수
1. **시계열 플롯** + 이동평균
2. **ADF 검정** (정상성 확인)
3. **ACF/PACF** (자기상관 구조)
4. **시계열 분해** (추세 + 계절성 + 잔차)

### Agent 통합 지시 예시
> "이 데이터의 [변수명]에 대해 단변량 분석을 수행해줘:
> 1) 기술통계와 분포 시각화 (히스토그램, 박스플롯, KDE)
> 2) 정규성 검정 (Shapiro-Wilk)
> 3) 이상치 탐지 (IQR, Z-score)
> 4) 결과를 표로 정리해줘."
"""),
    ]
    save("RnE 1. One Feature (단변량 분석).ipynb", cells)


# ============================================================
# 2편: Two Features (이변량 분석)
# ============================================================
def build_part2():
    cells = [

md("""# R&E 연구 검증 방법론 2편: Two Features (이변량 분석)

변수 **2개**를 골라서 "둘 사이에 관계가 있는가?"를 분석하는 단계.
연구의 핵심이다. **"X가 Y에 영향을 미치는가?"**에 답한다.

두 변수의 타입 조합에 따라 방법이 완전히 달라진다:

```
2-Feature
|
|-- [A] 수치 vs 수치
|     |-- 관계 유무: 상관분석 (Pearson / Spearman)
|     |-- 예측/영향: 선형 회귀, 다항 회귀
|     |-- 정보량: 상호정보량 (Mutual Information)
|
|-- [B] 범주 vs 수치
|     |-- 그룹 2개: t-test (모수) / Mann-Whitney (비모수)
|     |-- 그룹 3개+: ANOVA (모수) / Kruskal-Wallis (비모수)
|     |-- 사후검정: Tukey HSD
|     |-- 효과 크기: Cohen's d, Eta-squared
|
|-- [C] 범주 vs 범주
|     |-- 카이제곱 독립성 검정
|     |-- Fisher 정확 검정 (소표본)
|     |-- Cramer's V (효과 크기)
```

### 검정 선택 핵심 결정: 모수 vs 비모수

**1편에서 정규성 검정을 해야 하는 이유가 여기서 나온다.**

| 조건 | 모수 검정 (Parametric) | 비모수 검정 (Non-parametric) |
|------|----------------------|---------------------------|
| 정규분포 O | t-test, ANOVA, Pearson r | (사용 가능하지만 불필요) |
| 정규분포 X | (부적절) | Mann-Whitney, Kruskal-Wallis, Spearman rho |
| 표본 크기 | 충분히 클 때 (n>30 근사) | 작을 때도 안전 |
"""),

code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

df = sns.load_dataset('penguins').dropna()
print(f'데이터 수: {len(df)}')
df.head()"""),

# ---- 2-A: 수치 vs 수치 ----
md("""---
## 2-A. 수치 vs 수치

두 변수가 모두 숫자일 때. "하나가 올라가면 다른 것도 올라가는가?"

| 방법 | 질문 | 결과 |
|------|------|------|
| 산점도 | 관계가 있어 보이는가? | 시각적 판단 |
| **Pearson r** | 선형 관계의 강도와 방향 | -1 ~ +1 (정규분포 가정) |
| **Spearman rho** | 단조 관계의 강도와 방향 | -1 ~ +1 (비모수, 순위 기반) |
| 선형 회귀 | X가 1 늘면 Y가 얼마나 변하는가? | 회귀식, R-squared |
| 상호정보량 | 비선형 관계까지 포함한 의존성 | 0 이상 (클수록 의존적) |

### 상관 해석 기준
| |r| 범위 | 해석 |
|----------|------|
| 0.0 ~ 0.1 | 무시할 수준 |
| 0.1 ~ 0.3 | 약한 상관 |
| 0.3 ~ 0.5 | 중간 상관 |
| 0.5 ~ 0.7 | 강한 상관 |
| 0.7 ~ 1.0 | 매우 강한 상관 |

### Agent 지시 예시
> "flipper_length_mm와 body_mass_g의 산점도를 그리고,
> Pearson과 Spearman 상관계수를 둘 다 구해줘.
> 유의하면 선형 회귀도 해서 회귀식과 R-squared를 알려줘."
"""),

code("""# 산점도: 먼저 눈으로 확인
plt.figure(figsize=(7, 5))
plt.scatter(df['flipper_length_mm'], df['body_mass_g'], alpha=0.5)
plt.xlabel('Flipper Length (mm)')
plt.ylabel('Body Mass (g)')
plt.title('Flipper Length vs Body Mass')
plt.show()"""),

code("""# Pearson vs Spearman 상관분석
x = df['flipper_length_mm']
y = df['body_mass_g']

r_pearson, p_pearson = stats.pearsonr(x, y)
r_spearman, p_spearman = stats.spearmanr(x, y)

print('=== 상관분석: flipper_length vs body_mass ===')
print(f'  Pearson  r={r_pearson:.3f},  p={p_pearson:.2e}  (선형 관계, 정규분포 가정)')
print(f'  Spearman rho={r_spearman:.3f}, p={p_spearman:.2e}  (단조 관계, 비모수)')
print()

# Pearson과 Spearman이 비슷하면: 선형 관계
# Spearman >> Pearson이면: 비선형이지만 단조적 관계
diff = abs(r_spearman) - abs(r_pearson)
if abs(diff) < 0.05:
    print('  -> 두 값이 비슷: 관계가 대체로 선형적')
elif diff > 0.05:
    print('  -> Spearman > Pearson: 비선형이지만 단조적 관계 가능성')
else:
    print('  -> Pearson > Spearman: 이상치의 영향 가능성')"""),

code("""# 선형 회귀
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

X = df[['flipper_length_mm']]
y = df['body_mass_g']

model = LinearRegression().fit(X, y)
y_pred = model.predict(X)

print('=== 선형 회귀 ===')
print(f'  회귀식: body_mass = {model.coef_[0]:.2f} * flipper_length + ({model.intercept_:.2f})')
print(f'  R-squared: {r2_score(y, y_pred):.3f}')
print(f'  해석: 날개가 1mm 길어지면 체중이 약 {model.coef_[0]:.1f}g 증가하는 경향')
print(f'        모델이 체중 변동의 {r2_score(y, y_pred)*100:.1f}%를 설명')

# 회귀선 시각화
plt.figure(figsize=(7, 5))
plt.scatter(X, y, alpha=0.4, label='data')
plt.plot(X, y_pred, color='red', linewidth=2, label='regression')
plt.xlabel('Flipper Length (mm)')
plt.ylabel('Body Mass (g)')
plt.title(f'Linear Regression (R2={r2_score(y, y_pred):.3f})')
plt.legend()
plt.show()"""),

md("""### 상관 vs 회귀: 뭐가 다른가?

| | 상관분석 | 회귀분석 |
|--|---------|--------|
| 질문 | 관계가 **있는가**? 얼마나 강한가? | X로 Y를 **예측**할 수 있는가? |
| 방향성 | X<->Y 대칭 (누가 원인인지 모름) | X->Y 방향이 있음 |
| 결과물 | 상관계수 r (-1~1) | 회귀식 (y = ax + b), R-squared |
| 용도 | 탐색적 분석 | 예측, 영향력 정량화 |

### 주의: 상관 != 인과

"아이스크림 판매량과 익사 사고는 r = 0.9"
-> 아이스크림이 익사를 유발하는가? 아니다. 둘 다 **기온(제3변수)** 때문이다.

상관에서 인과를 주장하려면:
1. 시간적 선후관계 (A가 B보다 먼저)
2. 제3의 변수 통제
3. 이론적 메커니즘 설명 가능
"""),

md("""### 상관행렬: 수치형 변수 전체를 한눈에

여러 수치형 변수 간의 상관을 한 번에 보는 방법.
변수 쌍을 선정하거나, 다중공선성(multicollinearity)을 확인할 때 유용.

### Agent 지시 예시
> "수치형 변수 전체의 상관행렬을 구하고 히트맵으로 그려줘. 가장 강한 상관 쌍 3개를 알려줘."
"""),

code("""# 상관행렬 히트맵
numeric_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
corr = df[numeric_cols].corr()

plt.figure(figsize=(7, 6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            vmin=-1, vmax=1, square=True)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()

# 가장 강한 상관 쌍 추출
pairs = []
for i in range(len(numeric_cols)):
    for j in range(i+1, len(numeric_cols)):
        pairs.append((numeric_cols[i], numeric_cols[j], corr.iloc[i, j]))
pairs.sort(key=lambda x: abs(x[2]), reverse=True)

print('=== 상관 강도 순위 ===')
for v1, v2, r in pairs:
    print(f'  {v1} vs {v2}: r={r:.3f}')"""),

code("""# 상호정보량 (Mutual Information)
# 상관계수가 잡지 못하는 비선형 관계까지 측정
from sklearn.feature_selection import mutual_info_regression

X_mi = df[numeric_cols].values
print('=== 상호정보량 (body_mass_g 기준) ===')
print('  (높을수록 더 많은 정보를 공유)')
print()

mi = mutual_info_regression(
    df[['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm']],
    df['body_mass_g'],
    random_state=42
)
for col, score in zip(['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm'], mi):
    print(f'  {col:20s}: MI = {score:.3f}')

print()
print('  참고: MI는 0 이상. 선형이든 비선형이든 모든 종류의 의존성을 측정.')
print('  Pearson r는 선형만, Spearman rho는 단조만 잡지만 MI는 제한 없음.')"""),

# ---- 2-B: 범주 vs 수치 ----
md("""---
## 2-B. 범주 vs 수치

"그룹에 따라 숫자 값이 다른가?"
범주(그룹)가 몇 개인지에 따라 방법이 갈린다.

```
범주 vs 수치
|
|-- 정규분포 O (모수)
|     |-- 그룹 2개: 독립표본 t-test
|     |-- 그룹 3개+: One-way ANOVA + Tukey 사후검정
|
|-- 정규분포 X (비모수)
      |-- 그룹 2개: Mann-Whitney U
      |-- 그룹 3개+: Kruskal-Wallis + Dunn 사후검정
```

### 핵심 개념
"눈으로 보니 다른 것 같다"는 증거가 안 된다.
검정은 **"이 차이가 우연히 생길 수 있는 정도인가"**를 수치로 판단한다.
"""),

md("""### 2-B-1. t-test (그룹 2개, 모수)

| 종류 | 상황 | Python |
|------|------|--------|
| 독립표본 t-test | 서로 다른 두 그룹 비교 | `stats.ttest_ind(a, b)` |
| 대응표본 t-test | 같은 대상의 전후 비교 | `stats.ttest_rel(before, after)` |
| Welch t-test | 두 그룹의 분산이 다를 때 | `stats.ttest_ind(a, b, equal_var=False)` |

### Agent 지시 예시
> "수컷과 암컷 펭귄의 체중에 유의한 차이가 있는지 t-test 해줘.
> 정규성 검정 먼저 하고, p-value와 Cohen's d(효과 크기)도 보고해줘."
"""),

code("""# 시각화로 먼저 확인
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x='sex', y='body_mass_g')
plt.title('Body Mass by Sex')
plt.show()"""),

code("""# 독립표본 t-test: 수컷 vs 암컷 체중
male = df[df['sex'] == 'Male']['body_mass_g']
female = df[df['sex'] == 'Female']['body_mass_g']

# 먼저 정규성 확인
_, p_m = stats.shapiro(male)
_, p_f = stats.shapiro(female)
print(f'정규성 검정: Male p={p_m:.4f}, Female p={p_f:.4f}')
if p_m >= 0.05 and p_f >= 0.05:
    print('  -> 둘 다 정규분포 -> t-test 사용 가능')
else:
    print('  -> 정규분포 아님 -> Mann-Whitney도 함께 수행')
print()

# t-test
t_stat, p_value = stats.ttest_ind(male, female)
print('=== t-test: Male vs Female body_mass_g ===')
print(f'  Male   평균: {male.mean():.1f}g  (n={len(male)})')
print(f'  Female 평균: {female.mean():.1f}g  (n={len(female)})')
print(f'  차이: {male.mean() - female.mean():.1f}g')
print(f'  t-statistic: {t_stat:.3f}')
print(f'  p-value: {p_value:.2e}')
if p_value < 0.05:
    print('  -> 유의한 차이가 있다 (p < 0.05)')"""),

code("""# 효과 크기: Cohen's d
# p-value는 "차이가 있는가?" (Yes/No)
# Cohen's d는 "차이가 얼마나 큰가?" (크기)
# 논문에서는 둘 다 보고해야 한다.

def cohens_d(g1, g2):
    n1, n2 = len(g1), len(g2)
    pooled_std = np.sqrt(((n1-1)*g1.std()**2 + (n2-1)*g2.std()**2) / (n1+n2-2))
    return (g1.mean() - g2.mean()) / pooled_std

d = cohens_d(male, female)
print(f"Cohen's d = {d:.3f}")
print()

# 해석 기준 (Cohen, 1988)
if abs(d) < 0.2:
    size = '작은 효과 (small)'
elif abs(d) < 0.5:
    size = '작은~중간 효과'
elif abs(d) < 0.8:
    size = '중간 효과 (medium)'
else:
    size = '큰 효과 (large)'
print(f'  -> {size}')
print()
print('해석 기준 (Cohen, 1988):')
print('  |d| < 0.2: 작은 효과')
print('  |d| 0.2~0.5: 작은~중간')
print('  |d| 0.5~0.8: 중간 효과')
print('  |d| > 0.8: 큰 효과')"""),

md("""### p-value 올바르게 이해하기

**p-value란**: "차이가 없다고 가정했을 때(귀무가설), 이 정도 차이가 우연히 나올 확률"

| 흔한 오해 | 현실 |
|-----------|------|
| "효과가 있을 확률이 95%" | p-value는 그런 뜻이 아니다 |
| "p가 작을수록 효과가 크다" | 아니다. 효과 크기는 Cohen's d로 본다 |
| "p > 0.05면 차이가 없다" | "없다"가 아니라 "증거가 부족한 것" |
| "p < 0.05면 무조건 의미있다" | 표본이 매우 크면 사소한 차이도 유의하게 나옴 |

**그래서 반드시 효과 크기(effect size)를 함께 보고해야 한다.**
"""),

# ---- 비모수: Mann-Whitney ----
md("""### 2-B-2. Mann-Whitney U (그룹 2개, 비모수)

정규분포를 따르지 않을 때 t-test 대신 사용한다.
순위(rank)를 기반으로 비교하므로 분포 가정이 필요 없다.

### Agent 지시 예시
> "두 그룹의 [측정값]을 Mann-Whitney U 검정으로 비교해줘."
"""),

code("""# Mann-Whitney U (비모수 대안)
u_stat, p_mw = stats.mannwhitneyu(male, female, alternative='two-sided')

print('=== Mann-Whitney U: Male vs Female body_mass_g ===')
print(f'  U-statistic: {u_stat:.1f}')
print(f'  p-value: {p_mw:.2e}')
if p_mw < 0.05:
    print('  -> 유의한 차이가 있다 (비모수 검정)')
print()
print('  t-test와 비교:')
print(f'    t-test p = {p_value:.2e}')
print(f'    Mann-Whitney p = {p_mw:.2e}')
print('  -> 정규분포일 때는 보통 비슷한 결과. 비정규일 때 Mann-Whitney가 더 신뢰할 만함.')"""),

# ---- ANOVA ----
md("""### 2-B-3. ANOVA (그룹 3개+, 모수)

그룹이 3개 이상이면 t-test를 여러 번 하면 **안 된다**.
비교 횟수가 늘수록 우연히 유의한 결과가 나올 확률(1종 오류)이 쌓인다.

**ANOVA**: "이 그룹들 중 적어도 하나가 다른가?"를 한 번에 검정.
유의하면 -> **Tukey 사후검정**으로 어떤 쌍이 다른지 확인.

| 방법 | 조건 | Python |
|------|------|--------|
| One-way ANOVA | 정규분포 + 등분산 | `stats.f_oneway(g1, g2, g3)` |
| Kruskal-Wallis | 비모수 대안 | `stats.kruskal(g1, g2, g3)` |
| Tukey HSD | ANOVA 사후검정 | `pairwise_tukeyhsd()` |

### Agent 지시 예시
> "세 종의 펭귄 날개 길이에 차이가 있는지 ANOVA + Tukey 사후검정 해줘.
> 정규성 안 되면 Kruskal-Wallis도 해줘. eta-squared(효과 크기)도 보고해줘."
"""),

code("""# ANOVA: 3종 비교
plt.figure(figsize=(7, 4))
sns.boxplot(data=df, x='species', y='flipper_length_mm')
plt.title('Flipper Length by Species')
plt.show()"""),

code("""# One-way ANOVA
adelie = df[df['species'] == 'Adelie']['flipper_length_mm']
chinstrap = df[df['species'] == 'Chinstrap']['flipper_length_mm']
gentoo = df[df['species'] == 'Gentoo']['flipper_length_mm']

f_stat, p_anova = stats.f_oneway(adelie, chinstrap, gentoo)

print('=== One-way ANOVA: species -> flipper_length_mm ===')
print(f'  Adelie:    {adelie.mean():.1f}mm (n={len(adelie)})')
print(f'  Chinstrap: {chinstrap.mean():.1f}mm (n={len(chinstrap)})')
print(f'  Gentoo:    {gentoo.mean():.1f}mm (n={len(gentoo)})')
print(f'  F = {f_stat:.3f}, p = {p_anova:.2e}')
if p_anova < 0.05:
    print('  -> 적어도 한 쌍의 종 간에 유의한 차이 있음')
print()

# 효과 크기: Eta-squared
all_data = pd.concat([adelie, chinstrap, gentoo])
grand_mean = all_data.mean()
ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in [adelie, chinstrap, gentoo])
ss_total = sum((all_data - grand_mean)**2)
eta_sq = ss_between / ss_total
print(f'  Eta-squared = {eta_sq:.3f}')
print(f'  -> 종이 날개 길이 변동의 {eta_sq*100:.1f}%를 설명')
print()
print('  Eta-squared 해석:')
print('    < 0.01: 작은 효과')
print('    0.01~0.06: 중간 효과')
print('    > 0.14: 큰 효과')"""),

code("""# Tukey 사후검정: 어떤 쌍이 다른가?
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey = pairwise_tukeyhsd(df['flipper_length_mm'], df['species'], alpha=0.05)
print(tukey)
print()
print('reject=True인 쌍: 해당 두 종 사이에 유의한 차이 있음')"""),

code("""# Kruskal-Wallis (비모수 대안)
h_stat, p_kw = stats.kruskal(adelie, chinstrap, gentoo)

print('=== Kruskal-Wallis (비모수) ===')
print(f'  H = {h_stat:.3f}, p = {p_kw:.2e}')
print()
print('  ANOVA와 비교:')
print(f'    ANOVA p     = {p_anova:.2e}')
print(f'    Kruskal-W p = {p_kw:.2e}')"""),

# ---- 2-C: 범주 vs 범주 ----
md("""---
## 2-C. 범주 vs 범주

두 변수가 모두 범주형일 때. "A의 분포가 B에 따라 달라지는가?"

| 방법 | 상황 | Python |
|------|------|--------|
| **카이제곱 검정** | 기대빈도 >= 5인 셀이 대부분 | `stats.chi2_contingency()` |
| **Fisher 정확 검정** | 2x2 표, 소표본 | `stats.fisher_exact()` |
| **Cramer's V** | 효과 크기 | 직접 계산 |

### Agent 지시 예시
> "종(species)과 섬(island)의 교차표를 만들고, 카이제곱 검정과 Cramer's V를 구해줘."
"""),

code("""# 교차표
ct = pd.crosstab(df['species'], df['island'])
print('=== 교차표: species x island ===')
print(ct)
print()

ct.plot(kind='bar', figsize=(8, 4), edgecolor='black')
plt.title('Species x Island')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()"""),

code("""# 카이제곱 검정 + Cramer's V
chi2, p_chi, dof, expected = stats.chi2_contingency(ct)

print('=== 카이제곱 독립성 검정 ===')
print(f'  chi2 = {chi2:.3f}')
print(f'  p-value = {p_chi:.2e}')
print(f'  자유도 = {dof}')
if p_chi < 0.05:
    print('  -> 종과 섬 사이에 유의한 관계가 있다')
print()

# Cramer's V (효과 크기)
n = ct.sum().sum()
min_dim = min(ct.shape[0], ct.shape[1]) - 1
cramers_v = np.sqrt(chi2 / (n * min_dim))
print(f"Cramer's V = {cramers_v:.3f}")
print()
print("  Cramer's V 해석:")
print('    < 0.1: 약한 관계')
print('    0.1~0.3: 중간 관계')
print('    > 0.3: 강한 관계')
print()
print('기대빈도 (독립이라면 이렇게 분포했을 것):')
print(pd.DataFrame(expected, index=ct.index, columns=ct.columns).round(1))"""),

# ---- 주의사항 ----
md("""---
## 주의사항과 연구 윤리

### 변인 통제

| 용어 | 역할 | 예시 |
|------|------|------|
| 독립변인 (IV) | 내가 의도적으로 바꾸는 것 | 비료의 양 |
| 종속변인 (DV) | 그 결과로 변하는 것 (측정 대상) | 식물의 키 |
| 통제변인 (CV) | 바뀌면 안 되는 것 (고정) | 물의 양, 햇빛 |

핵심: **한 번에 하나만 바꾼다.** 두 가지를 동시에 바꾸면 원인 특정 불가.

### 절대 하면 안 되는 것

| 이름 | 행위 |
|------|------|
| **p-hacking** | 유의한 결과 나올 때까지 분석 방법을 바꾸는 것 |
| **cherry-picking** | 유리한 데이터만 골라서 보고 |
| **HARKing** | 결과 보고 나서 가설을 만들고, 처음부터 그랬던 척 하는 것 |

### 편향 (Bias)

| 종류 | 예시 |
|------|------|
| 선택 편향 | 특정 유형만 골라서 조사 |
| 확증 편향 | 내 가설에 맞는 데이터만 보려는 경향 |
| 생존자 편향 | 살아남은 것만 보고 판단 (탈락자 무시) |
"""),

# ---- 요약 ----
md("""---
## 2편 요약: 이변량 분석 선택 가이드

```
두 변수의 타입은?
|
|-- 수치 vs 수치
|     |-- 시각화: 산점도
|     |-- 관계 유무: Pearson r (정규) / Spearman rho (비모수)
|     |-- 예측: 선형 회귀 -> R-squared, 회귀식
|     |-- 비선형 의존성: 상호정보량 (MI)
|
|-- 범주 vs 수치
|     |-- 시각화: 박스플롯
|     |-- 정규분포 O + 2그룹: t-test + Cohen's d
|     |-- 정규분포 O + 3그룹+: ANOVA + Tukey + eta-squared
|     |-- 정규분포 X + 2그룹: Mann-Whitney U
|     |-- 정규분포 X + 3그룹+: Kruskal-Wallis
|
|-- 범주 vs 범주
      |-- 시각화: 교차표, 막대그래프
      |-- 카이제곱 검정 + Cramer's V
      |-- 소표본 2x2: Fisher 정확 검정
```

### Agent 통합 지시 예시
> "이 데이터에서 [독립변수]와 [종속변수]의 관계를 분석해줘.
> 변수 타입에 맞는 적절한 검정을 골라서 수행하고,
> p-value와 효과 크기를 함께 보고해줘.
> 시각화도 포함해줘."
"""),
    ]
    save("RnE 2. Two Features (이변량 분석).ipynb", cells)


# ============================================================
# 3편: Three+ Features (다변량 분석)
# ============================================================
def build_part3():
    cells = [

md("""# R&E 연구 검증 방법론 3편: Three+ Features (다변량 분석)

변수가 **3개 이상**일 때의 분석. 현실 데이터는 거의 항상 다변량이다.

"여러 변수가 동시에 결과에 어떻게 영향을 미치는가?"
"고차원 데이터에서 숨겨진 구조를 발견할 수 있는가?"

```
3+ Features
|
|-- [A] 관계 분석
|     |-- 다중 회귀 (Multiple Regression)
|     |-- 다중공선성 진단 (VIF)
|     |-- 편상관 (Partial Correlation)
|
|-- [B] 차원 축소 & 시각화
|     |-- PCA (주성분 분석)
|     |-- t-SNE / UMAP
|
|-- [C] 군집화 (비지도 학습)
|     |-- K-Means
|     |-- DBSCAN
|     |-- 계층적 군집화 (Dendrogram)
|
|-- [D] 분류 & 예측 (지도 학습)
|     |-- Logistic Regression
|     |-- Random Forest
|     |-- 교차 검증 (Cross-Validation)
|
|-- [E] 모델 해석
      |-- Feature Importance
      |-- Permutation Importance
      |-- SHAP
```
"""),

code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder

df = sns.load_dataset('penguins').dropna()
numeric_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
print(f'데이터 수: {len(df)}, 수치형 변수: {len(numeric_cols)}개')
df.head()"""),

# ---- 3-A: 다중 회귀 ----
md("""---
## 3-A. 다중 회귀 분석 (Multiple Regression)

독립변수가 2개 이상일 때의 회귀.
**"여러 변수 중 어떤 것이 종속변수에 영향을 미치는가?"**

2편의 단순 회귀와의 차이:
| | 단순 회귀 | 다중 회귀 |
|--|---------|---------|
| 독립변수 | 1개 | 2개+ |
| 모델 | y = ax + b | y = a1*x1 + a2*x2 + ... + b |
| 주의점 | - | **다중공선성** 확인 필수 |

### 다중공선성 (Multicollinearity)
독립변수들끼리 높은 상관이 있으면 회귀 계수가 불안정해진다.
**VIF (Variance Inflation Factor)**로 진단:
- VIF < 5: 문제 없음
- VIF 5~10: 주의
- VIF > 10: 심각한 공선성 -> 변수 제거 또는 PCA

### Agent 지시 예시
> "bill_length, bill_depth, flipper_length로 body_mass를 예측하는 다중 회귀를 해줘.
> 각 변수의 회귀 계수, p-value, R-squared를 보고하고 VIF도 확인해줘."
"""),

code("""# 다중 회귀: statsmodels (통계적 상세 결과)
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

X = df[['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm']]
y = df['body_mass_g']

# 상수항 추가 (절편)
X_const = sm.add_constant(X)

model = sm.OLS(y, X_const).fit()
print(model.summary())"""),

code("""# VIF (다중공선성 진단)
print('=== VIF (Variance Inflation Factor) ===')
print()
for i, col in enumerate(X.columns):
    vif = variance_inflation_factor(X.values, i)
    status = 'OK' if vif < 5 else ('주의' if vif < 10 else '심각!')
    print(f'  {col:20s}: VIF = {vif:.2f}  [{status}]')
print()
print('  VIF < 5: 문제 없음')
print('  VIF 5~10: 주의')
print('  VIF > 10: 변수 제거 또는 PCA 고려')"""),

code("""# 편상관 (Partial Correlation)
# "다른 변수들의 영향을 제거한 후의 순수한 관계"
# 예: flipper와 body_mass의 상관에서 bill_length, bill_depth의 영향을 제거

def partial_corr(df, x, y, covariates):
    \"\"\"x와 y의 편상관: covariates의 영향을 제거한 순수 상관\"\"\"
    from sklearn.linear_model import LinearRegression
    # x에서 covariates의 영향 제거 -> 잔차
    cov = df[covariates].values
    model_x = LinearRegression().fit(cov, df[x])
    model_y = LinearRegression().fit(cov, df[y])
    resid_x = df[x] - model_x.predict(cov)
    resid_y = df[y] - model_y.predict(cov)
    return stats.pearsonr(resid_x, resid_y)

print('=== 편상관 분석 ===')
print('flipper_length와 body_mass의 관계 (다른 변수 통제)')
print()

# 단순 상관
r_simple, p_simple = stats.pearsonr(df['flipper_length_mm'], df['body_mass_g'])
print(f'  단순 상관:   r = {r_simple:.3f}, p = {p_simple:.2e}')

# 편상관 (bill_length, bill_depth 통제)
r_partial, p_partial = partial_corr(df, 'flipper_length_mm', 'body_mass_g',
                                     ['bill_length_mm', 'bill_depth_mm'])
print(f'  편상관:      r = {r_partial:.3f}, p = {p_partial:.2e}')
print()
print('  -> 다른 변수를 통제하면 순수한 관계가 얼마나 변하는지 확인')
print('     제3변수의 영향을 배제한 "진짜 관계"를 볼 수 있다')"""),

# ---- 3-B: PCA + t-SNE ----
md("""---
## 3-B. 차원 축소 & 시각화

고차원(변수가 많은) 데이터를 2~3차원으로 압축해서 **눈으로 보는** 방법.

| 방법 | 특징 | 용도 |
|------|------|------|
| **PCA** | 분산을 최대한 보존하며 축소. 선형 | 변수 요약, 노이즈 제거, 공선성 해결 |
| **t-SNE** | 가까운 점은 가깝게, 먼 점은 멀게. 비선형 | 군집 시각화, 패턴 발견 |
| **UMAP** | t-SNE보다 빠르고 전역 구조 보존 | 대규모 데이터 시각화 |

### PCA 핵심 개념
- 원래 변수들의 **선형 조합**으로 새로운 축(주성분)을 만든다
- PC1이 가장 많은 분산을 설명, PC2가 그 다음, ...
- **설명 분산 비율**: PC 몇 개로 원본의 몇 %를 설명하는가?
- **적재량(loadings)**: 각 원래 변수가 주성분에 기여하는 정도

### Agent 지시 예시
> "수치형 변수들에 PCA를 적용해줘.
> 설명 분산 비율, 스크리 플롯, PC1-PC2 산점도(종별 색구분)를 보여줘.
> 각 PC에 어떤 원래 변수가 기여하는지 적재량도 알려줘."
"""),

code("""# PCA
from sklearn.decomposition import PCA

# 표준화 (PCA 전에 필수 - 단위가 다르면 큰 값이 지배)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[numeric_cols])

pca = PCA()
X_pca = pca.fit_transform(X_scaled)

# 설명 분산 비율
print('=== PCA 설명 분산 비율 ===')
for i, (var, cum) in enumerate(zip(pca.explained_variance_ratio_,
                                    np.cumsum(pca.explained_variance_ratio_))):
    print(f'  PC{i+1}: {var:.3f} ({var*100:.1f}%)  누적: {cum:.3f} ({cum*100:.1f}%)')

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# 스크리 플롯
axes[0].bar(range(1, len(pca.explained_variance_ratio_)+1),
            pca.explained_variance_ratio_, edgecolor='black', alpha=0.7)
axes[0].plot(range(1, len(pca.explained_variance_ratio_)+1),
             np.cumsum(pca.explained_variance_ratio_), 'ro-')
axes[0].set_xlabel('Principal Component')
axes[0].set_ylabel('Explained Variance Ratio')
axes[0].set_title('Scree Plot')
axes[0].set_xticks(range(1, len(numeric_cols)+1))

# PC1-PC2 산점도 (종별 색구분)
species_list = df['species'].unique()
colors = ['blue', 'orange', 'green']
for sp, c in zip(species_list, colors):
    mask = df['species'] == sp
    axes[1].scatter(X_pca[mask, 0], X_pca[mask, 1], c=c, label=sp, alpha=0.6)
axes[1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
axes[1].set_title('PCA: PC1 vs PC2')
axes[1].legend()

plt.tight_layout()
plt.show()"""),

code("""# PCA 적재량 (Loadings): 각 원래 변수의 기여도
loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f'PC{i+1}' for i in range(len(numeric_cols))],
    index=numeric_cols
)
print('=== PCA Loadings (적재량) ===')
print(loadings.round(3))
print()
print('해석 예시:')
for i in range(2):
    dominant = loadings[f'PC{i+1}'].abs().idxmax()
    print(f'  PC{i+1}: {dominant}의 영향이 가장 큼 (loading={loadings.loc[dominant, f"PC{i+1}"]:.3f})')"""),

code("""# t-SNE: 비선형 차원 축소 (군집 시각화에 강력)
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=42, perplexity=30)
X_tsne = tsne.fit_transform(X_scaled)

plt.figure(figsize=(7, 5))
for sp, c in zip(species_list, colors):
    mask = df['species'] == sp
    plt.scatter(X_tsne[mask, 0], X_tsne[mask, 1], c=c, label=sp, alpha=0.6)
plt.xlabel('t-SNE 1')
plt.ylabel('t-SNE 2')
plt.title('t-SNE Visualization')
plt.legend()
plt.show()

print('t-SNE 주의사항:')
print('  - 축의 값 자체는 의미 없음 (거리 비교 불가)')
print('  - perplexity 파라미터에 결과가 민감')
print('  - 전역 구조보다 지역 구조(군집)를 잘 보여줌')
print('  - 매번 결과가 다를 수 있음 (random_state 고정 필요)')"""),

# ---- 3-C: 군집화 ----
md("""---
## 3-C. 군집화 (Clustering) - 비지도 학습

정답 레이블 없이 **데이터 자체의 구조**를 발견하는 방법.
"이 데이터에서 자연스러운 그룹이 있는가?"

| 방법 | 특징 | 장점 | 단점 |
|------|------|------|------|
| **K-Means** | K개 군집 중심으로 분할 | 빠르고 직관적 | K를 미리 지정해야 함 |
| **DBSCAN** | 밀도 기반 군집화 | 군집 수 자동, 이상치 탐지 | eps, min_samples 조정 필요 |
| **계층적 (Hierarchical)** | 트리 구조로 병합/분할 | 덴드로그램으로 시각화 | 대규모 데이터에 느림 |

### 군집 수(K) 결정: Elbow Method + Silhouette Score

### Agent 지시 예시
> "수치형 변수를 표준화하고 K-Means 군집화를 해줘.
> Elbow method와 Silhouette score로 최적 K를 찾고,
> 군집 결과를 PCA 2D로 시각화해줘."
"""),

code("""# K-Means: Elbow Method + Silhouette Score
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

inertias = []
sil_scores = []
K_range = range(2, 8)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, labels))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Elbow
axes[0].plot(K_range, inertias, 'bo-')
axes[0].set_xlabel('K (Number of Clusters)')
axes[0].set_ylabel('Inertia (Within-cluster SS)')
axes[0].set_title('Elbow Method')

# Silhouette
axes[1].plot(K_range, sil_scores, 'ro-')
axes[1].set_xlabel('K (Number of Clusters)')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Score (higher = better)')

plt.tight_layout()
plt.show()

best_k = list(K_range)[np.argmax(sil_scores)]
print(f'Silhouette 최적 K = {best_k} (score = {max(sil_scores):.3f})')"""),

code("""# K-Means 결과 시각화 (PCA 2D)
best_km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
cluster_labels = best_km.fit_predict(X_scaled)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# K-Means 군집
scatter = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels, cmap='viridis', alpha=0.6)
axes[0].set_title(f'K-Means (K={best_k})')
axes[0].set_xlabel('PC1')
axes[0].set_ylabel('PC2')
plt.colorbar(scatter, ax=axes[0], label='Cluster')

# 실제 종과 비교
species_num = LabelEncoder().fit_transform(df['species'])
scatter2 = axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=species_num, cmap='viridis', alpha=0.6)
axes[1].set_title('Actual Species')
axes[1].set_xlabel('PC1')
axes[1].set_ylabel('PC2')
plt.colorbar(scatter2, ax=axes[1], label='Species')

plt.tight_layout()
plt.show()

# 군집과 실제 종의 일치도
ct = pd.crosstab(df['species'], cluster_labels, colnames=['Cluster'])
print('=== 군집 vs 실제 종 ===')
print(ct)"""),

code("""# DBSCAN: 밀도 기반 군집화
from sklearn.cluster import DBSCAN

db = DBSCAN(eps=1.2, min_samples=5)
db_labels = db.fit_predict(X_scaled)

n_clusters = len(set(db_labels)) - (1 if -1 in db_labels else 0)
n_noise = (db_labels == -1).sum()

plt.figure(figsize=(7, 5))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=db_labels, cmap='viridis', alpha=0.6)
plt.colorbar(scatter, label='Cluster (-1 = noise)')
plt.title(f'DBSCAN: {n_clusters} clusters, {n_noise} noise points')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()

print(f'군집 수: {n_clusters}')
print(f'노이즈(이상치): {n_noise}개')
print()
print('DBSCAN 장점: 군집 수를 자동 결정, 이상치를 -1로 분리')
print('DBSCAN 단점: eps와 min_samples 파라미터에 민감')"""),

code("""# 계층적 군집화 (Hierarchical Clustering) + 덴드로그램
from scipy.cluster.hierarchy import dendrogram, linkage

# 표본 추출 (덴드로그램은 전체 표시하면 너무 복잡)
sample_idx = np.random.RandomState(42).choice(len(X_scaled), 50, replace=False)
X_sample = X_scaled[sample_idx]
species_sample = df['species'].values[sample_idx]

linkage_matrix = linkage(X_sample, method='ward')

plt.figure(figsize=(14, 5))
dendrogram(linkage_matrix,
           labels=species_sample,
           leaf_rotation=90,
           leaf_font_size=8)
plt.title('Hierarchical Clustering Dendrogram (50 samples)')
plt.ylabel('Distance')
plt.tight_layout()
plt.show()

print('덴드로그램 읽는 법:')
print('  - 아래에서 위로: 가장 가까운 점들이 먼저 병합')
print('  - 수평선 높이: 병합될 때의 거리 (높을수록 멀리 떨어진 군집)')
print('  - 특정 높이에서 수평으로 자르면 -> 그 수의 군집이 됨')"""),

# ---- 3-D: 분류 ----
md("""---
## 3-D. 분류 & 예측 (지도 학습)

정답 레이블이 있을 때, **새로운 데이터의 레이블을 예측**하는 방법.

| 방법 | 특징 | 장점 |
|------|------|------|
| **Logistic Regression** | 선형 경계, 확률 출력 | 해석 용이, 기준선(baseline) |
| **Random Forest** | 앙상블(여러 결정 트리 투표) | 비선형, Feature Importance 제공 |
| **SVM** | 마진 최대화 경계 | 고차원에 강함 |
| **KNN** | 가장 가까운 K개 이웃 투표 | 단순, 직관적 |

### 핵심: 교차 검증 (Cross-Validation)
- 데이터를 K등분하여 K번 학습/평가를 반복
- 과적합(overfitting) 방지, 성능의 안정적 추정
- **절대 테스트 데이터로 학습하지 않는다**

### Agent 지시 예시
> "수치형 변수로 종(species)을 분류하는 Random Forest를 만들어줘.
> 5-fold 교차 검증으로 정확도를 보고하고, Feature Importance도 그려줘."
"""),

code("""# Random Forest 분류 + 교차 검증
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix

X = df[numeric_cols].values
y = LabelEncoder().fit_transform(df['species'])
species_names = df['species'].unique()

# 5-fold 교차 검증
rf = RandomForestClassifier(n_estimators=100, random_state=42)
scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')

print('=== Random Forest 5-Fold CV ===')
print(f'  Accuracy: {scores.mean():.3f} +/- {scores.std():.3f}')
print(f'  각 Fold: {[f"{s:.3f}" for s in scores]}')
print()

# 교차 검증 예측으로 혼동 행렬
y_pred = cross_val_predict(rf, X, y, cv=5)
print('=== Classification Report ===')
print(classification_report(y, y_pred, target_names=species_names))"""),

code("""# 혼동 행렬 시각화
cm = confusion_matrix(y, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=species_names, yticklabels=species_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (5-Fold CV)')
plt.tight_layout()
plt.show()

print('혼동 행렬 읽는 법:')
print('  - 대각선: 맞춘 개수')
print('  - 비대각선: 틀린 개수 (어떤 종을 어떤 종으로 오분류했는지)')"""),

# ---- 3-E: 모델 해석 ----
md("""---
## 3-E. 모델 해석 (Feature Importance & SHAP)

모델이 **왜 그런 예측을 했는가?** 단순히 정확도만 보고하면 연구가 아니다.

| 방법 | 원리 | 장점 |
|------|------|------|
| **Feature Importance** (RF 내장) | 각 변수가 분할에 기여한 정도 | 빠름, 직관적 |
| **Permutation Importance** | 변수를 섞었을 때 성능 하락 정도 | 모델 무관, 더 신뢰성 |
| **SHAP** | 게임이론 기반 각 변수의 기여도 | 개별 예측 해석 가능, 가장 상세 |

### 주의: Feature Importance의 함정
- RF 내장 Importance는 **상관된 변수에 편향**될 수 있다
- 상관된 변수 A, B가 있으면 둘 다 중요도가 낮게 나옴 (서로 나눠가짐)
- **Permutation Importance**가 더 신뢰할 만하다

### Agent 지시 예시
> "Random Forest의 Feature Importance와 Permutation Importance를 비교해줘.
> SHAP summary plot도 그려줘."
"""),

code("""# Feature Importance 비교
from sklearn.inspection import permutation_importance

# 모델 학습 (전체 데이터로, 해석 목적)
rf.fit(X, y)

# 1) RF 내장 Feature Importance
fi_builtin = rf.feature_importances_

# 2) Permutation Importance
perm_result = permutation_importance(rf, X, y, n_repeats=30, random_state=42)
fi_perm = perm_result.importances_mean

# 비교 시각화
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

idx = np.argsort(fi_builtin)
axes[0].barh(range(len(numeric_cols)), fi_builtin[idx], edgecolor='black', alpha=0.7)
axes[0].set_yticks(range(len(numeric_cols)))
axes[0].set_yticklabels([numeric_cols[i] for i in idx])
axes[0].set_title('RF Built-in Feature Importance')

idx2 = np.argsort(fi_perm)
axes[1].barh(range(len(numeric_cols)), fi_perm[idx2], edgecolor='black', alpha=0.7)
axes[1].set_yticks(range(len(numeric_cols)))
axes[1].set_yticklabels([numeric_cols[i] for i in idx2])
axes[1].set_title('Permutation Feature Importance')

plt.tight_layout()
plt.show()

print('=== Feature Importance 비교 ===')
for col, bi, pi in zip(numeric_cols, fi_builtin, fi_perm):
    print(f'  {col:20s}: Built-in={bi:.3f}, Permutation={pi:.3f}')"""),

code("""# SHAP (SHapley Additive exPlanations)
# Colab: !pip install shap
try:
    import shap

    explainer = shap.TreeExplainer(rf)
    shap_values = explainer.shap_values(X)

    # Summary Plot: 전체 변수의 중요도 + 방향
    plt.figure()
    shap.summary_plot(shap_values, X, feature_names=numeric_cols,
                      class_names=list(species_names), show=False)
    plt.tight_layout()
    plt.show()

    print('SHAP Summary Plot 읽는 법:')
    print('  - x축: SHAP 값 (양수=해당 클래스 예측에 기여, 음수=반대)')
    print('  - 색상: 변수 값의 크기 (빨강=높은 값, 파랑=낮은 값)')
    print('  - 각 점은 하나의 데이터 포인트')

except ImportError:
    print('shap 패키지가 설치되지 않았습니다.')
    print('Colab에서: !pip install shap')
    print()
    print('SHAP이 제공하는 것:')
    print('  1) 각 변수가 각 예측에 얼마나 기여했는지 수치화')
    print('  2) Summary plot: 전체 변수 중요도 + 방향')
    print('  3) Force plot: 개별 예측의 이유 시각화')
    print('  4) Dependence plot: 특정 변수와 SHAP 값의 관계')"""),

# ---- 3-F: 실전 워크플로우 ----
md("""---
## 3-F. 실전 분석 워크플로우

실제 연구에서 다변량 분석을 수행하는 전체 흐름.

```
[1] 데이터 탐색 (EDA)
    |-- 각 변수 단변량 분석 (1편)
    |-- 주요 변수 쌍 이변량 분석 (2편)
    |-- 상관행렬로 전체 관계 조망
    |
[2] 전처리
    |-- 결측치 처리 (dropna / 대체)
    |-- 이상치 처리 (제거 / 변환)
    |-- 표준화 (StandardScaler) - 단위가 다른 변수들
    |-- 인코딩 (범주형 -> 숫자) - LabelEncoder / OneHotEncoder
    |
[3] 차원 축소 & 군집화 (탐색적)
    |-- PCA / t-SNE로 구조 시각화
    |-- K-Means / DBSCAN으로 자연적 그룹 발견
    |
[4] 모델링
    |-- 연속 종속변수: 다중 회귀 + VIF
    |-- 범주 종속변수: 분류 (RF, Logistic, SVM)
    |-- 교차 검증으로 성능 평가
    |
[5] 해석
    |-- Feature Importance / SHAP
    |-- 통계적 유의성 보고
    |-- 효과 크기 보고
    |
[6] 보고
    |-- 결과 재현 가능하게 정리 (random_state 고정)
    |-- 한계점 명시
    |-- 코드와 데이터 공유
```
"""),

# ---- 요약 ----
md("""---
## 3편 요약: 다변량 분석 선택 가이드

```
변수 3개 이상 -> 목적이 무엇인가?
|
|-- 관계/영향력 파악
|     |-- 종속변수 있음 (수치): 다중 회귀 + VIF
|     |-- 종속변수 있음 (범주): 분류 (RF, Logistic)
|     |-- 종속변수 없음: 편상관, 상관행렬
|
|-- 구조/패턴 발견
|     |-- 차원 축소: PCA (설명), t-SNE (시각화)
|     |-- 군집화: K-Means (K 알 때), DBSCAN (K 모를 때)
|     |-- 계층적: 덴드로그램
|
|-- 모델 해석
      |-- 어떤 변수가 중요?: Feature Importance, Permutation
      |-- 왜 이 예측?: SHAP
```

### Agent 통합 지시 예시
> "이 데이터를 종합적으로 분석해줘:
> 1) 상관행렬로 변수 간 관계를 보고
> 2) PCA로 차원 축소해서 시각화하고
> 3) [종속변수]를 예측하는 모델을 만들어서 교차 검증하고
> 4) Feature Importance와 SHAP으로 어떤 변수가 중요한지 해석해줘."

### 1~3편 전체 분석 요약

| 변수 수 | 핵심 질문 | 대표 방법 |
|---------|----------|----------|
| **1개** | "어떻게 생겼는가?" | 기술통계, 정규성, KDE, 이상치 |
| **2개** | "둘 사이에 관계가 있는가?" | 상관, 회귀, t-test, ANOVA, 카이제곱 |
| **3개+** | "여러 변수가 동시에 어떻게 작용하는가?" | 다중회귀, PCA, 군집화, 분류, SHAP |
"""),
    ]
    save("RnE 3. Three+ Features (다변량 분석).ipynb", cells)


# ============================================================
# 빌드 실행
# ============================================================
print("Building R&E notebooks...")
build_part1()
build_part2()
build_part3()
print("Done!")
