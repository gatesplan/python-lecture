# -*- coding: utf-8 -*-
"""
k-NN 서술형 문제 3개 + 산점도 이미지 생성.

1) k=2 동작 서술 (동점 문제)        - 이미지 없음
2) 산점도 + 난독화 knn 코드 -> 분류법 이름 + 적절 k값/이유 서술
3) 두 클러스터 + 새 점 -> k=2 vs k=100 결과/오류 서술
   (새 점은 한 클러스터에 가깝게, 전체는 다른 클래스가 다수 -> k=100 오분류 명확)

거리는 유클리드(제곱)만, 직접 계산은 요구하지 않음(원리/서술 위주).
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
                   'problems-cnsh-26-1-2-08.json')

SK_CODE = '''from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=[[]])
model.fit(X, y)          # X: 점들의 좌표, y: 각 점의 클래스(A 또는 B)
print(model.predict([[4.5, 4.5]]))   # 새 점 [4.5, 4.5] 분류'''


def scatter_q2():
    rng = np.random.RandomState(7)
    A = rng.randn(8, 2) * 0.7 + [2.5, 2.5]
    B = rng.randn(8, 2) * 0.7 + [5.5, 5.5]
    plt.figure(figsize=(5, 4))
    plt.scatter(A[:, 0], A[:, 1], c='tab:orange', marker='o', s=70, edgecolors='k', label='class A')
    plt.scatter(B[:, 0], B[:, 1], c='tab:blue', marker='s', s=70, edgecolors='k', label='class B')
    plt.scatter([4.5], [4.5], c='red', marker='*', s=420, edgecolors='k', label='new point [4.5, 4.5]', zorder=5)
    plt.annotate('?', (4.5, 4.5), textcoords='offset points', xytext=(10, 6), fontsize=14, color='red')
    plt.xlabel('x1'); plt.ylabel('x2'); plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, 'knn-q2.png'), dpi=150)
    plt.close()


def scatter_q3():
    rng = np.random.RandomState(3)
    A = rng.randn(12, 2) * 0.55 + [2.5, 2.5]   # 다수 클래스(12)
    B = rng.randn(8, 2) * 0.55 + [6.0, 6.0]    # 소수 클래스(8)
    newp = [4.7, 4.7]                          # 두 무리 사이(중간영역)이되 B에 더 가까움
    plt.figure(figsize=(5, 4))
    plt.scatter(A[:, 0], A[:, 1], c='tab:orange', marker='o', s=70, edgecolors='k', label='class A (n=12)')
    plt.scatter(B[:, 0], B[:, 1], c='tab:blue', marker='s', s=70, edgecolors='k', label='class B (n=8)')
    plt.scatter([newp[0]], [newp[1]], c='red', marker='*', s=420, edgecolors='k', label='new point (?)', zorder=5)
    plt.annotate('?', (newp[0], newp[1]), textcoords='offset points', xytext=(10, 6), fontsize=14, color='red')
    plt.xlabel('x1'); plt.ylabel('x2'); plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, 'knn-q3.png'), dpi=150)
    plt.close()


def scatter_q4():
    rng = np.random.RandomState(11)
    A = rng.randn(9, 2) * 0.55 + [2.5, 2.5]
    B = rng.randn(8, 2) * 0.55 + [6.0, 6.0]
    outlier = [3.6, 3.6]   # A 무리 쪽에 섞인 B 이상치(노이즈)
    newp = [4.0, 4.0]      # 새 점: 이상치 바로 옆(실제로는 A 영역)
    plt.figure(figsize=(5, 4))
    plt.scatter(A[:, 0], A[:, 1], c='tab:orange', marker='o', s=70, edgecolors='k', label='class A')
    plt.scatter(B[:, 0], B[:, 1], c='tab:blue', marker='s', s=70, edgecolors='k', label='class B')
    plt.scatter([outlier[0]], [outlier[1]], c='tab:blue', marker='s', s=70, edgecolors='k')  # 이상치도 B
    plt.scatter([newp[0]], [newp[1]], c='red', marker='*', s=420, edgecolors='k', label='new point (?)', zorder=5)
    plt.annotate('?', (newp[0], newp[1]), textcoords='offset points', xytext=(10, 6), fontsize=14, color='red')
    plt.xlabel('x1'); plt.ylabel('x2'); plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(IMGDIR, 'knn-q4.png'), dpi=150)
    plt.close()


def ans_box(lines=6):
    return {"type": "answer-box", "lines": lines}


def proc(points):
    return {"type": "process-box", "title": "채점 포인트",
            "content": [{"type": "text", "content": t} for t in points]}


PROBLEMS = [
    {
        "id": "ml-knn-001", "type": "explain",
        "content": [
            {"type": "text", "content": "k-최근접 이웃(k-NN) 분류에서 k=2로 설정했을 때 분류가 어떻게 이루어지는지, 그리고 어떤 문제가 생길 수 있는지 서술하시오."},
            ans_box(5),
        ],
        "answer": {"type": "value", "value": "가장 가까운 2개의 다수결로 분류하지만, 두 이웃의 클래스가 다르면 1:1 동점이 되어 분류를 정할 수 없다(짝수 k의 동점 문제). 그래서 k는 보통 홀수로 둔다."},
        "explain": [proc([
            "새 데이터에서 가장 가까운 이웃 2개를 찾는다.",
            "그 2개의 클래스를 다수결(투표)한다.",
            "두 이웃의 클래스가 서로 다르면 1:1 동점 -> 다수결로 결정 불가.",
            "결론: 짝수 k(특히 2)는 동점이 생길 수 있어, k는 홀수가 바람직하다.",
        ])],
    },
    {
        "id": "ml-knn-002", "type": "explain",
        "content": [
            {"type": "text", "content": "아래 산점도의 데이터(class A, B)를 학습에 사용한다. 다음 코드를 읽고 물음에 답하시오."},
            {"type": "image", "src": "/images/knn-q2.png", "alt": "산점도", "width": 80, "align": "center"},
            {"type": "code", "language": "python", "content": SK_CODE},
            {"type": "text", "content": "(1) 이 코드가 사용하는 분류 알고리즘의 이름을 쓰시오. (2) 빈칸(n_neighbors)에 들어갈 k값을 정하고, 그렇게 정한 이유를 서술하시오."},
            ans_box(6),
        ],
        "answer": {"type": "value", "value": "(1) k-NN(k-최근접 이웃). (2) 예: k=3 또는 5. 짝수는 동점이 생기므로 홀수가 좋고, k=1은 이상치/노이즈에 민감, k가 너무 크면 멀리 있는 점까지 포함되어 클래스 경계가 흐려진다. 데이터가 두 무리로 비교적 잘 나뉘므로 작은 홀수면 충분하다."},
        "explain": [proc([
            "(1) KNeighborsClassifier는 k-NN(k-최근접 이웃) 분류기다.",
            "(2) 핵심 근거 3가지가 들어가면 정답 인정:",
            " - 홀수 권장(짝수는 동점).",
            " - k=1처럼 너무 작으면 노이즈/이상치 하나에 휘둘림.",
            " - k가 너무 크면 먼 점까지 포함 -> 경계가 흐려지고 다수 클래스로 쏠림.",
            "구체적 k 숫자(예: 3, 5)는 위 이유와 함께면 정답.",
        ])],
    },
    {
        "id": "ml-knn-003", "type": "explain",
        "content": [
            {"type": "text", "content": "두 클래스가 무리를 이룬 산점도에 새 점(빨간 별, ?)을 분류하려고 한다. (전체 데이터는 class A 12개 + class B 8개 = 20개)"},
            {"type": "image", "src": "/images/knn-q3.png", "alt": "산점도와 새 점", "width": 80, "align": "center"},
            {"type": "text", "content": "갑은 k=2, 을은 k=100으로 설정했다. 각 설정에서 새 점(?)이 어떤 클래스로 분류될지 예상하고, 둘 중 더 잘못된 설정이 무엇인지 이유와 함께 서술하시오."},
            ans_box(7),
        ],
        "answer": {"type": "value", "value": "k=2: 가장 가까운 2개가 모두 class B이므로 B로 분류된다(동작은 정상이지만, 짝수 k는 동점이 생길 수 있어 일반적으로 권장되지 않는다). k=100: 전체 데이터가 20개뿐이라 이웃을 100개 볼 수 없고, 설령 전체를 본다 해도 다수 클래스 A로만 분류되어 새 점의 위치(B에 가까움)가 무시된다. 따라서 둘 중 더 잘못된 설정은 k=100이다."},
        "explain": [proc([
            "새 점은 class B 무리에 확실히 가깝다.",
            "k=2: 가장 가까운 2개가 모두 B -> B로 분류(위치는 반영). 다만 짝수 k라 동점 위험이 있어 이상적이진 않다.",
            "k=100: 전체가 20개라 이웃 100개는 불가능(데이터 수 초과).",
            "  설령 전체를 이웃으로 보면 다수인 A로만 분류 -> 새 점 위치가 전혀 반영 안 됨.",
            "결론: k=2는 사소한 결함(짝수)일 뿐이지만 k=100은 위치 정보를 통째로 잃는 근본적 오류 -> 더 잘못된 것은 k=100.",
        ])],
    },
    {
        "id": "ml-knn-004", "type": "explain",
        "content": [
            {"type": "text", "content": "아래 산점도에서 class A 무리 쪽에 class B 점 하나가 섞여 있다(노이즈/이상치). 새 점(빨간 별, ?)을 분류하려고 한다."},
            {"type": "image", "src": "/images/knn-q4.png", "alt": "이상치가 섞인 산점도", "width": 80, "align": "center"},
            {"type": "text", "content": "새 점(?)을 k=1과 k=3으로 분류하면 각각 어떤 클래스가 되는지 예상하고, k=1을 쓸 때의 위험을 서술하시오."},
            ans_box(7),
        ],
        "answer": {"type": "value", "value": "k=1: 가장 가까운 1개가 A 무리에 섞인 B 이상치이므로 B로 분류된다(오분류). k=3: 가까운 3개는 B 이상치 1개 + 주변 A 2개라 A로 분류된다(정상). k=1은 가장 가까운 한 점만 보기 때문에 그 점이 노이즈/이상치면 그대로 오분류된다(이상치에 매우 민감, 과적합). k를 키우면 주변 다수로 보정된다."},
        "explain": [proc([
            "새 점은 실제로는 A 무리 영역에 있다.",
            "k=1: 가장 가까운 한 점이 하필 섞여 있던 B 이상치 -> B로 오분류.",
            "k=3: 가까운 3개 = B 이상치 1 + A 2 -> 다수결로 A(정상 분류).",
            "결론: k=1은 가장 가까운 한 점에만 의존해 노이즈/이상치 하나에 휘둘린다(과적합).",
            "k를 적당히 키우면 주변 여러 점의 다수결로 이상치 영향을 줄일 수 있다.",
        ])],
    },
    {
        "id": "ml-knn-005", "type": "explain",
        "content": [
            {"type": "text", "content": "k-최근접 이웃(k-NN) 분류에서 k값을 보통 홀수로 정하는 이유를 서술하시오. (클래스는 2개라고 가정한다.)"},
            ans_box(5),
        ],
        "answer": {"type": "value", "value": "k가 짝수이면 두 클래스의 이웃 수가 같아지는 동점(예: 2:2, 3:3)이 생길 수 있어 어느 쪽으로 분류할지 정할 수 없다. k를 홀수로 하면 두 클래스의 표 합이 홀수라 같아질 수 없으므로 항상 한쪽이 다수가 되어 분류가 결정된다."},
        "explain": [proc([
            "이웃들의 클래스를 다수결로 분류한다.",
            "클래스가 2개일 때 k가 짝수면 표가 반반(예: 2:2)이 되는 동점이 가능하다.",
            "동점이면 다수결로 클래스를 정할 수 없다.",
            "k가 홀수면 두 클래스의 표 합이 홀수라 같아질 수 없으므로 항상 다수가 정해진다.",
        ])],
    },
]


def build():
    os.makedirs(IMGDIR, exist_ok=True)
    scatter_q2()
    scatter_q3()
    scatter_q4()
    json.dump(PROBLEMS, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for p in PROBLEMS:
        print("OK", p["id"])
    print("saved:", OUT)


if __name__ == '__main__':
    build()
