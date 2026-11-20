"""재귀 호출 카드.
파이썬으로 실제 함수를 실행하며 sys.settrace로 call/line/return을 기록하고,
그 기록으로 카드 배치를 계산해 정적 HTML 한 장에 전부 그린다(재생 기능 없음).

사용:
  python recur_cards.py OUT.html                         내장 예제 전부
  python recur_cards.py OUT.html 이름 [이름 ...]          내장 예제 중 고른 것
  python recur_cards.py OUT.html --src SRC.py CALL [--src SRC.py CALL ...]
      SRC.py : 재귀 함수 정의(와 필요한 전역 변수). 함수 본문은 4칸 들여쓰기
      CALL   : 첫 호출식. 예) "f(-1, 0, 0)"
"""
import sys, json, ast, io, contextlib

EXAMPLES = [
    ('f(-1, 0, 0)', '''
A = [0, 1, 2, 7, 9, 10, 15, 16]
ans = 0

def f(k, s, j):
    if j == 3:
        if (s % 3) == 0:
            global ans
            ans = max(ans, s)
        return
    for i in range(k+1, len(A)):
        f(i, s + A[i], j + 1)
    return
'''),
    ('factorial(5)', '''
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)
'''),
    ('fib(4)', '''
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
'''),
]

# 배치 상수(px). 글자 폭은 14px 고정폭 글꼴 기준
CHW, PAD, IND = 8.2, 12, 18      # 글자 폭, 카드 안쪽 여백, 헤더 아래 줄 들여쓰기
HEAD, ROW, BOT = 30, 22, 8       # 헤더 높이, 줄 높이, 카드 아래 여백
FOLD_IND, FOLD_GAP = 24, 6         # 접힌 카드 안에서 자식 카드 들여쓰기, 헤더와 자식 사이
OV, GAP = 36, 8                  # 카드 겹침, 자식 카드가 끝난 뒤 부모 카드에 남기는 여백


def trace(src, call):
    events = []
    ids = {}                     # frame -> 카드 번호

    def tracer(frame, ev, arg):
        if frame.f_code.co_filename != '<src>' or frame.f_code.co_name == '<module>':
            return tracer
        if ev == 'call':
            cid = len(ids)
            ids[frame] = cid
            co = frame.f_code
            args = ', '.join(repr(frame.f_locals[v]) for v in co.co_varnames[:co.co_argcount])
            events.append({'t': 'call', 'id': cid, 'parent': ids.get(frame.f_back, -1),
                           'label': f'{co.co_name}({args})'})
        elif ev == 'line':
            loc = ', '.join(f'{k} = {v!r}' for k, v in frame.f_locals.items())
            events.append({'t': 'line', 'id': ids[frame], 'lineno': frame.f_lineno, 'locals': loc})
        elif ev == 'return':
            events.append({'t': 'return', 'id': ids[frame], 'value': repr(arg)})
        return tracer

    ns = {}
    exec(compile(src, '<src>', 'exec'), ns)
    sys.settrace(tracer)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(call, '<call>', 'eval'), ns)
    finally:
        sys.settrace(None)
    return events


def call_spans(text, fname):
    """text 안의 fname(...) 호출 구간 [(시작, 끝)]. 괄호 짝을 맞춰 끝을 찾는다"""
    spans, i = [], 0
    while True:
        a = text.find(fname + '(', i)
        if a < 0:
            return spans
        if a > 0 and (text[a - 1].isalnum() or text[a - 1] == '_'):     # 다른 이름의 끝부분이면 건너뛴다
            i = a + 1
            continue
        depth, b = 0, a + len(fname)
        while b < len(text):
            depth += {'(': 1, ')': -1}.get(text[b], 0)
            b += 1
            if depth == 0:
                break
        spans.append((a, b))
        i = b


