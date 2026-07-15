# -*- coding: utf-8 -*-
"""
전치 암호(transposition cipher) 문제 생성기.
채택 구현(방식2, 이중 반복문 + 부분블록 가드)을 그대로 시뮬레이션해
정답과 풀이를 계산하고 exam-builder JSON(problems-draft-05.json)을 만든다.

문제 형식: type="short", 코드 빈칸은 [[]], 정답은 answer.value, 풀이는 process-box.
"""
import json
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "exam-builder",
                   "frontend", "src", "data", "problems-draft-05.json")

# ----- 채택 구현 -----
def enc(s, key, k):
    r = ''
    for b in range(0, len(s), k):
        for j in key:
            if b + j < len(s):
                r += s[b + j]
    return r

def inv_key(key):
    k = len(key)
    inv = [0] * k
    for i in range(k):
        inv[key[i]] = i
    return inv

def dec(cipher, key, k):
    # 딱 떨어지는 길이만 사용(부분블록 복호화는 단순 역순열로 어긋남)
    return enc(cipher, inv_key(key), k)

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

# ----- 코드 문자열 생성 -----
def enc_code(s, key, k):
    return (f's = "{s}"\n'
            f'key = {key}\n'
            f'k = {k}\n'
            f"result = ''\n"
            f'for b in range(0, len(s), k):\n'
            f'    for j in key:\n'
            f'        if b + j < len(s):\n'
            f'            result += s[b + j]\n'
            f'print(result)')

def dec_code(cipher, key, k):
    return (f's = "{cipher}"\n'
            f'key = {key}\n'
            f'k = {k}\n'
            f'inv = [0] * k\n'
            f'for i in range(k):\n'
            f'    inv[key[i]] = i\n'
            f"result = ''\n"
            f'for b in range(0, len(s), k):\n'
            f'    for j in inv:\n'
            f'        if b + j < len(s):\n'
            f'            result += s[b + j]\n'
            f'print(result)')

# ----- 블록/풀이 헬퍼 -----
def blocks_of(s, k):
    return [s[i:i+k] for i in range(0, len(s), k)]

def rearrange_block(blk, key):
    return ''.join(blk[j] for j in key if j < len(blk))

def explain_enc(s, key, k):
    blks = blocks_of(s, k)
    lines = []
    lines.append("블록 크기 k=" + str(k) + "로 끊는다: " + " ".join("[" + b + "]" for b in blks))
    lines.append("각 블록을 key=" + str(key) + " 위치(0-based) 순서로 재배열한다.")
    for b in blks:
        used = [j for j in key if j < len(b)]
        picks = " ".join(b[j] + "(" + str(j) + ")" for j in used)
        skipped = [j for j in key if j >= len(b)]
        note = ""
        if skipped:
            note = "  (위치 " + ",".join(str(x) for x in skipped) + "는 블록 범위 밖 -> 가드로 건너뜀)"
        lines.append("  [" + b + "] -> " + rearrange_block(b, key) + "  : " + picks + note)
    lines.append("이어 붙이면 정답: " + enc(s, key, k))
    return lines

def explain_dec(cipher, key, k):
    inv = inv_key(key)
    lines = []
    lines.append("복호화는 암호화 키의 역순열을 적용한다.")
    lines.append("key=" + str(key) + " 의 역순열 inv=" + str(inv) + " (inv[key[i]]=i)")
    lines += explain_enc(cipher, inv, k)[1:]  # 같은 알고리즘을 inv로
    lines[-1] = "이어 붙이면 정답(원문): " + dec(cipher, key, k)
    return lines

# ----- JSON 블록 헬퍼 -----
def tb(t): return {"type": "text", "content": t}
def cb(code): return {"type": "code", "language": "python", "content": code}
def ob(o): return {"type": "output-sample", "content": o}
def pbox(lines): return [{"type": "process-box", "title": "풀이",
                          "content": [tb(l) for l in lines]}]

PROBLEMS = []
_next = 204
def add(content, answer_value, explain_lines, ptype="short"):
    global _next
    PROBLEMS.append({
        "id": "fb-" + str(_next),
        "type": ptype,
        "content": content,
        "answer": {"type": "value", "value": answer_value},
        "explain": pbox(explain_lines),
    })
    _next += 1

TRACE = "다음 코드의 실행 결과를 쓰시오."
BLANK = "다음 코드의 실행 결과가 <출력>과 같을 때, 빈칸에 들어갈 내용을 쓰시오."

