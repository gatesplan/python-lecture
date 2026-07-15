# -*- coding: utf-8 -*-
"""
암호/압축 변환 -> 코드 제시형 문제 생성기.

원칙: 문제 본문(content)에 변환 이름(스키테일/순열/카이사르/런길이)을 노출하지 않는다.
학생은 코드를 직접 읽고 동작을 추론한다. 허프만만은 코드화가 비현실적이라
'이름 없는 규칙 서술형'으로 제시한다.

안전장치: 생성한 코드 문자열을 실제로 exec해 stdout을 받고, 시뮬레이터 결과와
일치하는지 검증한 뒤에만 문제로 채택한다.

변환 표기(내부용): ('C',shift) ('S',cols) ('P',key,k) ('R',) ('H',)
"""
import io
import json
import heapq
import contextlib

# ===================== 변환 시뮬레이터 =====================

def caesar(s, shift):
    r = ''
    for ch in s:
        if 'A' <= ch <= 'Z':
            r += chr((ord(ch) - 65 + shift) % 26 + 65)
        elif 'a' <= ch <= 'z':
            r += chr((ord(ch) - 97 + shift) % 26 + 97)
        else:
            r += ch
    return r


def scytale(s, cols):
    n = len(s)
    rows = (n + cols - 1) // cols
    r = ''
    for c in range(cols):
        for rw in range(rows):
            idx = rw * cols + c
            if idx < n:
                r += s[idx]
    return r


def permute(s, key, k):
    r = ''
    for b in range(0, len(s), k):
        for j in key:
            if b + j < len(s):
                r += s[b + j]
    return r


def rle(s):
    if not s:
        return ''
    r = ''
    cur = s[0]
    cnt = 1
    for ch in s[1:]:
        if ch == cur:
            cnt += 1
        else:
            r += cur + str(cnt)
            cur = ch
            cnt = 1
    r += cur + str(cnt)
    return r


def huffman(s):
    """반환: (codes, bits, steps, freq)
    steps: [(left_label, left_freq, right_label, right_freq, parent_label, parent_freq)]"""
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    heap = []
    for ch in sorted(freq):
        heap.append((freq[ch], ord(ch), ch, ch, None, None))
    heapq.heapify(heap)
    steps = []
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        left, right = (a, b) if a[1] <= b[1] else (b, a)
        mfreq = a[0] + b[0]
        mascii = min(a[1], b[1])
        mlabel = left[2] + right[2]
        steps.append((left[2], left[0], right[2], right[0], mlabel, mfreq))
        heapq.heappush(heap, (mfreq, mascii, mlabel, None, left, right))
    root = heap[0]
    codes = {}

    def walk(node, prefix):
        _, _, _, ch, left, right = node
        if left is None and right is None:
            codes[ch] = prefix if prefix else '0'
            return
        walk(left, prefix + '0')
        walk(right, prefix + '1')

    walk(root, '')
    bits = ''.join(codes[ch] for ch in s)
    return codes, bits, steps, freq


# ===================== 코드 본문 생성 (중립 변수명, 이름 없음) =====================

def _body(t):
    """변수 s를 입력으로, r에 결과를 만드는 코드 라인 리스트."""
    if t[0] == 'C':
        return ['r = ""', 'for ch in s:',
                '    r += chr((ord(ch) - 65 + %d) %% 26 + 65)' % t[1]]
    if t[0] == 'S':
        return ['cols = %d' % t[1], 'rows = len(s) // cols', 'r = ""',
                'for c in range(cols):', '    for row in range(rows):',
                '        r += s[row * cols + c]']
    if t[0] == 'P':
        return ['key = %s' % str(t[1]), 'k = %d' % t[2], 'r = ""',
                'for b in range(0, len(s), k):', '    for j in key:',
                '        if b + j < len(s):', '            r += s[b + j]']
    if t[0] == 'R':
        return ['r = ""', 'i = 0', 'while i < len(s):', '    c = s[i]',
                '    cnt = 0', '    while i < len(s) and s[i] == c:',
                '        cnt += 1', '        i += 1', '    r += c + str(cnt)']
    raise ValueError(t)


def code_single(plain, t):
    return '\n'.join(['s = "%s"' % plain] + _body(t) + ['print(r)'])


def code_combo(plain, steps):
    names = ['f', 'g', 'h']
    funcs = []
    for idx, t in enumerate(steps):
        lines = ['def %s(s):' % names[idx]] + ['    ' + ln for ln in _body(t)] + ['    return r']
        funcs.append('\n'.join(lines))
    expr = '"%s"' % plain
    for nm in names[:len(steps)]:
        expr = '%s(%s)' % (nm, expr)
    return '\n\n'.join(funcs) + '\n\nprint(%s)' % expr


def run_code(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {})
    return buf.getvalue().strip()


# ===================== 변환 적용/추적 =====================

def apply_one(s, t):
    if t[0] == 'C':
        return caesar(s, t[1])
    if t[0] == 'S':
        return scytale(s, t[1])
    if t[0] == 'P':
        return permute(s, t[1], t[2])
    if t[0] == 'R':
        return rle(s)
    raise ValueError(t)


