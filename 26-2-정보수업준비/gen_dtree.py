# -*- coding: utf-8 -*-
"""
의사결정트리 문제 생성기 (plot_tree 이미지 + 문제 + 정답 자동).

- 7개 트리: 균형(depth2)과 불균형(depth3) 혼합, 전부 다른 주제.
- leaf 분포를 통제하기 위해 데이터를 수동 구성(combos: 조합별 No/Yes 개수)한다.
  -> 확률이 깔끔하게 떨어지고(75%, 60% 등), 트리 모양도 의도대로 나온다.
- 문제 유형:
    count : 도달 leaf에 모인 No/Yes 학습데이터 개수 (value 용어 없이 풀어 설명)
    vote  : 예측 class
    prob  : Yes(양성)로 분류될 확률(%)
- 정답은 학습 model로 자동 계산, plot_tree 표시값(정수)과 일치.
- feature/class 라벨은 영문(matplotlib 한글 회피), 문제 텍스트에서 한글 매핑.
"""
import os
import re
import json
import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
IMGDIR = os.path.join(HERE, '..', 'exam-builder', 'frontend', 'public', 'images')
OUT = os.path.join(HERE, '..', 'exam-builder', 'frontend', 'src', 'data',
                   'problems-cnsh-26-1-2-07.json')


# feature 영문명 -> 한글 설명 (트리가 실제 쓰는 feature만 문제에 노출)
KR = {
    'income': "income(소득): 0=낮음 1=높음", 'age': "age(나이)", 'student': "student: 0=아니오 1=예",
    'rain': "rain(비): 0=안옴 1=옴", 'temp': "temp(기온)", 'wind': "wind(바람): 0=약함 1=강함",
    'study': "study(공부시간)", 'attend': "attend(출석률)", 'hw': "hw(과제): 0=미제출 1=제출",
    'credit': "credit(신용): 0=나쁨 1=좋음", 'links': "links(링크수)", 'caps': "caps(대문자비율%)",
    'length': "length(글자수)", 'level': "level(레벨)", 'items': "items(아이템): 0=없음 1=있음",
    'allies': "allies(동료): 0=없음 1=있음", 'humid': "humid(습도%)", 'cloud': "cloud(구름량%)",
}


def used_feats(clf):
    return sorted(set(int(f) for f in clf.tree_.feature if f >= 0))


def relabel(anns, classes):
    """plot_tree 노드 텍스트를 학생 친화적으로 교체.
    value 용어 대신 '클래스명: 개수' 분포를 모든 노드에 표기.
    분기 노드 -> 조건 + 분포 / leaf -> 분포."""
    for ann in anns:
        txt = ann.get_text()
        m = re.search(r'value = \[(\d+), (\d+)\]', txt)
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        dist = "%s: %d, %s: %d" % (classes[0], a, classes[1], b)
        if '<=' in txt:
            ann.set_text("%s\n%s" % (txt.split('\n')[0], dist))   # 분기: 조건 + 분포
        else:
            ann.set_text(dist)                                     # leaf: 분포


def make(combos):
    """combos: [(feature_vals_tuple, n_neg, n_pos), ...] -> X, y"""
    X, y = [], []
    for vals, n0, n1 in combos:
        for _ in range(n0):
            X.append(list(vals)); y.append(0)
        for _ in range(n1):
            X.append(list(vals)); y.append(1)
    return np.array(X), np.array(y)