# =========================================================
# A. 결과추적 - 암호화 (반복 연습형 포함, 다수)
# =========================================================
enc_cases = [
    ("ABCDEF",   [0, 2, 1], 3),   # 딱 떨어짐
    ("ABCDEFG",  [0, 2, 1], 3),   # 부분블록(G)
    ("ABCDEFGH", [0, 2, 1], 3),   # 부분블록(GH)
    ("ABCDEFGHI",[0, 2, 1], 3),   # 딱 떨어짐(9)
    ("ABCDEFG",  [2, 1, 0], 3),   # 역순 블록
    ("ABCDEFG",  [1, 0, 2], 3),   # 213
    ("ABCDEFG",  [2, 0, 1], 3),   # 312
    ("ABCDEFG",  [1, 2, 0], 3),   # 231
    ("PYTHON",   [0, 2, 1], 3),   # 실제 단어
    ("PROGRAM",  [2, 1, 0], 3),   # 7글자 부분블록
    ("12345678", [0, 2, 1], 3),   # 숫자
    ("A1B2C3D4", [2, 1, 0], 3),   # 영문+숫자, 부분블록(D4? len8 -> 2남음)
    ("ABCDEF",   [1, 0],    2),   # k=2
    ("ABCDEFG",  [1, 0],    2),   # k=2 부분블록(1)
    ("COMPUTER", [1, 0],    2),   # k=2 단어
    ("ABCDEFGH", [3, 1, 2, 0], 4),    # k=4
    ("ABCDEFGHIJ",[1, 3, 0, 2], 4),   # k=4 부분블록(2)
    ("ABCDEFGHIJKL",[2, 0, 3, 1], 4), # k=4 딱 떨어짐
    ("SECURITY", [2, 0, 1], 3),   # 8글자 부분블록
    ("NETWORK",  [1, 2, 0], 3),   # 7글자 부분블록
]
for s, key, k in enc_cases:
    add([tb(TRACE), cb(enc_code(s, key, k))], enc(s, key, k), explain_enc(s, key, k))

# =========================================================
# B. 결과추적 - 복호화 (역순열, 딱 떨어지는 길이만)
# =========================================================
dec_cases = [
    ("ACBDFE",   [0, 2, 1], 3),   # ABCDEF 암호문
    ("CBAFED",   [2, 1, 0], 3),   # 역순키
    ("BCAEFD",   [2, 0, 1], 3),   # 312
    ("CABFDE",   [1, 2, 0], 3),   # 231
    ("BADCFE",   [1, 0],    2),   # k=2
    ("BCDAFGHE", [3, 0, 1, 2], 4),# k=4
]
for cipher, key, k in dec_cases:
    add([tb("다음은 전치 암호의 복호화 코드이다. " + TRACE), cb(dec_code(cipher, key, k))],
        dec(cipher, key, k), explain_dec(cipher, key, k))

# =========================================================
# C. 이중 적용 / 시저 결합
# =========================================================
# C1. 전치 2회(같은 키)
def double_enc_code(s, key, k):
    return (f's = "{s}"\n'
            f'key = {key}\n'
            f'k = {k}\n'
            f'def transpose(s, key, k):\n'
            f"    r = ''\n"
            f'    for b in range(0, len(s), k):\n'
            f'        for j in key:\n'
            f'            if b + j < len(s):\n'
            f'                r += s[b + j]\n'
            f'    return r\n'
            f'print(transpose(transpose(s, key, k), key, k))')

s, key, k = "ABCDEFGH", [0, 2, 1], 3
once = enc(s, key, k); twice = enc(once, key, k)
add([tb("다음 코드의 실행 결과를 쓰시오. (전치 암호를 두 번 적용한다.)"), cb(double_enc_code(s, key, k))],
    twice,
    ["1차 전치: " + s + " -> " + once,
     "2차 전치: " + once + " -> " + twice + " (1차 결과를 다시 같은 방식으로 전치)",
     "정답: " + twice])

# C2. 전치 2회(다른 키)
def double_enc_code2(s, key1, key2, k):
    return (f's = "{s}"\n'
            f'key1 = {key1}\n'
            f'key2 = {key2}\n'
            f'k = {k}\n'
            f'def transpose(s, key, k):\n'
            f"    r = ''\n"
            f'    for b in range(0, len(s), k):\n'
            f'        for j in key:\n'
            f'            if b + j < len(s):\n'
            f'                r += s[b + j]\n'
            f'    return r\n'
            f'print(transpose(transpose(s, key1, k), key2, k))')

s, key1, key2, k = "ABCDEFGHI", [0, 2, 1], [2, 1, 0], 3
once = enc(s, key1, k); twice = enc(once, key2, k)
add([tb("다음 코드의 실행 결과를 쓰시오."), cb(double_enc_code2(s, key1, key2, k))],
    twice,
    ["1차 전치(key1=" + str(key1) + "): " + s + " -> " + once,
     "2차 전치(key2=" + str(key2) + "): " + once + " -> " + twice,
     "정답: " + twice])

