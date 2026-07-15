# -*- coding: utf-8 -*-
"""
선형회귀 문제 3개 + 그래프 생성.

ml-lr-001 : R^2 낮은 그래프 vs 높은 그래프 -> 성능 비교 + 낮은 이유 (한 문장 서술)
ml-lr-002 : sklearn LinearRegression 코드 -> 무엇을 예측 / 회귀(숫자) 서술
ml-lr-003 : 이상치로 틀어진 회귀 -> 원인·해결 서술

원칙: 문제/그래프가 답을 떠먹이지 않게(이상치 강조·정답 범례 등 힌트 제거).
수식 없이 그래프 해석 위주. R^2는 '클수록 잘 맞음' 수준.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

HERE = os.path.dirname(__file__)
IMGDIR = os.path.join(HERE, '..', 'exam-builder', 'frontend', 'public', 'images')
OUT = os.path.join(HERE, '..', 'exam-builder', 'frontend', 'src', 'data',
                   'problems-cnsh-26-1-2-10.json')

LR_CODE = '''from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X, y)        # X: 공부 시간, y: 시험 점수
print(model.predict([[7]]))   # 공부 7시간일 때'''


def scatter_r2():
    rng = np.random.RandomState(1)
    x = np.linspace(1, 10, 25)
    y_low = 2.0 * x + 5 + rng.randn(25) * 9.0     # 분산 큼 -> R^2 낮음
    y_high = 2.0 * x + 5 + rng.randn(25) * 2.0    # 분산 작음 -> R^2 높음
    X = x.reshape(-1, 1)
    fig, axes = plt.subplots(2, 1, figsize=(5, 7))
    r2s = []
    for ax, yy, tag in [(axes[0], y_low, 'A'), (axes[1], y_high, 'B')]:
        m = LinearRegression().fit(X, yy)
        r2 = r2_score(yy, m.predict(X))
        r2s.append(r2)
        xs = np.array([[0], [11]])
        ax.scatter(x, yy, c='tab:blue', s=45, edgecolors='k', zorder=3)
        ax.plot(xs, m.predict(xs), c='red', lw=2)
        ax.set_title('graph %s  (R2 = %.2f)' % (tag, r2))
        ax.set_xlabel('x'); ax.set_ylabel('y'); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, 'lr-r2.png'), dpi=150)
    plt.close()
    return r2s[0], r2s[1]   # A(낮음), B(높음)


def scatter_outlier():
    rng = np.random.RandomState(4)
    x = np.arange(1, 11)
    y = 2.0 * x + 3 + rng.randn(10) * 1.0
    xo = np.append(x, 3).reshape(-1, 1)
    yo = np.append(y, 35.0)                        # 동떨어진 이상치(강조하지 않음)
    m_all = LinearRegression().fit(xo, yo)         # 이상치 포함 회귀선만 표시
    xs = np.array([[0], [11]])
    plt.figure(figsize=(5, 4))
    plt.scatter(xo.ravel(), yo, c='tab:blue', s=60, edgecolors='k', zorder=3)  # 모든 점 동일 마커
    plt.plot(xs, m_all.predict(xs), c='red', lw=2)
    plt.xlabel('x'); plt.ylabel('y'); plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, 'lr-outlier.png'), dpi=150)
    plt.close()


def proc(points):
    return {"type": "process-box", "title": "채점 포인트",
            "content": [{"type": "text", "content": t} for t in points]}


def build():
    os.makedirs(IMGDIR, exist_ok=True)
    r2_low, r2_high = scatter_r2()
    scatter_outlier()

    problems = [
        {
            "id": "ml-lr-001", "type": "explain",
            "content": [
                {"type": "text", "content": "같은 종류의 데이터에 각각 선형회귀(빨간 직선)를 적용한 두 그래프 A, B다. (R2는 결정계수)"},
                {"type": "image", "src": "/images/lr-r2.png", "alt": "R2 비교", "width": 80, "align": "center"},
                {"type": "text", "content": "A와 B 중 예측 성능이 더 좋은 쪽을 고르고, 그렇게 판단한 근거와 성능이 낮은 쪽이 왜 낮은지 서술하시오."},
                {"type": "answer-box", "lines": 6},
            ],
            "answer": {"type": "value", "value": "B(R2=%.2f)가 A(R2=%.2f)보다 성능이 좋다. R2가 1에 가까울수록 점들이 직선에 가깝게 모여 예측이 잘 맞기 때문이다. A는 점들이 직선에서 멀리 넓게 흩어져 있어(분산이 큼) 직선으로 예측하기 어려워 R2가 낮다." % (r2_high, r2_low)},
            "explain": [proc([
                "R2(결정계수)는 1에 가까울수록 데이터가 직선에 잘 맞는다는 뜻.",
                "B의 R2(%.2f)가 A의 R2(%.2f)보다 크므로 B가 성능이 좋다." % (r2_high, r2_low),
                "A가 낮은 이유: 점들이 직선에서 멀리 흩어져 있어(큰 분산) 직선이 잘 설명하지 못한다.",
                "(이상치/비선형 관계도 R2를 낮추는 원인으로 언급하면 가점)",
            ])],
        },
        {
            "id": "ml-lr-002", "type": "explain",
            "content": [
                {"type": "text", "content": "다음 코드를 읽고 물음에 답하시오."},
                {"type": "code", "language": "python", "content": LR_CODE},
                {"type": "text", "content": "이 코드가 무엇을 예측하는지 쓰고, 그 예측 결과가 분류와 회귀 중 어느 것에 해당하는지 이유와 함께 서술하시오."},
                {"type": "answer-box", "lines": 5},
            ],
            "answer": {"type": "value", "value": "공부 시간(X)으로 시험 점수(y)를, 특히 7시간 공부했을 때의 예상 점수를 예측한다. 예측 결과는 숫자(회귀)다. 시험 점수처럼 연속적인 수치를 예측하므로 회귀이며, 범주(합격/불합격 등)를 고르는 분류와 다르다."},
            "explain": [proc([
                "fit(X, y)로 공부시간-점수 관계를 학습하고 predict([[7]])로 7시간일 때 점수를 예측.",
                "점수는 연속적인 숫자 -> 회귀(LinearRegression).",
                "범주를 고르는 분류와 구분되면 정답.",
            ])],
        },
        {
            "id": "ml-lr-003", "type": "explain",
            "content": [
                {"type": "text", "content": "어떤 데이터에 선형회귀를 적용했더니 회귀직선(빨간 선)이 대부분의 점들과 동떨어지게 나왔다."},
                {"type": "image", "src": "/images/lr-outlier.png", "alt": "회귀 결과", "width": 85, "align": "center"},
                {"type": "text", "content": "이 직선이 데이터의 경향과 맞지 않는 원인이 무엇인지, 그리고 어떻게 해결해야 하는지 서술하시오."},
                {"type": "answer-box", "lines": 6},
            ],
            "answer": {"type": "value", "value": "데이터 대부분은 일정한 직선 경향을 보이는데, 멀리 동떨어진 점(이상치) 하나가 회귀직선을 그 쪽으로 끌어당겨 직선이 대부분의 점에서 벗어났다. 전처리 단계에서 이런 이상치를 찾아 제거(또는 수정)한 뒤 다시 학습해야 한다."},
            "explain": [proc([
                "원인: 다른 점들과 크게 떨어진 이상치 1개가 회귀직선을 끌어당겼다.",
                "선형회귀는 모든 점과의 오차를 줄이려 하므로 멀리 있는 한 점에도 크게 흔들린다.",
                "해결: 전처리에서 이상치를 찾아 제거/수정한 뒤 다시 학습한다.",
            ])],
        },
    ]

    json.dump(problems, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for p in problems:
        print("OK", p["id"])
    print("R2_A(low)=%.2f, R2_B(high)=%.2f" % (r2_low, r2_high))
    print("saved:", OUT)


if __name__ == '__main__':
    build()
