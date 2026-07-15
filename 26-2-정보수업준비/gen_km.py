# -*- coding: utf-8 -*-
"""
k-Means 문제 3개 + 산점도 이미지 생성.

ml-km-001 : k=2 동작 단계 서술
ml-km-002 : O/X 8개 (개념 종합 - 초기 랜덤성/수렴/k 과대 포함)
ml-km-003 : 산점도(군집 3개) + sklearn 코드 -> (1)지도/비지도 (2)적절 k (3)k=100 과대

원리/개념 위주(거리 직접계산 없음), 코드는 sklearn 기반.
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
                   'problems-cnsh-26-1-2-09.json')

KM_CODE = '''from sklearn.cluster import KMeans

model = KMeans(n_clusters=[[]])
labels = model.fit_predict(X)   # X: 점들의 좌표 (정답 y 없음)
print(labels)'''

OX_ITEMS = [
    "k-Means는 정답(레이블) 없이 데이터를 묶는 비지도학습이다.",                       # O
    "k는 나눌 군집의 개수이고, 초기 중심점도 k개를 정한다.",                          # O
    "같은 데이터, 같은 k값으로 학습하면 결과가 동일하다.",                            # X
    "결과를 고정하려면 random_state(시드)를 지정한다.",                              # O
    "각 점은 가장 가까운 중심점에 배정되고, 중심점은 배정된 점들의 평균으로 이동한다.",  # O
    "반복하면 서로 다른 두 중심점도 결국 같은 위치로 합쳐진다.",                       # X
    "군집 개수 k는 데이터 개수보다 많아도 된다.",                                    # X
    "결과는 각 점의 군집 번호이며, 번호 자체에 크기/순서 의미는 없다.",               # O
]
OX_ANS = ["O", "O", "X", "O", "O", "X", "X", "O"]
OX_MARK = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ"]


def scatter_km3():
    rng = np.random.RandomState(5)
    c1 = rng.randn(8, 2) * 0.5 + [2.0, 2.0]
    c2 = rng.randn(8, 2) * 0.5 + [6.5, 2.5]
    c3 = rng.randn(8, 2) * 0.5 + [4.0, 6.5]
    pts = np.vstack([c1, c2, c3])
    plt.figure(figsize=(5, 4))
    plt.scatter(pts[:, 0], pts[:, 1], c='gray', marker='o', s=70, edgecolors='k')
    plt.xlabel('x1'); plt.ylabel('x2')
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, 'km-3.png'), dpi=150)
    plt.close()
    return len(pts)


def proc(points):
    return {"type": "process-box", "title": "채점 포인트",
            "content": [{"type": "text", "content": t} for t in points]}


def build():
    os.makedirs(IMGDIR, exist_ok=True)
    n = scatter_km3()

    ox_answer = ", ".join("%s:%s" % (m, a) for m, a in zip(OX_MARK, OX_ANS))

    problems = [
        {
            "id": "ml-km-001", "type": "explain",
            "content": [
                {"type": "text", "content": "k-Means 군집화에서 k=2로 설정했을 때 알고리즘이 어떻게 동작하는지 단계적으로 서술하시오."},
                {"type": "answer-box", "lines": 6},
            ],
            "answer": {"type": "value", "value": "1) 중심점 2개를 무작위 위치에 정한다(초기화). 2) 각 점을 더 가까운 중심점에 배정해 2개 그룹을 만든다. 3) 각 그룹에 속한 점들의 평균 위치로 중심점을 옮긴다(재설정). 4) 배정과 이동을 더 이상 변화가 없을 때까지 반복하고 멈춘다. 결과로 데이터가 2개 군집으로 나뉜다."},
            "explain": [proc([
                "초기화: 중심점(centroid)을 k=2개, 보통 무작위 위치에 둔다.",
                "배정: 각 점을 더 가까운 중심점 쪽으로 보내 2개 그룹을 만든다.",
                "재설정: 각 그룹 점들의 평균으로 중심점을 이동한다.",
                "반복/종료: 배정->이동을 변화가 없을 때까지 반복한다.",
                "4단계(초기화/배정/재설정/반복종료)가 들어가면 정답.",
            ])],
        },
        {
            "id": "ml-km-002", "type": "short",
            "content": [
                {"type": "text", "content": "다음 k-Means에 대한 설명을 읽고, 옳으면 O, 틀리면 X로 판정하시오."},
                {"type": "condition-box", "title": "보기", "marker": "kr-con", "items": list(OX_ITEMS)},
                {"type": "answer-box", "lines": 4},
            ],
            "answer": {"type": "value", "value": ox_answer},
            "explain": [proc([
                "ㄱ O: 정답 레이블 없이 묶으므로 비지도학습.",
                "ㄴ O: k = 군집 수 = 초기 중심점 개수.",
                "ㄷ X: 초기 중심점이 무작위라, 시드를 고정하지 않으면 결과가 달라질 수 있다.",
                "ㄹ O: random_state로 무작위 초기화를 고정하면 결과가 재현된다.",
                "ㅁ O: 배정(가까운 중심) + 재설정(평균 이동)이 k-Means의 핵심 반복.",
                "ㅂ X: 서로 다른 중심점은 각자 영역 점들의 평균으로 갱신되어 다른 위치를 유지한다(같은 점으로 합쳐지지 않음).",
                "ㅅ X: 군집은 데이터 개수보다 많을 수 없다(점 없는 빈 군집 발생, 에러).",
                "ㅇ O: 군집 번호는 단순 식별자라 크기/순서 의미가 없다.",
                "정답: " + ox_answer,
            ])],
        },
        {
            "id": "ml-km-003", "type": "explain",
            "content": [
                {"type": "text", "content": "다음 산점도의 점들(좌표 데이터)을 아래 코드로 처리한다. 코드를 읽고 물음에 답하시오."},
                {"type": "image", "src": "/images/km-3.png", "alt": "산점도", "width": 80, "align": "center"},
                {"type": "code", "language": "python", "content": KM_CODE},
                {"type": "text", "content": "(1) 이 코드는 지도학습과 비지도학습 중 무엇인가? (2) 빈칸(n_clusters)에 들어갈 k값을 정하고 그 이유를 쓰시오. (3) 만약 k=100으로 설정하면 어떤 문제가 생기는지 서술하시오."},
                {"type": "answer-box", "lines": 7},
            ],
            "answer": {"type": "value", "value": "(1) 비지도학습 (정답 y 없이 X만 사용하고 fit_predict로 군집을 찾음). (2) k=3 (점들이 세 무리로 뚜렷이 뭉쳐 있으므로). (3) 전체 데이터가 %d개뿐이라 군집을 100개 만들 수 없다. 점이 하나도 없는 빈 군집이 생겨 에러가 나거나, 사실상 점마다 따로 나뉘어 군집화가 무의미해진다." % n},
            "explain": [proc([
                "(1) X(좌표)만 있고 정답 y가 없으며 fit_predict로 묶음 -> 비지도학습.",
                "(2) 산점도에 점 무리가 3개 -> k=3.",
                "(3) 전체 점이 %d개인데 k=100이면 데이터 수보다 군집이 많다." % n,
                "    -> 빈 군집 발생(에러) / 군집화가 의미를 잃음.",
            ])],
        },
    ]

    json.dump(problems, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for p in problems:
        print("OK", p["id"])
    print("data points:", n, "| saved:", OUT)


if __name__ == '__main__':
    build()