# C3. 전치 후 시저
def trans_then_caesar_code(s, key, k, shift):
    return (f's = "{s}"\n'
            f'key = {key}\n'
            f'k = {k}\n'
            f'shift = {shift}\n'
            f"t = ''\n"
            f'for b in range(0, len(s), k):\n'
            f'    for j in key:\n'
            f'        if b + j < len(s):\n'
            f'            t += s[b + j]\n'
            f"result = ''\n"
            f'for ch in t:\n'
            f'    result += chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))\n'
            f'print(result)')

s, key, k, shift = "ABCDEF", [0, 2, 1], 3, 3
t = enc(s, key, k); res = caesar(t, shift)
add([tb("다음 코드의 실행 결과를 쓰시오. (전치 후 시저 암호를 적용한다.)"),
     cb(trans_then_caesar_code(s, key, k, shift))],
    res,
    ["전치(key=" + str(key) + "): " + s + " -> " + t,
     "시저(shift=" + str(shift) + "): 각 글자를 " + str(shift) + "칸 뒤로",
     "  " + " ".join(c + "->" + caesar(c, shift) for c in t),
     "정답: " + res])

# C4. 시저 후 전치
def caesar_then_trans_code(s, shift, key, k):
    return (f's = "{s}"\n'
            f'shift = {shift}\n'
            f'key = {key}\n'
            f'k = {k}\n'
            f"c = ''\n"
            f'for ch in s:\n'
            f'    c += chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))\n'
            f"result = ''\n"
            f'for b in range(0, len(c), k):\n'
            f'    for j in key:\n'
            f'        if b + j < len(c):\n'
            f'            result += c[b + j]\n'
            f'print(result)')

s, shift, key, k = "HELLO", 2, [0, 2, 1], 3
c = caesar(s, shift); res = enc(c, key, k)
add([tb("다음 코드의 실행 결과를 쓰시오. (시저 후 전치 암호를 적용한다.)"),
     cb(caesar_then_trans_code(s, shift, key, k))],
    res,
    ["시저(shift=" + str(shift) + "): " + s + " -> " + c,
     "전치(key=" + str(key) + "): " + c + " -> " + res,
     "정답: " + res])

# C5. 전치+시저, 부분블록
s, key, k, shift = "PYTHON", [2, 0, 1], 3, 1
t = enc(s, key, k); res = caesar(t, shift)
add([tb("다음 코드의 실행 결과를 쓰시오. (전치 후 시저 암호를 적용한다.)"),
     cb(trans_then_caesar_code(s, key, k, shift))],
    res,
    ["전치(key=" + str(key) + "): " + s + " -> " + t,
     "시저(shift=" + str(shift) + "): " + t + " -> " + res,
     "정답: " + res])

# =========================================================
# D. 중간단계 추적
# =========================================================
# D1. 첫 블록 처리 직후 result
s, key, k = "ABCDEFGH", [0, 2, 1], 3
first = rearrange_block(s[0:k], key)
code_d1 = (f's = "{s}"\n'
           f'key = {key}\n'
           f'k = {k}\n'
           f"result = ''\n"
           f'for b in range(0, len(s), k):\n'
           f'    for j in key:\n'
           f'        if b + j < len(s):\n'
           f'            result += s[b + j]\n'
           f'    print(result)   # 각 블록 처리 후 출력')
all_snaps = []
acc = ''
for b in range(0, len(s), k):
    acc += rearrange_block(s[b:b+k], key)
    all_snaps.append(acc)
add([tb("다음 코드를 실행할 때 가장 먼저 출력되는 줄(첫 번째 print 결과)을 쓰시오."), cb(code_d1)],
    all_snaps[0],
    ["print는 바깥 for(블록 단위) 안에 있으므로 블록 하나를 처리할 때마다 현재까지의 result를 출력한다.",
     "첫 블록 [" + s[0:k] + "] 처리 후 result = " + all_snaps[0],
     "정답: " + all_snaps[0]])

# D2. 두 번째 블록 처리 직후 result
add([tb("위와 같은 코드(블록마다 result 출력)에서 두 번째로 출력되는 줄을 쓰시오. "
        "s=\"" + s + "\", key=" + str(key) + "."), cb(code_d1)],
    all_snaps[1],
    ["첫 블록 [" + s[0:k] + "] -> " + all_snaps[0],
     "둘째 블록 [" + s[k:2*k] + "]까지 처리 후 result = " + all_snaps[1],
     "정답: " + all_snaps[1]])

