# -*- coding: utf-8 -*-
"""
오늘 만든 문제들을 주제가 고루 퍼지도록 시험지 세트로 조합.
- 전체 문제가 최소 1회 등장(중복 허용).
- 토픽별 오프셋 회전 배분으로 각 세트에 여러 주제가 섞이게 함.
"""
from collections import Counter

BASE = "http://localhost:5173/preview?ids="

TOPICS = [
    ("암호-단독/추적", ['g1-%03d' % n for n in [61, 62, 63, 64, 65, 66, 79, 81, 82]]),
    ("암호-조합",      ['g1-%03d' % n for n in list(range(67, 79)) + [80] + list(range(83, 93))]),
    ("클래스",         ['g1-%03d' % n for n in range(93, 107)]),
    ("의사결정트리",   ['ml-dt-%03d' % n for n in range(1, 8)]),
    ("k-NN",          ['ml-knn-%03d' % n for n in range(1, 6)]),
    ("k-Means",       ['ml-km-%03d' % n for n in range(1, 4)]),
    ("선형회귀",       ['ml-lr-%03d' % n for n in range(1, 4)]),
    ("meta",          ['ml-meta-%03d' % n for n in range(1, 9)]),
]

NSET = 7
sets = [[] for _ in range(NSET)]
off = 0
for label, ids in TOPICS:
    for i, pid in enumerate(ids):
        sets[(i + off) % NSET].append((label, pid))
    off += len(ids)

# 세트 4+5, 6+7 병합 -> 5세트
sets = [sets[0], sets[1], sets[2], sets[3] + sets[4], sets[5] + sets[6]]

total = sum(len(ids) for _, ids in TOPICS)
print("전체 고유 문제: %d개 / %d세트\n" % (total, len(sets)))

for k, s in enumerate(sets, 1):
    ids = [p for _, p in s]
    tc = Counter(l for l, _ in s)
    topic_str = ", ".join("%s %d" % (lbl, c) for lbl, c in tc.items())
    print("=== 세트 %d  (%d문제) ===" % (k, len(s)))
    print("  주제: " + topic_str)
    print("  " + BASE + ",".join(ids))
    print()

all_ids = [p for s in sets for _, p in s]
print("총 슬롯 %d, 고유 %d (전체 커버: %s)"
      % (len(all_ids), len(set(all_ids)), "OK" if len(set(all_ids)) == total else "누락!"))