# pid, combos, feats(영문), classes(영문), max_depth, 입력, 유형, 한글설명, 입력설명
TREES = [
    # 균형 d2, 확률 -> 입력 [1,3] => 75%
    ("ml-dt-001",
     [((0, 25, 0), 3, 1), ((0, 45, 0), 4, 0), ((1, 25, 0), 1, 3), ((1, 45, 0), 0, 4)],
     ['income', 'age', 'student'], ['No', 'Yes'], 2, [1, 25, 0], 'prob',
     "income: 0=낮음 1=높음, age: 나이, student: 0=아니오 1=예", "income=1, age=25, student=0"),
    # 불균형 d3 (rain=1이면 안함 pure), 경로개수 -> mixed leaf [3,2]
    ("ml-dt-002",
     [((1, 15, 0), 8, 0), ((0, 15, 0), 5, 0), ((0, 15, 1), 4, 0), ((0, 28, 0), 0, 6), ((0, 28, 1), 3, 2)],
     ['rain', 'temp', 'wind'], ['No', 'Yes'], 3, [0, 28, 1], 'count',
     "rain: 0=안옴 1=옴, temp: 기온, wind: 0=약함 1=강함", "rain=0, temp=28, wind=1"),
    # 균형 d2, 다수결
    ("ml-dt-003",
     [((3, 60, 0), 5, 0), ((3, 90, 0), 3, 2), ((8, 60, 0), 2, 3), ((8, 90, 0), 0, 5)],
     ['study', 'attend', 'hw'], ['Fail', 'Pass'], 2, [8, 90, 0], 'vote',
     "study: 공부시간, attend: 출석률, hw: 과제제출 0/1", "study=8, attend=90, hw=0"),
    # 불균형 d3 (credit=0이면 거절 pure), 경로개수 -> mixed leaf [2,3]
    ("ml-dt-004",
     [((0, 0, 25), 8, 0), ((1, 0, 25), 5, 0), ((1, 0, 45), 4, 0), ((1, 1, 25), 2, 3), ((1, 1, 45), 0, 6)],
     ['credit', 'income', 'age'], ['No', 'Yes'], 3, [1, 1, 25], 'count',
     "credit: 0=나쁨 1=좋음, income: 0=낮음 1=높음, age: 나이", "credit=1, income=1, age=25"),
    # 균형 d2, 확률 -> 입력 [2,3] => 60%
    ("ml-dt-005",
     [((2, 30, 100), 4, 1), ((2, 70, 100), 3, 2), ((7, 30, 100), 2, 3), ((7, 70, 100), 0, 5)],
     ['links', 'caps', 'length'], ['Ham', 'Spam'], 2, [7, 30, 100], 'prob',
     "links: 링크수, caps: 대문자비율, length: 글자수", "links=7, caps=30, length=100"),
    # 불균형 d3 (level>=고이면 승리 pure), 다수결
    ("ml-dt-006",
     [((8, 0, 0), 0, 8), ((3, 0, 0), 5, 0), ((3, 0, 1), 4, 0), ((3, 1, 0), 3, 1), ((3, 1, 1), 0, 5)],
     ['level', 'items', 'allies'], ['Lose', 'Win'], 3, [3, 1, 1], 'vote',
     "level: 레벨, items: 아이템 0/1, allies: 동료 0/1", "level=3, items=1, allies=1"),
    # 균형 d2, 경로개수 -> mixed leaf [3,3]
    ("ml-dt-007",
     [((50, 30, 0), 6, 0), ((50, 80, 0), 4, 2), ((85, 30, 0), 3, 3), ((85, 80, 0), 0, 6)],
     ['humid', 'cloud', 'wind'], ['No', 'Yes'], 2, [85, 30, 0], 'count',
     "humid: 습도, cloud: 구름량, wind: 바람 0/1", "humid=85, cloud=30, wind=0"),
]


def leaf_depths(clf):
    t = clf.tree_
    acc = []
    def rec(node, d):
        if t.children_left[node] == -1:
            acc.append(d)
        else:
            rec(t.children_left[node], d + 1)
            rec(t.children_right[node], d + 1)
    rec(0, 0)
    return sorted(acc)


def int_value(clf, leaf):
    v = clf.tree_.value[leaf].ravel()
    ns = clf.tree_.n_node_samples[leaf]
    return (v * ns).round().astype(int)


def fit(entry):
    pid, combos = entry[0], entry[1]
    X, y = make(combos)
    depth = entry[4]
    return DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X, y)