def build(src, call, folded=False):
    """기록을 시간 순서대로 따라가며 배치한다.
    - 카드 x는 호출 깊이로 정한다(깊을수록 오른쪽, 부모 카드 오른쪽 끝에 OV만큼 겹친다)
    - 카드 안의 줄은 실행된 순서대로 아래로 쌓인다
    - 자식 카드는 호출한 줄 높이에서 시작하고, 부모 카드는 자식이 끝날 때까지 아래로 늘어난다
    - 카드 맨 아래 줄은 돌려준 값이다"""
    src = src.strip('\n')
    lines = src.split('\n')
    events = trace(src, call)

    # 블록 머리 줄 -> (본문 첫 줄, 본문 끝 줄, 본문을 건너뛸 때 붙일 주석)
    # for/while: 본문으로 들어가지 않으면 반복 끝. if: 본문으로 들어가지 않으면 조건이 거짓
    loops = {}
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.For):
            msg = f'# {ast.get_source_segment(src, node.iter)}에 남은 {ast.get_source_segment(src, node.target)} 값이 없어 반복 끝'
        elif isinstance(node, ast.While):
            msg = f'# {ast.get_source_segment(src, node.test)} : 거짓이라 반복 끝'
        elif isinstance(node, ast.If):
            msg = f'# {ast.get_source_segment(src, node.test)} : 거짓이라 건너뜀'
        else:
            continue
        if node.body[0].lineno == node.lineno:            # 머리 줄과 본문이 한 줄이면 판정할 수 없다
            continue
        loops[node.lineno] = (node.body[0].lineno, node.body[-1].end_lineno, msg)

    # 블록 머리 줄 실행 뒤 같은 호출 안의 다음 줄이 본문 밖이면, 본문을 건너뛴 것이다
    loop_end = {}
    for n, e in enumerate(events):
        if e['t'] == 'line' and e['lineno'] in loops:
            a, b, msg = loops[e['lineno']]
            nxt = next(x for x in events[n + 1:] if x['id'] == e['id'] and x['t'] in ('line', 'return'))
            if nxt['t'] == 'return' or not (a <= nxt['lineno'] <= b):
                loop_end[id(e)] = msg

    def width(t):                                     # 한글은 2칸으로 센다
        return sum(2 if '가' <= ch <= '힣' else 1 for ch in t)

    body = [l[4:] for l in lines[1:]]                 # def 본문 들여쓰기 4칸을 뗀다
    notes = [lines[k - 1][4:len(lines[k - 1]) - len(lines[k - 1].lstrip())] + '    ' + m for k, (_, _, m) in loops.items()]
    labels = [e['label'] for e in events if e['t'] == 'call']
    first_loc = {}
    for e in events:
        if e['t'] == 'line':
            first_loc.setdefault(e['id'], e['locals'])
    head = [len(e['label']) + 4 + len(first_loc.get(e['id'], '')) for e in events if e['t'] == 'call']
    maxlen = max(max(width(l) for l in body) + 2, max(head))      # 본문 줄은 헤더보다 IND만큼 들어가 있다
    STEP = round(PAD + IND + maxlen * CHW + PAD)                 # 깊이 한 단계마다 오른쪽으로 가는 거리
    note_w = max([width(t) for t in notes] or [0])
    CW = max(STEP + OV, round(PAD + IND + note_w * CHW + PAD))   # 카드 폭. 주석 줄이 길면 넓어지고 자식과 더 겹친다

    depth = {}
    for e in events:
        if e['t'] == 'call':
            depth[e['id']] = 0 if e['parent'] < 0 else depth[e['parent']] + 1

    cards = {}
    for n, e in enumerate(events):
        if e['t'] == 'call':
            pc = cards.get(e['parent'])
            if pc is None:
                x, y = 10, 10
            elif pc['fold']:
                # 접힌 카드 안: 코드 줄이 없으므로 헤더 바로 아래에 한 단계 들여 놓고, 형제는 앞 카드가 끝난 아래에 놓는다
                x = pc['x'] + FOLD_IND
                y = pc['cur'] + (FOLD_GAP if not pc['row_kids'] else 0)
                pc['row_kids'].append(e['id'])
            else:
                # 호출한 줄 바로 아래, 그 줄의 첫 호출 식이 시작하는 글자 위치에 맞춰 시작한다
                # 같은 줄의 두 번째 호출은 앞 호출이 끝난 아래, 같은 위치(같은 깊이)에서 시작
                row_txt = pc['rows'][-1]['text']
                spans = call_spans(row_txt, e['label'].split('(')[0])
                col = spans[0][0] if spans else 0
                x = pc['x'] + PAD + IND + col * CHW
                y = pc['last_row_y'] + ROW if not pc['kid_after_row'] else pc['cur'] + GAP
                pc['kid_after_row'] = True
                pc['row_kids'].append(e['id'])      # 이 줄에서 부른 호출들. 반환값을 줄에 끼워 넣을 때 쓴다
            cards[e['id']] = {'id': e['id'], 'label': e['label'], 'parent': e['parent'], 'x': x, 'y': y,
                              'cur': y + HEAD, 'rows': [], 'locals': first_loc.get(e['id']), 'last_row_y': None,
                              'fold': folded and depth[e['id']] >= 1,
                              'kid_after_row': False, 'row_kids': [], 'value': None}
        elif e['t'] == 'line':
            c = cards[e['id']]
            if c['fold']:                       # 접힌 카드는 코드 줄을 그리지 않는다
                continue
            c['rows'].append({'y': c['cur'], 'text': lines[e['lineno'] - 1][4:]})
            c['last_row_y'] = c['cur']
            c['cur'] += ROW
            c['kid_after_row'] = False
            c['row_kids'] = []
            if c['locals'] is None:
                c['locals'] = e['locals']
            if id(e) in loop_end:
                # 본문을 건너뜀(반복 끝, 조건 거짓): 머리 줄 안쪽으로 한 단계 들여 이유를 쓴다. 다음 줄은 원래 들여쓰기로 돌아간다
                head_txt = c['rows'][-1]['text']
                ind = head_txt[:len(head_txt) - len(head_txt.lstrip())] + '    '
                c['rows'].append({'y': c['cur'], 'text': ind + loop_end[id(e)], 'kind': 'note'})
                c['cur'] += ROW
        else:
            c = cards[e['id']]
            if c['fold']:
                c['value'] = e['value']
                # 자식이 있으면 마지막 자식 아래까지, 없으면 헤더만
                c['cur'] = c['cur'] - GAP + FOLD_GAP if c['row_kids'] else c['y'] + HEAD + 2 - BOT
            else:
                last = c['rows'][-1]['text'] if c['rows'] else ''
                indent = last[:len(last) - len(last.lstrip())]
                calls = call_spans(last, c['label'].split('(')[0])
                if last.strip().startswith('return') and calls:
                    # 실행된 return 문. 호출 부분은 돌려받은 값으로 바뀌므로 취소선
                    c['rows'].append({'y': c['cur'], 'text': last, 'kind': 'del', 'strike': calls})
                    c['cur'] += ROW
                c['value'] = e['value']
                vals = [cards[k]['value'] for k in c['row_kids']]
                if calls and len(calls) == len(vals):
                    # 호출 구간만 돌려받은 값으로 바꾸고 나머지 식은 그대로 둔다
                    new, pos = '', 0
                    for (a, b), v in zip(calls, vals):
                        new += last[pos:a] + v
                        pos = b
                    new += last[pos:]
                    c['rows'].append({'y': c['cur'], 'text': new + '   # ' + e['value'], 'kind': 'add'})
                    c['cur'] += ROW
                elif last.strip().startswith('return'):
                    # 호출 없는 return 문은 다시 쓰지 않고 실행된 줄을 초록으로 칠해 값만 붙인다
                    c['rows'][-1].update(text=last + '   # ' + e['value'], kind='add')
                else:
                    # return 문 없이 함수 끝에 닿은 경우
                    c['rows'].append({'y': c['cur'], 'text': indent + 'return   # ' + e['value'], 'kind': 'add'})
                    c['cur'] += ROW
            c['h'] = c['cur'] + BOT - c['y']
            if c['parent'] >= 0:
                pc = cards[c['parent']]
                pc['cur'] = max(pc['cur'], c['y'] + c['h'] + GAP)

    width = max(c['x'] + CW for c in cards.values()) + 20
    height = max(c['y'] + c['h'] for c in cards.values()) + 20
    out_cards = [{k: c[k] for k in ('id', 'label', 'parent', 'x', 'y', 'h', 'rows', 'locals', 'fold')}
                 for c in cards.values()]
    return {'cards': out_cards, 'cw': CW, 'width': width, 'height': height}


