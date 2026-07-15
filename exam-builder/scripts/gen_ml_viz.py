# -*- coding: utf-8 -*-
"""ML 시각화 서술형 문제용 이미지 생성. 기존 public/images 스타일 재현(영문 라벨)."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import numpy as np
from matplotlib.patches import FancyBboxPatch

OUT = r'C:\Projects\python-lecture\exam-builder\frontend\public\images'
ORANGE = '#ff7f0e'
BLUE = '#1f77b4'
GREEN = '#2ca02c'
POINT = '#3a78c0'
plt.rcParams['axes.unicode_minus'] = False


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=110, bbox_inches='tight')
    plt.close(fig)


def blob(cx, cy, n, s=0.45, seed=0):
    rng = np.random.RandomState(seed)
    return np.c_[rng.normal(cx, s, n), rng.normal(cy, s, n)]


# ===================== KNN scatter =====================
def knn_scatter(ax, A, B, new=None, C=None, xlabel='x1', ylabel='x2', legend=True, na=None, nb=None, nc=None):
    A = np.array(A); B = np.array(B)
    la = 'class A' + (' (n=%d)' % na if na else '')
    lb = 'class B' + (' (n=%d)' % nb if nb else '')
    ax.scatter(A[:, 0], A[:, 1], c=ORANGE, marker='o', s=90, edgecolors='black', label=la, zorder=3)
    ax.scatter(B[:, 0], B[:, 1], c=BLUE, marker='s', s=90, edgecolors='black', label=lb, zorder=3)
    if C is not None:
        C = np.array(C)
        lc = 'class C' + (' (n=%d)' % nc if nc else '')
        ax.scatter(C[:, 0], C[:, 1], c=GREEN, marker='^', s=110, edgecolors='black', label=lc, zorder=3)
    if new is not None:
        ax.scatter([new[0]], [new[1]], c='red', marker='*', s=430, edgecolors='black', label='new point (?)', zorder=4)
        ax.annotate('?', (new[0], new[1]), textcoords='offset points', xytext=(12, 8),
                    color='red', fontsize=15, fontweight='bold')
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    if legend:
        ax.legend(loc='upper left', fontsize=9)


# N1: 경계에 놓인 새 점
fig, ax = plt.subplots(figsize=(6.2, 4.6))
A = blob(2.6, 2.6, 9, 0.4, 1); B = blob(6.4, 6.4, 9, 0.4, 2)
knn_scatter(ax, A, B, new=[4.5, 4.5])
save(fig, 'knn-n1')

# N2: 축 스케일 차이 (x는 0~1000, y는 0~10)
fig, ax = plt.subplots(figsize=(6.4, 4.6))
rng = np.random.RandomState(3)
A = np.c_[rng.normal(250, 80, 9), rng.normal(7.5, 1.0, 9)]
B = np.c_[rng.normal(750, 80, 9), rng.normal(3.0, 1.0, 9)]
knn_scatter(ax, A, B, new=[500, 5.2], xlabel='annual_income (0~1000)', ylabel='rating (0~10)')
ax.set_xlim(0, 1000); ax.set_ylim(0, 10)
save(fig, 'knn-n2')

# N3: 불균형 (A 다수, B 소수), 새 점은 B 쪽
fig, ax = plt.subplots(figsize=(6.2, 4.6))
A = blob(4.2, 4.2, 16, 1.1, 4); B = blob(7.2, 6.8, 5, 0.4, 5)
knn_scatter(ax, A, B, new=[6.8, 6.2], na=16, nb=5)
save(fig, 'knn-n3')

# N4: 동점 - 새 점 주변 정확히 A 2개, B 2개 인접
fig, ax = plt.subplots(figsize=(6.2, 4.6))
A_far = blob(2.3, 2.3, 6, 0.4, 6); B_far = blob(7.6, 7.6, 6, 0.4, 7)
A_near = np.array([[4.5, 5.5], [5.5, 4.5]])
B_near = np.array([[4.5, 4.5], [5.5, 5.5]])
A = np.vstack([A_far, A_near]); B = np.vstack([B_far, B_near])
knn_scatter(ax, A, B, new=[5.0, 5.0])
ax.set_title('4 nearest neighbors: 2 class A + 2 class B (tie at k=4)', fontsize=10)
save(fig, 'knn-n4')

# N5: 3 클래스
fig, ax = plt.subplots(figsize=(6.2, 4.6))
A = blob(2.5, 6.5, 8, 0.45, 8); B = blob(6.8, 6.2, 8, 0.45, 9); C = blob(4.5, 2.5, 8, 0.45, 10)
knn_scatter(ax, A, B, new=[6.2, 5.4], C=C)
save(fig, 'knn-n5')

# N6: 정확히 두 무리 중앙(대칭)
fig, ax = plt.subplots(figsize=(6.2, 4.6))
A = blob(2.5, 4.5, 9, 0.4, 11); B = blob(7.5, 4.5, 9, 0.4, 12)
knn_scatter(ax, A, B, new=[5.0, 4.5])
ax.set_title('new point is exactly midway between two clusters', fontsize=10)
save(fig, 'knn-n6')


# ===================== KMeans scatter =====================
def km_scatter(ax, pts, centers=None, labels=None, title=None):
    pts = np.array(pts)
    if labels is None:
        ax.scatter(pts[:, 0], pts[:, 1], c='gray', s=70, edgecolors='black', zorder=3)
    else:
        cmap = [ORANGE, BLUE, GREEN]
        labels = np.array(labels)
        for k in sorted(set(labels)):
            m = labels == k
            ax.scatter(pts[m, 0], pts[m, 1], c=cmap[k % 3], s=70, edgecolors='black', zorder=3)
    if centers is not None:
        centers = np.array(centers)
        ax.scatter(centers[:, 0], centers[:, 1], c='red', marker='X', s=240,
                   edgecolors='black', linewidths=1.5, zorder=4, label='center')
        ax.legend(loc='upper left', fontsize=9)
    ax.set_xlabel('x1'); ax.set_ylabel('x2')
    if title:
        ax.set_title(title, fontsize=10)


three = np.vstack([blob(2.5, 2.5, 8, 0.4, 21), blob(7, 2.5, 8, 0.4, 22), blob(4.7, 7, 8, 0.4, 23)])

# N1: 같은 데이터, 초기 중심 위치 다른 두 경우
fig, axes = plt.subplots(1, 2, figsize=(10, 4.3))
km_scatter(axes[0], three, centers=[[2.5, 2.5], [7, 2.5]], title='start A: initial centers')
km_scatter(axes[1], three, centers=[[4.5, 4], [5, 5]], title='start B: initial centers')
save(fig, 'km-n1')

# N2: 점이 3무리로 뚜렷
fig, ax = plt.subplots(figsize=(6.2, 4.6))
km_scatter(ax, three, title='how many clusters (k)?')
save(fig, 'km-n2')

# N3: 3무리인데 k=2로 묶임 (두 무리가 한 색)
fig, ax = plt.subplots(figsize=(6.2, 4.6))
labels = [0] * 8 + [0] * 8 + [1] * 8  # 아래 두 무리가 같은 군집(0), 위 무리만 1
km_scatter(ax, three, labels=labels, centers=[[4.75, 2.5], [4.7, 7]], title='k=2 result on 3 clusters')
save(fig, 'km-n3')

# N4: 계산용 정수 격자 점 + 중심 2개
fig, ax = plt.subplots(figsize=(6.0, 5.0))
pts = np.array([[1, 1], [1, 2], [2, 1], [6, 6], [7, 6], [6, 7], [7, 7]])
ax.scatter(pts[:, 0], pts[:, 1], c='gray', s=110, edgecolors='black', zorder=3)
for (x, y) in pts:
    ax.annotate('(%d,%d)' % (x, y), (x, y), textcoords='offset points', xytext=(8, 6), fontsize=9)
c = np.array([[2, 2], [5, 5]])
ax.scatter(c[:, 0], c[:, 1], c='red', marker='X', s=260, edgecolors='black', linewidths=1.5, zorder=4)
ax.annotate('center1 (2,2)', (2, 2), textcoords='offset points', xytext=(8, -16), color='red', fontsize=9)
ax.annotate('center2 (5,5)', (5, 5), textcoords='offset points', xytext=(8, -16), color='red', fontsize=9)
ax.set_xlim(0, 8.5); ax.set_ylim(0, 8.5); ax.set_xlabel('x1'); ax.set_ylabel('x2')
ax.grid(alpha=0.3)
save(fig, 'km-n4')

# N5: 비지도(색 없음) vs 지도(색 있음)
fig, axes = plt.subplots(1, 2, figsize=(10, 4.3))
km_scatter(axes[0], three, title='unlabeled data (no answer y)')
km_scatter(axes[1], three, labels=[0] * 8 + [1] * 8 + [2] * 8, title='labeled data (answer y given)')
save(fig, 'km-n5')

# N6: k-Means가 약한 분포 (길쭉한 평행 띠)
fig, ax = plt.subplots(figsize=(6.2, 4.6))
rng = np.random.RandomState(24)
band1 = np.c_[rng.uniform(1, 9, 25), rng.normal(5.8, 0.25, 25)]
band2 = np.c_[rng.uniform(1, 9, 25), rng.normal(4.2, 0.25, 25)]
both = np.vstack([band1, band2])
km_scatter(ax, both, title='two long horizontal bands')
save(fig, 'km-n6')


# ===================== Decision tree =====================
def tnode(ax, x, y, lines, fc='white', w=2.3, h=0.95):
    box = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                         boxstyle='round,pad=0.08,rounding_size=0.18',
                         linewidth=1.5, edgecolor='black', facecolor=fc, zorder=2)
    ax.add_patch(box)
    ax.text(x, y, '\n'.join(lines), ha='center', va='center', fontsize=10.5, zorder=3)


def tedge(ax, x1, y1, x2, y2, label=None):
    ax.annotate('', xy=(x2, y2 + 0.5), xytext=(x1, y1 - 0.5),
                arrowprops=dict(arrowstyle='->', lw=1.4))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, label, fontsize=10.5, ha='center', va='center',
                bbox=dict(boxstyle='round', fc='white', ec='none'))


def leafcolor(neg, pos):
    t = neg + pos
    if t == 0:
        return 'white'
    r = pos / t
    if r == 0.5:
        return 'white'
    if r < 0.5:
        k = (0.5 - r) * 2
        return mc.to_hex((1, 1 - 0.45 * k, 1 - 0.85 * k))
    k = (r - 0.5) * 2
    return mc.to_hex((1 - 0.78 * k, 1 - 0.45 * k, 1))


def setup_tree(ax, xlim=(0, 10), ylim=(0, 6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis('off')


# N1: 2단계 완전 트리 (스팸 분류, 분기 과정 서술)
fig, ax = plt.subplots(figsize=(8.5, 5.2)); setup_tree(ax)
tnode(ax, 5, 5.3, ['links <= 5', 'Ham: 7, Spam: 7'], 'white')
tnode(ax, 2.6, 3.0, ['caps <= 40', 'Ham: 6, Spam: 1'], leafcolor(6, 1))
tnode(ax, 7.4, 3.0, ['caps <= 40', 'Ham: 1, Spam: 6'], leafcolor(1, 6))
tnode(ax, 1.3, 0.9, ['Ham: 5, Spam: 0'], leafcolor(5, 0), w=2.0, h=0.7)
tnode(ax, 3.9, 0.9, ['Ham: 1, Spam: 1'], leafcolor(1, 1), w=2.0, h=0.7)
tnode(ax, 6.1, 0.9, ['Ham: 1, Spam: 1'], leafcolor(1, 1), w=2.0, h=0.7)
tnode(ax, 8.7, 0.9, ['Ham: 0, Spam: 5'], leafcolor(0, 5), w=2.0, h=0.7)
tedge(ax, 5, 5.3, 2.6, 3.0, 'True'); tedge(ax, 5, 5.3, 7.4, 3.0, 'False')
tedge(ax, 2.6, 3.0, 1.3, 0.9, 'T'); tedge(ax, 2.6, 3.0, 3.9, 0.9, 'F')
tedge(ax, 7.4, 3.0, 6.1, 0.9, 'T'); tedge(ax, 7.4, 3.0, 8.7, 0.9, 'F')
save(fig, 'dt-n1')

# N2: 얕은 트리 vs 깊은 트리 (과적합 비교)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
ax = axes[0]; setup_tree(ax); ax.set_title('Tree P (shallow)', fontsize=11)
tnode(ax, 5, 4.7, ['x1 <= 3', 'No: 10, Yes: 10'], 'white')
tnode(ax, 2.7, 1.7, ['No: 8, Yes: 2'], leafcolor(8, 2), w=2.2, h=0.7)
tnode(ax, 7.3, 1.7, ['No: 2, Yes: 8'], leafcolor(2, 8), w=2.2, h=0.7)
tedge(ax, 5, 4.7, 2.7, 1.7, 'T'); tedge(ax, 5, 4.7, 7.3, 1.7, 'F')
ax = axes[1]; setup_tree(ax); ax.set_title('Tree Q (very deep)', fontsize=11)
tnode(ax, 5, 5.4, ['x1 <= 3'], 'white', w=1.7, h=0.6)
tnode(ax, 2.8, 3.7, ['x2 <= 5'], 'white', w=1.7, h=0.6)
tnode(ax, 7.2, 3.7, ['x2 <= 5'], 'white', w=1.7, h=0.6)
for x in (1.4, 4.0, 6.2, 8.6):
    tnode(ax, x, 2.0, ['x3<=1'], 'white', w=1.4, h=0.55)
for x in (0.7, 2.1, 3.3, 4.7, 5.5, 6.9, 7.9, 9.3):
    tnode(ax, x, 0.6, ['1'], leafcolor(1, 0) if int(x) % 2 else leafcolor(0, 1), w=0.9, h=0.5)
tedge(ax, 5, 5.4, 2.8, 3.7); tedge(ax, 5, 5.4, 7.2, 3.7)
tedge(ax, 2.8, 3.7, 1.4, 2.0); tedge(ax, 2.8, 3.7, 4.0, 2.0)
tedge(ax, 7.2, 3.7, 6.2, 2.0); tedge(ax, 7.2, 3.7, 8.6, 2.0)
ax.text(5, -0.1, '(each leaf = 1 training sample)', ha='center', fontsize=9, color='dimgray')
save(fig, 'dt-n2')

# N3: 불순도 - 루트 섞임 -> 분할 후 순수
fig, ax = plt.subplots(figsize=(8.0, 5.0)); setup_tree(ax)
tnode(ax, 5, 5.0, ['color <= 0.5', 'No: 5, Yes: 5'], 'white')
tnode(ax, 2.7, 1.7, ['No: 5, Yes: 0', '(pure)'], leafcolor(5, 0))
tnode(ax, 7.3, 1.7, ['No: 0, Yes: 5', '(pure)'], leafcolor(0, 5))
tedge(ax, 5, 5.0, 2.7, 1.7, 'True'); tedge(ax, 5, 5.0, 7.3, 1.7, 'False')
save(fig, 'dt-n3')

# N4: 루트 특성 강조 (특성 중요도)
fig, ax = plt.subplots(figsize=(8.5, 5.2)); setup_tree(ax)
tnode(ax, 5, 5.3, ['study_hours <= 4', 'Fail: 8, Pass: 8'], 'white')
tnode(ax, 2.6, 2.9, ['Fail: 7, Pass: 1'], leafcolor(7, 1))
tnode(ax, 7.4, 2.9, ['attend <= 60', 'Fail: 1, Pass: 7'], leafcolor(1, 7))
tnode(ax, 6.1, 0.8, ['Fail: 1, Pass: 1'], leafcolor(1, 1), w=2.0, h=0.7)
tnode(ax, 8.7, 0.8, ['Fail: 0, Pass: 6'], leafcolor(0, 6), w=2.0, h=0.7)
tedge(ax, 5, 5.3, 2.6, 2.9, 'True'); tedge(ax, 5, 5.3, 7.4, 2.9, 'False')
tedge(ax, 7.4, 2.9, 6.1, 0.8, 'T'); tedge(ax, 7.4, 2.9, 8.7, 0.8, 'F')
save(fig, 'dt-n4')


# ===================== Linear regression =====================
def reg_scatter(ax, x, y, line=None, title=None, residual=False, predict=None):
    x = np.array(x); y = np.array(y)
    ax.scatter(x, y, c=POINT, s=65, edgecolors='black', zorder=3)
    if line is not None:
        a, b = line
        xs = np.array([x.min() - 0.5, x.max() + 0.5])
        if predict is not None:
            xs = np.array([x.min() - 0.5, predict + 0.5])
        ax.plot(xs, a * xs + b, c='red', lw=2, zorder=2)
        if residual:
            for xi, yi in zip(x, y):
                ax.plot([xi, xi], [yi, a * xi + b], c='gray', lw=1.0, zorder=1)
        if predict is not None:
            ax.scatter([predict], [a * predict + b], c='red', marker='*', s=320,
                       edgecolors='black', zorder=4)
            ax.axvline(x.max(), color='gray', ls='--', lw=1)
            ax.annotate('training range ends', (x.max(), ax.get_ylim()[0]), fontsize=8,
                        color='dimgray', rotation=90, va='bottom', ha='right')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.grid(alpha=0.3)
    if title:
        ax.set_title(title, fontsize=11)


# N1: 비선형(곡선) 데이터에 직선 적합
fig, ax = plt.subplots(figsize=(6.2, 4.6))
rng = np.random.RandomState(31)
x = np.linspace(1, 10, 24)
y = -(x - 5.5) ** 2 + 30 + rng.normal(0, 2.0, 24)
reg_scatter(ax, x, y, line=(0.1, 17), title='linear fit on curved data (R2 = 0.05)')
save(fig, 'lr-n1')

# N2: 외삽 - 학습 범위(1~10) 밖 x=20 예측
fig, ax = plt.subplots(figsize=(6.2, 4.6))
rng = np.random.RandomState(32)
x = np.linspace(1, 10, 20); y = 2.0 * x + 5 + rng.normal(0, 1.5, 20)
reg_scatter(ax, x, y, line=(2.0, 5), title='predict at x=20 (outside training range)', predict=20)
save(fig, 'lr-n2')

# N3: 분산 작음(R2 높음) vs 큼(R2 낮음)
fig, axes = plt.subplots(2, 1, figsize=(6.2, 8.0))
rng = np.random.RandomState(33)
x = np.linspace(1, 10, 24)
y1 = 2 * x + 3 + rng.normal(0, 1.0, 24)
y2 = 2 * x + 3 + rng.normal(0, 7.0, 24)
reg_scatter(axes[0], x, y1, line=(2, 3), title='graph A  (R2 = 0.96)')
reg_scatter(axes[1], x, y2, line=(2, 3), title='graph B  (R2 = 0.41)')
save(fig, 'lr-n3')

# N4: 잔차(점-직선 수직거리) 표시
fig, ax = plt.subplots(figsize=(6.2, 4.6))
rng = np.random.RandomState(34)
x = np.linspace(1, 10, 14); y = 1.8 * x + 4 + rng.normal(0, 2.5, 14)
reg_scatter(ax, x, y, line=(1.8, 4), title='gray segments = residuals (errors)', residual=True)
save(fig, 'lr-n4')

# N5: 양의 상관 vs 음의 상관
fig, axes = plt.subplots(1, 2, figsize=(10, 4.3))
rng = np.random.RandomState(35)
x = np.linspace(1, 10, 20)
reg_scatter(axes[0], x, 2 * x + 3 + rng.normal(0, 1.5, 20), line=(2, 3), title='graph A')
reg_scatter(axes[1], x, -2 * x + 25 + rng.normal(0, 1.5, 20), line=(-2, 25), title='graph B')
save(fig, 'lr-n5')


# ===================== Confusion matrix =====================
def confusion(ax, mat, labels_actual, labels_pred, title=None):
    mat = np.array(mat)
    ax.imshow(mat, cmap='Blues')
    ax.set_xticks([0, 1]); ax.set_xticklabels(labels_pred)
    ax.set_yticks([0, 1]); ax.set_yticklabels(labels_actual)
    ax.set_xlabel('predicted'); ax.set_ylabel('actual')
    vmax = mat.max()
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(mat[i, j]), ha='center', va='center', fontsize=22,
                    color='white' if mat[i, j] > vmax * 0.5 else 'black')
    if title:
        ax.set_title(title, fontsize=11)


# N1: 스팸 필터 (위양성 강조)
fig, ax = plt.subplots(figsize=(5.6, 4.8))
confusion(ax, [[35, 15], [3, 47]], ['Actual: Ham', 'Actual: Spam'], ['Pred: Ham', 'Pred: Spam'])
save(fig, 'cm-n1')

# N2: 불균형 데이터 (정확도 함정)
fig, ax = plt.subplots(figsize=(5.6, 4.8))
confusion(ax, [[985, 5], [8, 2]], ['Actual: Neg', 'Actual: Pos'], ['Pred: Neg', 'Pred: Pos'])
save(fig, 'cm-n2')

# N3: 정확도 계산용
fig, ax = plt.subplots(figsize=(5.6, 4.8))
confusion(ax, [[50, 10], [20, 40]], ['Actual: Neg', 'Actual: Pos'], ['Pred: Neg', 'Pred: Pos'])
save(fig, 'cm-n3')

# N4: 두 모델 비교 (위양성형 vs 위음성형)
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))
confusion(axes[0], [[60, 30], [2, 28]], ['Actual: Neg', 'Actual: Pos'], ['Pred: Neg', 'Pred: Pos'], title='Model X')
confusion(axes[1], [[88, 2], [18, 12]], ['Actual: Neg', 'Actual: Pos'], ['Pred: Neg', 'Pred: Pos'], title='Model Y')
save(fig, 'cm-n4')

print('done: 25 images written to', OUT)