# D3. b, j 특정 값일 때 s[b+j]
s = "ABCDEFG"
add([tb("코드 result += s[b + j] 실행 중 s=\"" + s + "\" 이고 b=3, j=2 일 때 "
        "s[b + j] 가 가리키는 글자를 쓰시오.")],
    s[3+2],
    ["b + j = 3 + 2 = 5", "s[5] = " + s[5] + " (s=\"" + s + "\", 0-based)",
     "정답: " + s[5]])

# D4. 가드가 거짓이 되는 횟수
s, key, k = "ABCDEFG", [0, 2, 1], 3   # 마지막 블록 [G] 길이1, j=2,j=1 두 번 거짓
false_cnt = 0
for b in range(0, len(s), k):
    for j in key:
        if not (b + j < len(s)):
            false_cnt += 1
add([tb("다음 코드에서 조건문 if b + j < len(s) 가 거짓이 되어 글자를 건너뛰는 횟수를 쓰시오."),
     cb(enc_code(s, key, k))],
    str(false_cnt),
    ["s 길이 7, k=3 -> 블록 [ABC][DEF][G]",
     "마지막 블록 [G]는 위치 0만 유효. key=[0,2,1] 중 j=2, j=1 이 범위 밖 -> 2번 거짓",
     "정답: " + str(false_cnt)])

# D5. 마지막으로 추가되는 글자
s, key, k = "ABCDEFGH", [0, 2, 1], 3
res = enc(s, key, k)
add([tb("다음 코드에서 result에 가장 마지막으로 추가되는 글자를 쓰시오."), cb(enc_code(s, key, k))],
    res[-1],
    ["최종 result = " + res, "마지막 글자: " + res[-1],
     "(마지막 블록 [" + s[6:] + "]을 key 순서로 처리한 결과의 끝)",
     "정답: " + res[-1]])

# D6. 블록 개수
s, k = "ABCDEFGHIJ", 3
nblocks = (len(s) + k - 1) // k
add([tb("문자열 s=\"" + s + "\" 를 블록 크기 k=" + str(k) + "로 끊을 때 "
        "바깥 for b in range(0, len(s), k) 반복 횟수(블록 개수)를 쓰시오.")],
    str(nblocks),
    ["len(s)=" + str(len(s)) + ", k=" + str(k),
     "range(0, " + str(len(s)) + ", " + str(k) + ") = 0,3,6,9 -> " + str(nblocks) + "회",
     "정답: " + str(nblocks)])

# =========================================================
# E. 빈칸
# =========================================================
# E1. step 빈칸 -> k
s, key, k = "ABCDEFG", [0, 2, 1], 3
code = enc_code(s, key, k).replace("range(0, len(s), k)", "range(0, len(s), [[]])")
add([tb(BLANK), cb(code), ob(enc(s, key, k))], "k",
    ["바깥 for는 블록 시작 위치를 k 간격으로 만들어야 한다.",
     "블록 크기 = key 길이 = 3 = k", "정답: k (또는 3)"])

# E2. step 빈칸, 숫자 직접
code = enc_code(s, key, k).replace("range(0, len(s), k)", "range(0, len(s), [[]])").replace("k = 3\n", "")
add([tb(BLANK + " (숫자로 답하시오.)"), cb(code), ob(enc(s, key, k))], "3",
    ["key=[0,2,1]의 길이가 3이므로 블록을 3칸씩 끊는다.", "정답: 3"])

# E3. for j in [[]] -> key
code = enc_code(s, key, k).replace("for j in key", "for j in [[]]")
add([tb(BLANK), cb(code), ob(enc(s, key, k))], "key",
    ["안쪽 for는 블록 안에서 글자를 꺼낼 순서, 즉 key를 따라야 한다.", "정답: key"])

# E4. 가드 [[]] -> len(s)
code = enc_code(s, key, k).replace("if b + j < len(s)", "if b + j < [[]]")
add([tb(BLANK), cb(code), ob(enc(s, key, k))], "len(s)",
    ["부분 블록에서 인덱스가 문자열 끝을 넘지 않도록 막는 가드다.",
     "b + j 가 문자열 길이 len(s) 미만일 때만 유효", "정답: len(s)"])

# E5. 인덱스 s[b + [[]]] -> j
code = enc_code(s, key, k).replace("result += s[b + j]", "result += s[b + [[]]]")
add([tb(BLANK), cb(code), ob(enc(s, key, k))], "j",
    ["블록 시작 b에서 블록 내 위치 j를 더해 실제 인덱스를 만든다.", "정답: j"])