import html as _h


def esc(s):
    return _h.escape(s, quote=False)


def render(d, title=True):
    """기록 전체를 한 번에 그린다"""
    s = f'<h2>{esc(d["name"])}</h2>' if title else ''
    s += f'<div class="stage" style="width:{d["width"]:.0f}px;height:{d["height"]:.0f}px">'
    for c in d['cards']:
        rows = ''
        for r in c['rows']:
            kind = r.get('kind')
            t = r['text']
            if kind == 'del':
                body, pos = '', 0
                for a, b in r['strike']:
                    body += esc(t[pos:a]) + '<s>' + esc(t[a:b]) + '</s>'
                    pos = b
                body += esc(t[pos:])
            else:
                body = esc(t)
            sign = {'del': '<span class="sign">-</span>', 'add': '<span class="sign">+</span>'}.get(kind, '')
            rows += (f'<div class="row{" " + kind if kind else ""}" style="top:{r["y"] - c["y"]:.0f}px">'
                     f'{sign}{body}</div>')
        s += (f'<div class="card{" fold" if c["fold"] else ""}" style="left:{c["x"]:.0f}px;top:{c["y"]:.0f}px;width:{d["cw"]}px;'
              f'height:{c["h"]:.0f}px;z-index:{c["id"] + 1}">'
              f'<div class="head"><span>{esc(c["label"])}</span><span class="loc">{esc(c["locals"] or "")}</span></div>'
              + rows + '</div>')
    return s + '</div>'