def trace(plain, steps):
    cur = plain
    tr = []
    for t in steps:
        prev = cur
        cur = apply_one(cur, t)
        tr.append((prev, cur))
    return cur, tr


# ===================== 허프만 규칙 (이름 없는 condition-box) =====================

HUFF_RULES = [
    "부호화: 빈도가 가장 작은 두 노드를 합쳐 부모 노드를 만든다(반복).",
    "빈도가 같으면 ASCII가 작은(빠른) 노드를 먼저 고른다.",
    "두 노드를 합칠 때 ASCII가 작은 쪽을 왼쪽(0), 큰 쪽을 오른쪽(1)에 둔다.",
    "ASCII 순서: A(65) < B(66) < ... < Z(90).",
]


def huff_explain(label_target, target):
    codes, bits, steps, freq = huffman(target)
    lines = [label_target]
    lines.append("빈도: " + ", ".join("%s:%d" % (c, freq[c]) for c in sorted(freq)))
    for (ll, lf, rl, rf, pl, pf) in steps:
        lines.append("%s(%d) + %s(%d) -> %s(%d): %s=왼쪽(0), %s=오른쪽(1)"
                     % (ll, lf, rl, rf, pl, pf, ll, rl))
    lines.append("코드: " + ", ".join("%s=%s" % (c, codes[c]) for c in sorted(codes)))
    lines.append("비트열: " + " ".join(codes[ch] for ch in target) + " = " + bits)
    lines.append("정답: " + bits)
    return bits, lines


# ===================== 문제 빌더 =====================

def build(pid, plain, steps):
    """steps의 마지막이 ('H',)이면 허프만 종결 문제, 아니면 코드 실행 결과 문제."""
    has_h = steps[-1][0] == 'H'
    pre = steps[:-1] if has_h else steps

    content = []
    explain_lines = []

    # 선행 코드형 변환 결과(허프만 입력 또는 최종값)
    mid, tr = trace(plain, pre)

    if has_h:
        if pre:
            # 코드 + 규칙
            code = code_single(plain, pre[0]) if len(pre) == 1 else code_combo(plain, pre)
            got = run_code(code)
            assert got == mid, "code/sim mismatch %s: %r != %r" % (pid, got, mid)
            content.append({"type": "text",
                            "content": "다음 코드의 출력 문자열을, 아래 규칙으로 부호화한 최종 비트열을 쓰시오."})
            content.append({"type": "code", "language": "python", "content": code})
            content.append({"type": "condition-box", "title": "규칙", "marker": "kr-con", "items": list(HUFF_RULES)})
            bits, hlines = huff_explain("코드 출력: " + mid, mid)
            for i, (a, b) in enumerate(tr):
                explain_lines.append("코드 %d단계: %s -> %s" % (i + 1, a, b))
            explain_lines += hlines
        else:
            content.append({"type": "text",
                            "content": "다음 평문을 아래 규칙으로 부호화한 최종 비트열을 쓰시오."})
            content.append({"type": "text", "content": "평문: " + plain})
            content.append({"type": "condition-box", "title": "규칙", "marker": "kr-con", "items": list(HUFF_RULES)})
            bits, hlines = huff_explain("부호화 대상: " + plain, plain)
            explain_lines += hlines
        answer = bits
    else:
        code = code_single(plain, pre[0]) if len(pre) == 1 else code_combo(plain, pre)
        got = run_code(code)
        assert got == mid, "code/sim mismatch %s: %r != %r" % (pid, got, mid)
        content.append({"type": "text", "content": "다음 코드의 실행 결과를 쓰시오."})
        content.append({"type": "code", "language": "python", "content": code})
        for i, (a, b) in enumerate(tr):
            explain_lines.append("%d단계: %s -> %s" % (i + 1, a, b))
        explain_lines.append("정답: " + mid)
        answer = mid

    return {
        "id": pid,
        "type": "short",
        "content": content,
        "answer": {"type": "value", "value": answer},
        "explain": [{"type": "process-box", "title": "풀이",
                     "content": [{"type": "text", "content": ln} for ln in explain_lines]}],
    }


# ===================== 기존 g1-061~080 (이름 제거 수정) =====================

EXISTING = [
    ('g1-061', 'HELLO', [('C', 3)]),
    ('g1-062', 'PYTHON', [('C', 5)]),
    ('g1-063', 'ABCDEF', [('S', 3)]),
    ('g1-064', 'DATABASE', [('S', 4)]),
    ('g1-065', 'BANANA', [('H',)]),
    ('g1-066', 'PEPPER', [('H',)]),
    ('g1-067', 'SECRET', [('C', 1), ('S', 3)]),
    ('g1-068', 'PLANET', [('C', 2), ('S', 2)]),
    ('g1-069', 'FRIEND', [('S', 3), ('C', 1)]),
    ('g1-070', 'GARDEN', [('S', 2), ('C', 3)]),
    ('g1-071', 'APPLE', [('C', 1), ('H',)]),
    ('g1-072', 'BUBBLE', [('C', 2), ('H',)]),
    ('g1-073', 'LETTER', [('S', 2), ('H',)]),
    ('g1-074', 'COFFEE', [('S', 3), ('H',)]),
    ('g1-075', 'PUZZLE', [('C', 1), ('S', 3), ('H',)]),
    ('g1-076', 'GARDEN', [('C', 2), ('S', 2), ('H',)]),
    ('g1-077', 'SUMMER', [('S', 2), ('C', 1), ('H',)]),
    ('g1-078', 'WINTER', [('S', 3), ('C', 2), ('H',)]),
    ('g1-079', 'AAABBBCCD', [('R',)]),
    ('g1-080', 'AABBA', [('C', 1), ('R',)]),
]

