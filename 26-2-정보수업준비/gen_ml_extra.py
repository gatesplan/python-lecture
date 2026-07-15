# -*- coding: utf-8 -*-
"""
ML 서술형 추가분 (기존 51문항에 없던 주제 보강).

ml-rf-001~003   : 앙상블/랜덤포레스트 (다수결 안정성, 과적합 저항, 투표 계산)   [이미지]
ml-sel-001~002  : 알고리즘 선택 맵 적용 (상황->지도/비지도+회귀/분류/군집)        [이미지]
ml-logit-001~002: 로지스틱회귀가 '어떻게' 분류하나 (확률->0.5 기준->범주)        [이미지]
ml-trap-001~002 : 함정형 (정확도 함정 / 상관 != 인과)                            [이미지]

근거: 기계학습-이론요약.md(가르친 범위), 시험정보(코드/파라미터 불요, 서술형),
      기말고사-시험범위(함정 포함, AI 흐름 이해형). 인-피겨 텍스트는 영문 관례.
출력 파일: problems-cnsh-26-1-2-17.json (glob 자동 로딩)
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
IMGDIR = os.path.join(HERE, '..', 'exam-builder', 'frontend', 'public', 'images')
OUT = os.path.join(HERE, '..', 'exam-builder', 'frontend', 'src', 'data',
                   'problems-cnsh-26-1-2-17.json')


def proc(points):
    return {"type": "process-box", "title": "채점 포인트",
            "content": [{"type": "text", "content": t} for t in points]}


def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, name), dpi=150)
    plt.close()


# ---------------- 이미지 생성 ----------------

def img_rf_vote():
    votes = ['A', 'A', 'B', 'A', 'A']
    n = len(votes)
    xs = [1.2 + i * 1.6 for i in range(n)]
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    top = 4.0
    for i, (x, v) in enumerate(zip(xs, votes)):
        wrong = (v == 'B')
        fc = '#e0a0a0' if wrong else '#9bb8de'
        tri = plt.Polygon([[x - 0.55, top - 0.7], [x + 0.55, top - 0.7], [x, top + 0.35]],
                          closed=True, facecolor=fc, edgecolor='black')
        ax.add_patch(tri)
        ax.text(x, top - 0.95, 'Tree %d' % (i + 1), ha='center', va='top', fontsize=10)
        ax.text(x, top - 0.15, v, ha='center', va='center', fontsize=15, fontweight='bold')
        ax.annotate('', xy=(x, 1.55), xytext=(x, top - 1.05),
                    arrowprops=dict(arrowstyle='->', color='gray'))
    box = plt.Rectangle((xs[0] - 0.7, 0.75), xs[-1] - xs[0] + 1.4, 0.8,
                        facecolor='#f0f0f0', edgecolor='black')
    ax.add_patch(box)
    ax.text((xs[0] + xs[-1]) / 2, 1.15, 'Majority vote', ha='center', va='center', fontsize=12)
    ax.text((xs[0] + xs[-1]) / 2, 0.25, 'Predict: A   (A:4  vs  B:1)', ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1e6b2e')
    ax.set_xlim(0, xs[-1] + 1.2)
    ax.set_ylim(0, 5)
    ax.axis('off')
    save('rfx-vote.png')


def img_rf_table():
    col = ['', 'Tree1', 'Tree2', 'Tree3', 'Tree4', 'Tree5']
    rows = [['X1', 'A', 'A', 'A', 'B', 'A'],
            ['X2', 'A', 'B', 'A', 'B', 'A']]
    fig, ax = plt.subplots(figsize=(6.2, 1.9))
    ax.axis('off')
    tbl = ax.table(cellText=rows, colLabels=col, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 1.7)
    save('rfx-table.png')


def img_sel_map():
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 10)
    ax.axis('off')

    def box(x, y, w, h, text, fc='#eef3ff'):
        ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor=fc, edgecolor='black'))
        ax.text(x, y, text, ha='center', va='center', fontsize=10)

    def arrow(x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->'))
        if label:
            ax.text((x1 + x2) / 2 + 0.25, (y1 + y2) / 2, label, fontsize=10, color='#1f4fa0')

    box(6.5, 9.0, 4.6, 1.0, 'Has answer labels (y)?')
    # No -> unsupervised
    box(2.6, 6.3, 3.2, 1.0, 'No\n(no labels)', '#f3eaff')
    box(2.6, 3.6, 3.4, 1.3, 'Unsupervised\nClustering\n(k-Means)', '#e8f6e8')
    arrow(4.6, 8.55, 3.0, 6.85, 'No')
    arrow(2.6, 5.75, 2.6, 4.3)
    # Yes -> supervised
    box(9.6, 6.3, 4.4, 1.0, 'Yes: predict a\nnumber or a category?', '#fff6e6')
    arrow(8.4, 8.55, 9.6, 6.85, 'Yes')
    box(7.4, 3.4, 3.2, 1.5, 'Number ->\nRegression\n(Linear Reg.)', '#fff6e6')
    box(11.0, 3.2, 3.6, 1.9, 'Category ->\nClassification\n(k-NN, Tree,\nLogistic, RandomForest)', '#fdecec')
    arrow(8.4, 5.75, 7.6, 4.2, 'number')
    arrow(10.6, 5.75, 11.0, 4.2, 'category')
    save('sel-map.png')


def img_sigmoid(points=None, name='logit-curve.png'):
    z = np.linspace(-6, 6, 400)
    p = 1.0 / (1.0 + np.exp(-z))
    fig, ax = plt.subplots(figsize=(5.4, 3.7))
    ax.plot(z, p, color='#2a6fb0', lw=2.2)
    ax.axhline(0.5, ls='--', color='gray')
    ax.axvline(0, ls=':', color='gray')
    ax.text(-5.9, 0.12, 'class 0  (p < 0.5)', color='#c0392b', fontsize=10)
    ax.text(0.6, 0.9, 'class 1  (p > 0.5)', color='#1e8449', fontsize=10)
    ax.text(0.15, 0.53, '0.5', color='gray', fontsize=9)
    if points:
        for name_, pp in points:
            zz = float(np.log(pp / (1 - pp)))
            ax.plot(zz, pp, 'o', color='black', ms=7)
            dy = 12 if pp < 0.5 else -16
            ax.annotate('%s (p=%.2f)' % (name_, pp), (zz, pp),
                        textcoords='offset points', xytext=(8, dy), fontsize=9)
    ax.set_xlabel('model output (z)')
    ax.set_ylabel('probability')
    ax.set_ylim(-0.05, 1.08)
    ax.set_title('Logistic (sigmoid) function')
    save(name)


def img_trap_acc():
    CM = np.array([[950, 0], [50, 0]])  # [[TN,FP],[FN,TP]]
    fig, ax = plt.subplots(figsize=(4.4, 3.8))
    ax.imshow(CM, cmap='Blues')
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(CM[i, j]), ha='center', va='center',
                    fontsize=18, color='white' if CM[i, j] > 300 else 'black')
    ax.set_xticks([0, 1]); ax.set_xticklabels(['Pred: Neg', 'Pred: Pos'])
    ax.set_yticks([0, 1]); ax.set_yticklabels(['Actual: Neg', 'Actual: Pos'])
    ax.set_xlabel('predicted'); ax.set_ylabel('actual')
    ax.set_title('Model predicts everything as Neg')
    save('trap-acc-cm.png')


def img_trap_corr():
    rng = np.random.RandomState(7)
    temp = np.linspace(22, 35, 45) + rng.normal(0, 0.5, 45)
    icecream = (temp - 18) * 9 + rng.normal(0, 8, 45)
    drown = (temp - 18) * 1.3 + rng.normal(0, 1.2, 45)
    fig, ax = plt.subplots(figsize=(5.4, 3.9))
    sc = ax.scatter(icecream, drown, c=temp, cmap='coolwarm', edgecolor='k', s=40)
    cb = plt.colorbar(sc)
    cb.set_label('temperature (C)')
    ax.set_xlabel('ice cream sales')
    ax.set_ylabel('drowning accidents')
    ax.set_title('high correlation (R2 ~ 0.9)')
    ax.text(0.04, 0.92, 'hidden cause: temperature', transform=ax.transAxes,
            fontsize=9, color='#7a3b3b',
            bbox=dict(boxstyle='round', fc='#fdecec', ec='#c08a8a'))
    save('trap-corr.png')


# ---------------- 문제 ----------------

PROBLEMS = [
    {
        "id": "ml-rf-001", "type": "explain",
        "content": [
            {"type": "text", "content": "아래 그림은 의사결정트리 5개로 이루어진 랜덤 포레스트가 새 데이터 하나를 분류하는 과정이다. (각 트리는 A 또는 B로 예측)"},
            {"type": "image", "src": "/images/rfx-vote.png", "alt": "랜덤포레스트 다수결", "width": 95, "align": "center"},
            {"type": "text", "content": "랜덤 포레스트처럼 여러 트리의 예측을 모아 다수결로 정하는 방식이, 트리 하나만 쓰는 것보다 더 안정적인(믿을 만한) 이유를 그림을 근거로 서술하시오."},
            {"type": "answer-box", "lines": 6},
        ],
        "answer": {"type": "value", "value": "트리 하나는 우연히 학습 데이터의 잡음에 휘둘려 틀린 예측을 할 수 있다. 그림에서도 Tree 3은 B로 잘못 예측했지만, 나머지 4개 트리가 A로 예측해 다수결 결과는 A로 올바르게 나왔다. 이처럼 서로 조금씩 다른 여러 트리의 예측을 모으면 개별 트리의 실수가 다수에 의해 상쇄되어, 한 트리만 쓸 때보다 예측이 안정적이고 과적합에 강해진다."},
        "explain": [proc([
            "단일 트리는 잡음/우연으로 틀릴 수 있음.",
            "그림: Tree 3만 B(오답), 나머지 4개 A -> 다수결 A로 교정.",
            "여러 트리의 실수가 서로 상쇄(앙상블 효과) -> 더 안정적, 과적합에 강함.",
            "'개별 오류가 다수결로 상쇄된다'가 들어가면 정답.",
        ])],
    },
    {
        "id": "ml-rf-002", "type": "explain",
        "content": [
            {"type": "text", "content": "의사결정트리 하나를 가지를 끝까지 깊게 키우면 학습 데이터는 거의 다 맞히지만 새 데이터에서는 성능이 떨어진다(과적합). 랜덤 포레스트가 이런 과적합에 비교적 강한 이유를, '트리마다 다른 데이터와 특성을 사용한다'는 점과 연결해 서술하시오."},
            {"type": "answer-box", "lines": 6},
        ],
        "answer": {"type": "value", "value": "랜덤 포레스트는 각 트리를 만들 때 전체 데이터에서 일부를 무작위로 뽑고(중복 허용), 사용할 특성도 일부만 무작위로 골라 학습시킨다. 그래서 트리마다 서로 다른 관점으로 조금씩 다르게 학습되어, 특정 데이터의 잡음에 모든 트리가 함께 과적합되지 않는다. 이렇게 서로 다른 트리들의 예측을 다수결/평균으로 합치면 한 트리가 외운 잡음은 묻히고 공통된 패턴만 남아, 단일 트리보다 과적합에 강하다."},
        "explain": [proc([
            "각 트리: 데이터 일부(무작위, 중복허용) + 특성 일부(무작위)로 학습 -> 트리마다 다름.",
            "트리들이 같은 잡음에 함께 과적합되지 않음.",
            "예측을 모으면 개별 잡음은 상쇄되고 공통 패턴만 남음.",
            "'트리마다 다르게 학습 + 모아서 잡음 상쇄'가 핵심.",
        ])],
    },
    {
        "id": "ml-rf-003", "type": "explain",
        "content": [
            {"type": "text", "content": "아래는 의사결정트리 5개로 된 랜덤 포레스트가 두 데이터 X1, X2를 분류한 결과 표다."},
            {"type": "image", "src": "/images/rfx-table.png", "alt": "트리별 투표 결과", "width": 95, "align": "center"},
            {"type": "text", "content": "(1) X1과 X2의 최종 예측을 각각 다수결로 구하시오. (2) X2처럼 표가 3:2로 갈릴 수 있는데, 트리 개수를 짝수가 아니라 홀수로 두면 좋은 이유를 서술하시오. (범주는 2개)"},
            {"type": "answer-box", "lines": 6},
        ],
        "answer": {"type": "value", "value": "(1) X1은 A가 4표, B가 1표이므로 최종 A. X2는 A가 3표, B가 2표이므로 최종 A. (2) 범주가 2개일 때 트리 개수가 홀수이면 두 범주의 표가 동점이 될 수 없어 다수결이 항상 한쪽으로 정해진다. 짝수면 2:2처럼 동점이 나와 어느 쪽으로 결정할지 모호해지는 상황이 생길 수 있다."},
        "explain": [proc([
            "X1: 4:1 -> A.   X2: 3:2 -> A.",
            "홀수 트리: 2범주에서 동점 불가 -> 항상 다수결 결정 가능.",
            "짝수면 동점(예: 2:2) 발생 가능 -> 결정 모호.",
            "(1) 두 최종예측 + (2) 동점 회피 이유가 들어가면 정답.",
        ])],
    },
    {
        "id": "ml-sel-001", "type": "explain",
        "content": [
            {"type": "text", "content": "아래는 머신러닝 문제 해결 맵(알고리즘 선택 흐름)이다."},
            {"type": "image", "src": "/images/sel-map.png", "alt": "알고리즘 선택 맵", "width": 120, "align": "center"},
            {"type": "text", "content": "다음 세 상황을 각각 이 맵에 따라 (가) 지도학습/비지도학습, (나) 회귀/분류/군집 중 무엇인지 판단하고, 알맞은 알고리즘 예를 하나씩 쓰시오."},
            {"type": "condition-box", "title": "상황", "marker": "kr-con", "items": [
                "(1) 메일의 단어/링크 수로 스팸인지 정상인지 가른다 (스팸/정상 정답 표시 있음)",
                "(2) 집의 면적, 방 수로 집값(원)을 예측한다 (실제 가격 정답 있음)",
                "(3) 고객의 구매 기록만으로 비슷한 고객끼리 묶는다 (정답 없음)",
            ]},
            {"type": "answer-box", "lines": 7},
        ],
        "answer": {"type": "value", "value": "(1) 정답(스팸/정상)이 있으므로 지도학습이고, 예측 대상이 범주이므로 분류다. 예: 의사결정트리, k-NN, 로지스틱회귀, 랜덤 포레스트 중 하나. (2) 정답(가격)이 있으므로 지도학습이고, 예측 대상이 연속적인 숫자이므로 회귀다. 예: 선형회귀. (3) 정답이 없으므로 비지도학습이고, 비슷한 것끼리 묶으므로 군집이다. 예: k-Means."},
        "explain": [proc([
            "맵 1단계(정답 있나?): (1)(2) 있음 -> 지도, (3) 없음 -> 비지도.",
            "맵 2단계(지도일 때 숫자/범주?): (1) 범주 -> 분류, (2) 숫자 -> 회귀.",
            "(3) 비지도 + 묶기 -> 군집(k-Means).",
            "세 상황 모두 (지도/비지도)+(회귀/분류/군집)+알고리즘 예가 맞으면 정답.",
        ])],
    },
    {
        "id": "ml-sel-002", "type": "explain",
        "content": [
            {"type": "text", "content": "어떤 학생이 '시험 성적과 관련된 예측은 모두 회귀다'라고 생각한다. 다음 두 작업이 각각 회귀인지 분류인지 구분하고, 그렇게 나뉘는 기준을 서술하시오."},
            {"type": "condition-box", "title": "작업", "marker": "kr-con", "items": [
                "(가) 공부 시간으로 시험 점수(0~100점)를 예측",
                "(나) 공부 시간으로 합격(70점 이상)/불합격을 예측",
            ]},
            {"type": "answer-box", "lines": 6},
        ],
        "answer": {"type": "value", "value": "(가)는 회귀다. 0~100 사이의 연속적인 숫자(점수)를 예측하기 때문이다. (나)는 분류다. 합격/불합격이라는 정해진 범주 중 하나를 예측하기 때문이다. 회귀와 분류를 가르는 기준은 예측 대상이 '연속적인 숫자인가(회귀)' 아니면 '정해진 범주인가(분류)'이며, 같은 성적 주제라도 무엇을 예측하느냐에 따라 달라진다."},
        "explain": [proc([
            "(가) 점수(연속 숫자) 예측 -> 회귀.",
            "(나) 합격/불합격(범주) 예측 -> 분류.",
            "기준: 출력이 숫자면 회귀, 범주면 분류.",
            "'주제가 아니라 예측 대상의 형태로 나뉜다'가 핵심.",
        ])],
    },
    {
        "id": "ml-logit-001", "type": "explain",
        "content": [
            {"type": "text", "content": "아래는 로지스틱회귀가 사용하는 곡선(로지스틱/시그모이드 함수)이다. 가로축은 모델이 계산한 값(z), 세로축은 0~1 사이 확률이며 점선은 0.5 기준이다."},
            {"type": "image", "src": "/images/logit-curve.png", "alt": "로지스틱 곡선", "width": 85, "align": "center"},
            {"type": "text", "content": "로지스틱회귀가 입력 데이터를 받아 최종적으로 두 범주(class 0/class 1) 중 하나로 분류하기까지의 과정을, 이 곡선과 0.5 기준을 이용해 단계적으로 서술하시오."},
            {"type": "answer-box", "lines": 7},
        ],
        "answer": {"type": "value", "value": "1) 입력 특성들을 식에 넣어 하나의 값(z)을 계산한다. 2) 그 값을 로지스틱(시그모이드) 함수에 통과시켜 0~1 사이의 확률로 바꾼다. 3) 이 확률을 기준값 0.5와 비교한다. 4) 확률이 0.5보다 크면 class 1, 작으면 class 0으로 판정한다. 즉 연속적인 확률을 구한 뒤 기준으로 잘라 범주를 정하므로 결과가 범주(분류)다."},
        "explain": [proc([
            "입력 -> 값(z) 계산 -> 시그모이드로 0~1 확률 변환.",
            "확률을 0.5와 비교: >0.5 면 class 1, <0.5 면 class 0.",
            "연속 확률을 기준으로 잘라 범주 결정 -> 분류.",
            "'확률 -> 0.5 기준 -> 범주'의 흐름이 들어가면 정답.",
        ])],
    },
    {
        "id": "ml-logit-002", "type": "explain",
        "content": [
            {"type": "text", "content": "로지스틱회귀 모델이 세 사람 P1, P2, P3에 대해 '양성(class 1)일 확률'을 아래와 같이 계산했다. 기준값은 0.5다. (P1=0.85, P2=0.45, P3=0.20)"},
            {"type": "image", "src": "/images/logit-points.png", "alt": "곡선 위 세 점", "width": 85, "align": "center"},
            {"type": "text", "content": "각 사람을 class 0과 class 1 중 무엇으로 분류할지 쓰고, P2처럼 확률이 0.5에 가까운 경우 그 예측을 얼마나 신뢰할 수 있는지 함께 서술하시오."},
            {"type": "answer-box", "lines": 6},
        ],
        "answer": {"type": "value", "value": "P1은 확률 0.85로 0.5보다 크므로 class 1, P3는 0.20으로 0.5보다 작으므로 class 0으로 분류한다. P2는 0.45로 0.5보다 약간 작아 class 0으로 분류되지만, 확률이 0.5에 매우 가까워 모델이 두 범주를 거의 반반으로 본 것이므로 이 예측은 강하게 신뢰하기 어렵다(경계에 가까운 불확실한 예측)."},
        "explain": [proc([
            "0.5 초과면 class 1, 미만이면 class 0.",
            "P1=0.85 -> class 1,  P3=0.20 -> class 0,  P2=0.45 -> class 0.",
            "P2는 0.5에 근접 -> 확신이 낮은(경계) 예측.",
            "세 분류 결과 + P2 불확실성 언급이 들어가면 정답.",
        ])],
    },
    {
        "id": "ml-trap-001", "type": "explain",
        "content": [
            {"type": "text", "content": "어떤 모델이 정상 950명, 환자 50명(총 1000명)인 데이터에서 모두 '정상'이라고만 예측했다. 아래는 그 혼동행렬이다. (Neg=정상, Pos=환자. 행=실제, 열=예측)"},
            {"type": "image", "src": "/images/trap-acc-cm.png", "alt": "정확도 함정 혼동행렬", "width": 80, "align": "center"},
            {"type": "text", "content": "이 모델의 정확도는 95%로 높다. 그런데도 좋은 모델이라고 할 수 없는 이유를, 혼동행렬의 수치를 근거로 서술하시오."},
            {"type": "answer-box", "lines": 7},
        ],
        "answer": {"type": "value", "value": "이 모델은 모두 정상으로만 찍었기 때문에 정상 950명은 다 맞혀 정확도가 950/1000 = 95%로 높게 나온다. 하지만 정작 찾아내야 할 환자 50명은 한 명도 맞히지 못했다(전부 정상으로 분류). 이처럼 한 범주가 압도적으로 많은 불균형 데이터에서는 다수 범주만 찍어도 정확도가 높게 나와 모델의 실제 쓸모를 가린다. 환자를 한 명도 못 잡으므로 진단 모델로는 쓸모가 없으며, 정확도 대신 환자를 얼마나 잡았는지(재현율)나 혼동행렬을 함께 봐야 한다."},
        "explain": [proc([
            "정확도 95% = 정상 950명을 다 맞혀서 나온 수치.",
            "환자 50명은 0명 적중(전부 정상으로 분류).",
            "불균형 데이터에서 다수만 찍어도 정확도 높음 -> 정확도가 함정.",
            "'중요한 소수(환자)를 못 잡는다 + 정확도만으론 안 됨'이 핵심.",
        ])],
    },
    {
        "id": "ml-trap-002", "type": "explain",
        "content": [
            {"type": "text", "content": "여름철 어느 도시에서 '아이스크림 판매량'과 '물놀이 사고 건수'를 조사해 선형회귀를 했더니 결정계수 R2가 0.9로 매우 높게 나왔다. 아래는 그 산점도다(색은 그날의 기온)."},
            {"type": "image", "src": "/images/trap-corr.png", "alt": "상관 대 인과 산점도", "width": 90, "align": "center"},
            {"type": "text", "content": "이 결과를 보고 '아이스크림 판매가 물놀이 사고를 일으킨다'고 결론 내리는 것이 왜 잘못인지 서술하시오."},
            {"type": "answer-box", "lines": 7},
        ],
        "answer": {"type": "value", "value": "R2가 높다는 것은 두 값이 함께 늘고 주는 관계(상관관계)가 강하다는 뜻일 뿐, 한쪽이 다른 쪽의 원인이라는 뜻(인과관계)은 아니다. 여기서는 '기온(여름 더위)'이라는 숨은 공통 원인이 있어, 더울수록 아이스크림도 많이 팔리고 물놀이도 늘어 사고도 함께 증가한 것이다. 두 변수는 공통 원인 때문에 같이 움직였을 뿐 서로 원인-결과가 아니므로, R2가 높다고 인과관계로 단정하면 안 된다."},
        "explain": [proc([
            "R2/상관이 높다 = 같이 움직인다(상관)일 뿐, 인과 아님.",
            "숨은 공통 원인: 기온(여름). 더위 -> 아이스크림 판매 + 물놀이/사고 둘 다 증가.",
            "상관관계 != 인과관계 가 핵심.",
            "'숨은 변수(기온) 때문에 함께 움직였다'가 들어가면 정답.",
        ])],
    },
]


def build():
    os.makedirs(IMGDIR, exist_ok=True)
    img_rf_vote()
    img_rf_table()
    img_sel_map()
    img_sigmoid(name='logit-curve.png')
    img_sigmoid(points=[('P1', 0.85), ('P2', 0.45), ('P3', 0.20)], name='logit-points.png')
    img_trap_acc()
    img_trap_corr()
    json.dump(PROBLEMS, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for p in PROBLEMS:
        print("OK", p["id"])
    print("saved:", OUT)


if __name__ == '__main__':
    build()