def figure(src, call):
    """접은 그림(기본)과 펼친 그림을 함께 싣는다. 누르면 펼치고, 다시 누르면 접는다"""
    full = build(src, call)
    fold = build(src, call, folded=True)
    if len(fold['cards']) == len(full['cards']) and not any(c['fold'] for c in fold['cards']):
        return render(full, title=False)
    return ('<div class="rc" onclick="this.classList.toggle(\'open\')">'
            '<div class="fold-view">' + render(fold, title=False) + '</div>'
            '<div class="full-view">' + render(full, title=False) + '</div></div>')


CSS = '''
body { font-family: "Malgun Gothic", sans-serif; color: #111; background: #fff; margin: 0; padding: 16px; font-size: 14px; }
h2 { font-size: 16px; font-family: Consolas, "D2Coding", monospace; margin: 24px 0 8px; }
.stage { position: relative; }
.card { position: absolute; background: #fff; border: 1px solid #888; box-shadow: 2px 2px 6px rgba(0,0,0,.18);
        font-family: Consolas, "D2Coding", monospace; font-size: 14px; }
.card .head { height: 30px; line-height: 30px; padding: 0 12px; font-weight: bold; border-bottom: 1px solid #ddd;
              display: flex; justify-content: space-between; white-space: pre; }
.card .head .loc { font-weight: normal; color: #666; }
.card .row { position: absolute; left: 0; height: 22px; line-height: 22px; padding-left: 30px; white-space: pre; }
.card .row { right: 0; }
.card .row .sign { position: absolute; left: 14px; }
.card .row.note { color: #777; }
.card .row.del { background: #ffebe9; color: #82071e; }
.card .row.add { background: #e6ffec; color: #116329; }
.rc { cursor: pointer; }
.rc .full-view { display: none; }
.rc.open .full-view { display: block; }
.rc.open .fold-view { display: none; }
'''

def main():
    OUT_PATH = sys.argv[1]
    ARGS = sys.argv[2:]
    if '--src' in ARGS:                                          # --src SRC.py CALL 묶음들
        JOBS = []
        while ARGS:
            assert ARGS[0] == '--src' and len(ARGS) >= 3, '형식: --src SRC.py CALL'
            JOBS.append((ARGS[2], open(ARGS[1], encoding='utf-8').read()))
            ARGS = ARGS[3:]
    else:                                                        # 이름을 주면 그 내장 예제만
        JOBS = [(name, src) for name, src in EXAMPLES if not ARGS or name in ARGS]
    DATA = [(name, figure(src, name)) for name, src in JOBS]

    doc = ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           '<title>재귀 호출 카드</title>\n<style>' + CSS + '</style>\n</head>\n<body>\n'
           + '\n'.join(f'<h2>{esc(name)}</h2>' + fig for name, fig in DATA) + '\n</body>\n</html>\n')
    bad = sorted({ch for ch in doc if ord(ch) > 127 and not ('\uac00' <= ch <= '\ud7a3')})
    assert not bad, bad
    open(OUT_PATH, 'w', encoding='utf-8').write(doc)
    for name, fig in DATA:
        print(name, len(fig))


if __name__ == '__main__':
    main()