# 기존 정답(재현 검증용)
EXISTING_ANS = {
    'g1-061': 'KHOOR', 'g1-062': 'UDYMTS', 'g1-063': 'ADBECF', 'g1-064': 'DBAATSAE',
    'g1-065': '100110110', 'g1-066': '100110001', 'g1-067': 'TSFFDU', 'g1-068': 'RCGNPV',
    'g1-069': 'GFSOJE', 'g1-070': 'JUHDGQ', 'g1-071': '0001101001', 'g1-072': '01100101100',
    'g1-073': '010100001011', 'g1-074': '000100101101', 'g1-075': '10001101100010',
    'g1-076': '0111101000000110', 'g1-077': '10010001101001', 'g1-078': '1110001000010011',
    'g1-079': 'A3B3C2D1', 'g1-080': 'B2C2B1',
}


def build_existing():
    out = []
    for pid, plain, steps in EXISTING:
        prob = build(pid, plain, steps)
        exp = EXISTING_ANS[pid]
        ok = prob['answer']['value'] == exp
        print(('OK  ' if ok else 'FAIL') + ' %s -> %s (기존 %s)' % (pid, prob['answer']['value'], exp))
        assert ok, pid
        out.append(prob)
    return out


# ===================== 신규 g1-081~ (누락 조합/순열, 코드 제시형) =====================

NEW = [
    # 순열 단독 (스키테일 단독 g1-063/064와 코드 구조 대비)
    ('g1-081', 'ALGORITHM', [('P', [2, 0, 1], 3)]),
    ('g1-082', 'NOTEBOOKS', [('P', [1, 2, 0], 3)]),
    # 2-조합 누락분
    ('g1-083', 'COMPUTERS', [('S', 3), ('P', [2, 0, 1], 3)]),   # S->P
    ('g1-084', 'ALGORITHM', [('P', [2, 0, 1], 3), ('S', 3)]),   # P->S
    ('g1-085', 'AAAABBBB', [('S', 2), ('R',)]),                 # S->R
    ('g1-086', 'AABBBA', [('P', [2, 0, 1], 3), ('R',)]),        # P->R
    ('g1-087', 'COFFEE', [('P', [1, 0], 2), ('H',)]),           # P->H
    # 3-조합 누락분: 런길이 종결
    ('g1-088', 'AAAABBBB', [('S', 2), ('C', 1), ('R',)]),       # S->C->R
    ('g1-089', 'AAAAAABB', [('C', 1), ('S', 2), ('R',)]),       # C->S->R
    # 3-조합 누락분: 순열 포함
    ('g1-090', 'PYTHON', [('C', 2), ('P', [1, 0], 2), ('H',)]),  # C->P->H
    ('g1-091', 'LETTER', [('P', [1, 0], 2), ('C', 1), ('H',)]),  # P->C->H
    ('g1-092', 'COMPUTER', [('P', [1, 0], 2), ('S', 2), ('H',)]),  # P->S->H
]


def build_new():
    out = []
    for pid, plain, steps in NEW:
        prob = build(pid, plain, steps)
        seq = '->'.join(t[0] for t in steps)
        print('OK   %s [%s] %s -> %s' % (pid, seq, plain, prob['answer']['value']))
        out.append(prob)
    return out


def save():
    import os
    base = os.path.join(os.path.dirname(__file__), '..', 'exam-builder',
                        'frontend', 'src', 'data')
    # 1) 기존 01.json의 g1-061~080 교체
    p01 = os.path.join(base, 'problems-cnsh-26-1-2-01.json')
    data = json.load(open(p01, encoding='utf-8'))
    fixed = {p['id']: p for (pid, plain, steps) in EXISTING
             for p in [build(pid, plain, steps)]}
    for i, prob in enumerate(data):
        if prob['id'] in fixed:
            data[i] = fixed[prob['id']]
    json.dump(data, open(p01, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 2) 신규 -> 새 파일
    p05 = os.path.join(base, 'problems-cnsh-26-1-2-05.json')
    json.dump([build(pid, plain, steps) for (pid, plain, steps) in NEW],
              open(p05, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('saved:', p01, '/', p05)


if __name__ == '__main__':
    import sys
    build_existing()
    print('=== 기존 20문제 정답 재현 + 코드 exec 검증 완료 ===')
    print()
    build_new()
    print('=== 신규 12문제 생성 + 코드 exec 검증 완료 ===')
    if '--save' in sys.argv:
        save()