def inspect():
    for e in TREES:
        clf = fit(e)
        pid, _, feats, classes, depth, inp, qtype, kr, inpdesc = e
        leaf = clf.apply([inp])[0]
        val = int_value(clf, leaf)
        proba = clf.tree_.value[leaf].ravel()
        pred = classes[int(clf.predict([inp])[0])]
        bal = '균형' if len(set(leaf_depths(clf))) == 1 else '불균형'
        uf = [feats[i] for i in used_feats(clf)]
        print("%s [%s/%s] depths=%s used=%s -> leaf=[%d,%d] pred=%s p(pos)=%.2f"
              % (pid, qtype, bal, leaf_depths(clf), uf, val[0], val[1], pred, proba[1]))


def build():
    os.makedirs(IMGDIR, exist_ok=True)
    out = []
    for i, e in enumerate(TREES, 1):
        clf = fit(e)
        pid, _, feats, classes, depth, inp, qtype, _kr, _id = e
        used = used_feats(clf)
        kr = ", ".join(KR[feats[i]] for i in used)
        inpdesc = ", ".join("%s=%s" % (feats[i], inp[i]) for i in used)
        plt.figure(figsize=(7, 4) if depth == 3 else (6, 3.5))
        anns = plot_tree(clf, feature_names=feats, class_names=classes,
                         filled=True, impurity=False, fontsize=10, rounded=True)
        relabel(anns, classes)
        plt.tight_layout()
        img = "dt-%d.png" % i
        plt.savefig(os.path.join(IMGDIR, img), dpi=200)
        plt.close()

        leaf = clf.apply([inp])[0]
        val = int_value(clf, leaf)
        proba = clf.tree_.value[leaf].ravel()
        pred = classes[int(clf.predict([inp])[0])]
        neg, pos = classes[0], classes[1]

        if qtype == 'count':
            q = ("입력 %s 가 도달하는 칸(leaf)에 적힌 %s 개수와 %s 개수를 [%s, %s] 순서로 쓰시오."
                 % (inpdesc, neg, pos, neg, pos))
            ans = "[%d, %d]" % (val[0], val[1])
            ex = ["입력 %s 를 트리 맨 위에서부터 분기 조건(예/아니오)에 따라 내려간다." % inpdesc,
                  "도달한 칸: %s %d, %s %d." % (neg, val[0], pos, val[1]),
                  "정답: " + ans]
        elif qtype == 'vote':
            q = "입력 %s 의 예측 결과(class)를 쓰시오." % inpdesc
            ans = pred
            ex = ["입력 %s 가 도달한 leaf: %s %d개, %s %d개." % (inpdesc, neg, val[0], pos, val[1]),
                  "더 많은 쪽으로 분류 -> %s." % pred,
                  "정답: " + ans]
        else:  # prob
            pct = round(proba[1] * 100)
            ans = "%d%%" % pct
            q = ("입력 %s 가 '%s'로 분류될 확률을 백분율로 쓰시오. "
                 "(확률 = 도달한 칸의 %s 개수 / 전체 개수)" % (inpdesc, pos, pos))
            ex = ["입력 %s 가 도달한 leaf: %s %d개, %s %d개 (합 %d)." % (inpdesc, neg, val[0], pos, val[1], val[0] + val[1]),
                  "%s 확률 = %d / %d = %s." % (pos, val[1], val[0] + val[1], ans),
                  "정답: " + ans]

        out.append({
            "id": pid, "type": "short",
            "content": [
                {"type": "text", "content": "다음 의사결정트리를 보고 물음에 답하시오. (%s)" % kr},
                {"type": "image", "src": "/images/%s" % img, "alt": "의사결정트리", "width": 90, "align": "center"},
                {"type": "text", "content": q},
            ],
            "answer": {"type": "value", "value": ans},
            "explain": [{"type": "process-box", "title": "풀이",
                         "content": [{"type": "text", "content": t} for t in ex]}],
        })
        print("OK %s [%s] -> %s" % (pid, qtype, ans))
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print("saved:", OUT)


if __name__ == '__main__':
    import sys
    if '--save' in sys.argv:
        build()
    else:
        inspect()