# E6. result 초기화 -> ''
code = enc_code(s, key, k).replace("result = ''", "result = [[]]")
add([tb(BLANK), cb(code), ob(enc(s, key, k))], "''",
    ["글자를 이어 붙일 빈 문자열로 초기화한다.", "정답: '' (빈 문자열)"])

# E7. 역순열 빈칸(복호화) -> i
cipher, key, k = "ACBDFE", [0, 2, 1], 3
code = dec_code(cipher, key, k).replace("inv[key[i]] = i", "inv[key[i]] = [[]]")
add([tb(BLANK), cb(code), ob(dec(cipher, key, k))], "i",
    ["역순열은 'key[i] 위치에서 온 글자는 원래 i번째' 라는 대응을 만든다.",
     "따라서 inv[key[i]] = i", "정답: i"])

# E8. 키 변환 "132" -> [0,2,1]
code = ('keystr = "132"\n'
        'key = []\n'
        'for ch in keystr:\n'
        '    key.append(int(ch) - [[]])\n'
        'print(key)')
add([tb(BLANK), cb(code), ob("[0, 2, 1]")], "1",
    ["1-based 키 문자열 \"132\"를 0-based 인덱스로 바꾸려면 각 숫자에서 1을 뺀다.",
     "1->0, 3->2, 2->1", "정답: 1"])

# =========================================================
# F. 응용 / 추론
# =========================================================
# F1. 키 추론
add([tb("전치 암호(블록 크기 3)로 \"ABC\" 를 암호화했더니 \"ACB\" 가 되었다. "
        "사용한 키 key(0-based 리스트)를 쓰시오.")],
    "[0, 2, 1]",
    ["결과 ACB의 각 글자가 원본 ABC의 몇 번째인지 본다.",
     "A=원본0, C=원본2, B=원본1 -> key=[0, 2, 1]", "정답: [0, 2, 1]"])

# F2. 원문 추론(손 복호화)
cipher, key, k = "BCAEFD", [2, 0, 1], 3
plain = dec(cipher, key, k)
add([tb("블록 크기 3, key=" + str(key) + " 로 암호화한 결과가 \"" + cipher + "\" 이다. "
        "원문을 쓰시오.")],
    plain,
    ["key=" + str(key) + " 는 블록을 (원본0->2번째, 원본1->0번째, 원본2->1번째)로 보낸다.",
     "역으로 풀면 역순열 inv=" + str(inv_key(key)),
     "암호문 " + cipher + " 를 inv로 재배열 -> " + plain, "정답: " + plain])

# F3. 위치 매핑
s, key, k = "ABCDEFG", [0, 2, 1], 3
res = enc(s, key, k)
pos = res.index(s[1])  # 원문 1번(B)이 암호문 어디로?
add([tb("s=\"" + s + "\", key=" + str(key) + " 로 전치 암호화할 때 "
        "원문의 1번 글자(B)는 암호문에서 몇 번째 위치(0-based)로 가는가?")],
    str(pos),
    ["첫 블록 [ABC]를 key=[0,2,1] 순서로 -> A(0)C(2)B(1) = ACB",
     "B는 블록 안에서 마지막에 출력 -> 암호문 인덱스 " + str(pos),
     "정답: " + str(pos)])

# F4. 항등 키
add([tb("블록 크기 3인 전치 암호에서 암호문이 원문과 항상 같아지는 키 key(0-based 리스트)를 쓰시오.")],
    "[0, 1, 2]",
    ["글자 순서를 바꾸지 않는 키, 즉 위치를 그대로 두는 항등 순열이어야 한다.",
     "정답: [0, 1, 2]"])

# F5. 암호문 길이
s, key, k = "ABCDEFG", [0, 2, 1], 3
add([tb("전치 암호는 글자를 바꾸지 않고 순서만 재배열한다. "
        "s=\"" + s + "\"(길이 7)을 암호화한 결과의 길이를 쓰시오.")],
    str(len(s)),
    ["전치 암호는 글자를 더하거나 빼지 않으므로 길이가 보존된다.",
     "정답: " + str(len(s))])

# ----- 저장 -----
with open(os.path.normpath(OUT), "w", encoding="utf-8") as f:
    json.dump(PROBLEMS, f, ensure_ascii=False, indent=2)

print("총 문제 수:", len(PROBLEMS))
print("id 범위: fb-204 ~ fb-" + str(203 + len(PROBLEMS)))
# 카테고리별 개수
print("A 암호화추적:", len(enc_cases))
print("B 복호화추적:", len(dec_cases))
print("저장:", os.path.normpath(OUT))
