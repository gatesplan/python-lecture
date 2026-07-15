# -*- coding: utf-8 -*-
"""
ML meta(개념) 문제 6개.

ml-meta-001 : 배운 5개 알고리즘 -> 지도/비지도 + 회귀/분류/군집 분류
ml-meta-002 : k-NN vs k-Means 차이 (지도/비지도, 하는 일, k의 의미)
ml-meta-003 : 전처리 코드(fillna/dropna/이상치) -> 무엇을·왜
ml-meta-004 : train/test 분리 이유
ml-meta-005 : 혼동행렬 해석 (암 진단, 위음성의 위험)  [이미지]
ml-meta-006 : AI 전체 흐름 서술 (데이터 로드->전처리->학습->평가)

R2(회귀 평가)는 선형회귀 문제에서 다루므로 meta에서는 분류 평가(혼동행렬)만.
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
                   'problems-cnsh-26-1-2-11.json')

PREP_CODE = '''import pandas as pd

df = pd.read_csv('students.csv')
df['math'] = df['math'].fillna(df['math'].mean())
df = df.dropna()
df = df[df['score'] <= 100]'''

ALGOS = ["선형회귀", "로지스틱회귀", "k-NN(최근접 이웃)", "의사결정트리", "k-Means"]

# 혼동행렬: [[TN, FP], [FN, TP]]  (Neg=암 아님, Pos=암)
CM = np.array([[80, 12], [13, 15]])


def cm_image():
    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    ax.imshow(CM, cmap='Blues')
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(CM[i, j]), ha='center', va='center',
                    fontsize=18, color='white' if CM[i, j] > 50 else 'black')
    ax.set_xticks([0, 1]); ax.set_xticklabels(['Pred: Neg', 'Pred: Pos'])
    ax.set_yticks([0, 1]); ax.set_yticklabels(['Actual: Neg', 'Actual: Pos'])
    ax.set_xlabel('predicted'); ax.set_ylabel('actual')
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, 'meta-cm.png'), dpi=150)
    plt.close()


def proc(points):
    return {"type": "process-box", "title": "채점 포인트",
            "content": [{"type": "text", "content": t} for t in points]}


PROBLEMS = [
    {
        "id": "ml-meta-001", "type": "explain",
        "content": [
            {"type": "text", "content": "다음 다섯 알고리즘을 각각 (가) 지도학습/비지도학습, (나) 회귀/분류/군집 중 무엇에 해당하는지 분류하시오."},
            {"type": "condition-box", "title": "알고리즘", "marker": "kr-con", "items": list(ALGOS)},
            {"type": "answer-box", "lines": 6},
        ],
        "answer": {"type": "value", "value": "선형회귀: 지도학습·회귀 / 로지스틱회귀: 지도학습·분류 / k-NN: 지도학습·분류 / 의사결정트리: 지도학습·분류 / k-Means: 비지도학습·군집"},
        "explain": [proc([
            "지도/비지도: 정답(레이블)을 쓰면 지도, 안 쓰면 비지도.",
            "회귀=숫자 예측, 분류=범주 예측, 군집=정답 없이 그룹화.",
            "ㄱ 선형회귀: 지도·회귀.   ㄴ 로지스틱회귀: 지도·분류(이름은 회귀지만 분류).",
            "ㄷ k-NN: 지도·분류.   ㄹ 의사결정트리: 지도·분류.   ㅁ k-Means: 비지도·군집.",
        ])],
    },
    {
        "id": "ml-meta-002", "type": "explain",
        "content": [
            {"type": "text", "content": "k-NN과 k-Means는 둘 다 이름에 'k'가 있지만 서로 다른 알고리즘이다. 두 알고리즘이 (지도/비지도), (하는 일), (k의 의미) 측면에서 어떻게 다른지 서술하시오."},
            {"type": "answer-box", "lines": 7},
        ],
        "answer": {"type": "value", "value": "k-NN은 지도학습 분류 알고리즘으로, 정답이 있는 데이터를 이용해 새 데이터를 가장 가까운 이웃들의 다수결로 분류한다. 여기서 k는 '참고할 이웃의 수'다. k-Means는 비지도학습 군집 알고리즘으로, 정답 없이 비슷한 데이터끼리 묶는다. 여기서 k는 '나눌 군집(중심점)의 개수'다."},
        "explain": [proc([
            "지도/비지도: k-NN은 지도(정답 사용), k-Means는 비지도(정답 없음).",
            "하는 일: k-NN은 분류, k-Means는 군집.",
            "k의 의미: k-NN은 이웃 수, k-Means는 군집 수.",
            "세 측면이 모두 들어가면 정답.",
        ])],
    },
    {
        "id": "ml-meta-003", "type": "explain",
        "content": [
            {"type": "text", "content": "다음은 데이터를 학습에 쓰기 전에 정리하는 코드이다."},
            {"type": "code", "language": "python", "content": PREP_CODE},
            {"type": "text", "content": "2~4번째 줄은 각각 어떤 처리를 하며, 왜 그 처리가 필요한지 서술하시오."},
            {"type": "answer-box", "lines": 7},
        ],
        "answer": {"type": "value", "value": "fillna(df['math'].mean()): math 열의 빈 값(결측치)을 그 열의 평균으로 채운다 - 빈 값이 있으면 학습이 안 되므로. dropna(): 아직 남아 있는 결측치가 있는 행을 제거한다 - 불완전한 데이터를 빼기 위해. df[df['score'] <= 100]: 점수가 100을 넘는 비정상 값(이상치)을 걸러낸다 - 잘못된 데이터가 결과를 왜곡하지 않도록. 즉 결측치와 이상치를 정리해 모델이 올바른 데이터로 학습하게 한다."},
        "explain": [proc([
            "2줄 fillna(mean): 결측치를 평균으로 대체.",
            "3줄 dropna: 남은 결측치 행 제거.",
            "4줄 조건 필터: score>100 같은 이상치 제거.",
            "공통 이유: 결측치/이상치가 있으면 학습이 안 되거나 결과가 왜곡됨.",
        ])],
    },
    {
        "id": "ml-meta-004", "type": "explain",
        "content": [
            {"type": "text", "content": "지도학습 모델을 만들 때 보통 데이터를 train(학습용)과 test(평가용)로 나눈다. 데이터를 이렇게 나누는 이유를 서술하시오."},
            {"type": "answer-box", "lines": 5},
        ],
        "answer": {"type": "value", "value": "학습에 사용하지 않은 새 데이터(test)로 평가해야, 모델이 처음 보는 데이터에도 잘 작동하는지(일반화) 확인할 수 있다. 학습에 쓴 데이터로만 평가하면 모델이 그 데이터를 외운 것일 수 있어 실제 성능을 제대로 알 수 없다."},
        "explain": [proc([
            "test는 학습에 안 쓴 데이터 -> 새 데이터에 대한 성능(일반화) 측정.",
            "train으로만 평가하면 외워서 잘 맞는 것과 구분이 안 됨.",
            "'일반화 확인'(또는 새 데이터 성능)이 들어가면 정답.",
        ])],
    },
    {
        "id": "ml-meta-005", "type": "explain",
        "content": [
            {"type": "text", "content": "다음은 어떤 암 진단 모델의 혼동행렬이다. (Neg=암 아님, Pos=암. 행=실제, 열=예측)"},
            {"type": "image", "src": "/images/meta-cm.png", "alt": "혼동행렬", "width": 75, "align": "center"},
            {"type": "text", "content": "이 모델을 실제 암 진단에 사용할 때 어떤 문제가 있는지, 혼동행렬의 수치를 근거로 서술하시오."},
            {"type": "answer-box", "lines": 7},
        ],
        "answer": {"type": "value", "value": "실제 암 환자(Pos) 28명 중 13명을 음성(Neg)으로 잘못 판정했다(위음성). 암 진단에서 위음성은 암 환자를 놓쳐 치료 시기를 놓치게 하는 치명적 오류다. 전체 정확도는 (80+15)/120 ≈ 79%로 나쁘지 않아 보이지만, 정작 암 환자의 약 46%(13/28)를 놓치므로 진단 모델로는 위험하다. 위음성을 줄이는 방향으로 개선해야 한다."},
        "explain": [proc([
            "혼동행렬 읽기: 실제 Pos(암) = 13(위음성) + 15(맞춤) = 28명.",
            "위음성(FN)=13: 실제 암인데 음성으로 판정 -> 환자를 놓침.",
            "암 진단에서는 위음성이 위양성보다 훨씬 위험하다(치료 시기 놓침).",
            "정확도(약 79%)만 보면 괜찮아 보여도 암 환자를 절반 가까이 놓침 -> 부적합.",
            "핵심: '위음성이 많아 암 환자를 놓친다'가 들어가면 정답.",
        ])],
    },
    {
        "id": "ml-meta-006", "type": "explain",
        "content": [
            {"type": "text", "content": "머신러닝으로 문제를 해결하는 전체 과정을, 데이터를 준비하는 단계부터 모델 성능을 확인하는 단계까지 순서대로 서술하시오."},
            {"type": "answer-box", "lines": 7},
        ],
        "answer": {"type": "value", "value": "1) 데이터 로드: csv 등에서 데이터를 불러온다. 2) 전처리: 결측치·이상치를 정리하는 등 데이터를 학습에 맞게 다듬는다. 3) 데이터 분리: train(학습용)과 test(평가용)로 나눈다. 4) 학습(fit): train 데이터로 모델을 학습시킨다. 5) 예측/평가: test 데이터로 예측하고 R2(회귀)·정확도(분류) 등으로 성능을 평가한다."},
        "explain": [proc([
            "데이터 로드 -> 전처리 -> (train/test 분리) -> 학습(fit) -> 예측/평가 순서.",
            "전처리(결측치·이상치 정리)와 학습/평가 단계가 들어가야 함.",
            "순서가 맞고 각 단계가 무엇을 하는지 설명되면 정답.",
        ])],
    },
    {
        "id": "ml-meta-007", "type": "explain",
        "content": [
            {"type": "text", "content": "R2(결정계수)는 회귀 모델의 성능을 나타내는 지표다. R2가 무엇을 의미하는지, 그리고 값이 1에 가까울 때와 0에 가까울 때가 각각 어떤 상태인지 서술하시오."},
            {"type": "answer-box", "lines": 5},
        ],
        "answer": {"type": "value", "value": "R2(결정계수)는 회귀 모델이 데이터의 경향을 얼마나 잘 설명(예측)하는지를 보통 0~1 사이로 나타낸 값이다. 1에 가까울수록 점들이 회귀직선에 가깝게 모여 예측이 잘 맞고, 0에 가까울수록 직선이 데이터를 잘 설명하지 못해 예측이 부정확하다."},
        "explain": [proc([
            "R2는 회귀의 예측 성능(직선이 데이터를 얼마나 설명하는지)을 나타낸다.",
            "보통 0~1 범위, 1에 가까울수록 좋음(직선에 잘 맞음).",
            "0에 가까우면 직선이 데이터를 설명하지 못함(성능 나쁨).",
        ])],
    },
    {
        "id": "ml-meta-008", "type": "explain",
        "content": [
            {"type": "text", "content": "로지스틱회귀는 이름에 '회귀'가 들어가 있어 회귀(숫자 예측)로 오해하기 쉽지만, 실제로는 분류 알고리즘이다. 로지스틱회귀가 회귀가 아니라 분류인 이유를 서술하시오."},
            {"type": "answer-box", "lines": 5},
        ],
        "answer": {"type": "value", "value": "로지스틱회귀는 연속적인 숫자를 예측하는 것이 아니라, 데이터가 어느 범주(예: 합격/불합격, 양성/음성)에 속하는지를 구분한다. 로지스틱 함수로 0~1 사이 값(확률)을 구한 뒤 기준(보통 0.5)으로 범주를 나누므로 결과가 범주다. 따라서 이름과 달리 분류 알고리즘이다."},
        "explain": [proc([
            "회귀=숫자 예측, 분류=범주 예측.",
            "로지스틱회귀의 결과는 숫자가 아니라 범주(예: 0/1, 합격/불합격).",
            "로지스틱 함수로 확률(0~1)을 구하고 기준으로 나눠 범주를 정함 -> 분류.",
            "'이름은 회귀지만 출력이 범주라 분류'가 핵심.",
        ])],
    },
]


def build():
    os.makedirs(IMGDIR, exist_ok=True)
    cm_image()
    json.dump(PROBLEMS, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for p in PROBLEMS:
        print("OK", p["id"])
    print("saved:", OUT)


if __name__ == '__main__':
    build()
