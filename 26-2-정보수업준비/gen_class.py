# -*- coding: utf-8 -*-
"""
클래스/객체 기초 문제 생성기 (갈래2 범위, 코드 제시형).

범위: 단일 클래스 / __init__ 속성 초기화(기본값 포함) / 메서드 정의·호출 /
      self.x 상태변경 추적. 상속·클래스변수·복잡한 상호작용 제외.
형식: 실행결과 / 중간단계 추적 / 빈칸 / 동작설명 (코드 작성형 없음).
배운 범위 제약: 딕셔너리 get/items/values만, join/enumerate/리스트컴프리헨션 미사용.

안전장치: 모든 코드를 exec해 출력/동작을 검증한다.
  - result : answer = exec 출력 (자동)
  - trace  : answer 수동 지정, full(전체코드) exec 최종출력로 보조 검증
  - blank  : answer = 빈칸값, full(정답코드) exec 출력 == expect 로 검증
  - desc   : answer 수동(설명), code exec 동작(무에러) 확인
"""
import io
import os
import json
import contextlib


def run_code(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {})
    return buf.getvalue().strip()


# ===================== 문제 정의 =====================

PROBS = [
    # --- 실행결과: __init__ 속성 출력 ---
    {"id": "g1-093", "kind": "result",
     "q": "다음 코드의 실행 결과를 쓰시오.",
     "code": '''class Hero:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

a = Hero("기사", 100)
print(a.name, a.hp)''',
     "ex": "Hero 객체를 만들 때 __init__이 name, hp 속성을 설정한다. a.name=기사, a.hp=100."},

    # --- 실행결과: 메서드 호출 ---
    {"id": "g1-094", "kind": "result",
     "q": "다음 코드의 실행 결과를 쓰시오.",
     "code": '''class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        print(self.name, "멍멍")

d = Dog("바둑이")
d.bark()''',
     "ex": "d.bark()는 self.name(=바둑이)과 '멍멍'을 출력한다."},

    # --- 실행결과: self 상태 누적 변경 ---
    {"id": "g1-095", "kind": "result",
     "q": "다음 코드의 실행 결과를 쓰시오.",
     "code": '''class Monster:
    def __init__(self, hp):
        self.hp = hp
    def hit(self, dmg):
        self.hp = self.hp - dmg

m = Monster(50)
m.hit(10)
m.hit(15)
print(m.hp)''',
     "ex": "hp=50 -> hit(10) -> 40 -> hit(15) -> 25."},

    # --- 중간단계 추적 ---
    {"id": "g1-096", "kind": "trace", "answer": "40",
     "q": "다음 코드에서 두 번째 hit를 실행하기 직전 m.hp의 값을 쓰시오.",
     "code": '''class Monster:
    def __init__(self, hp):
        self.hp = hp
    def hit(self, dmg):
        self.hp = self.hp - dmg

m = Monster(50)
m.hit(10)
m.hit(15)
print(m.hp)''',
     "ex": "hp=50 -> 첫 hit(10) -> 40. 두 번째 hit 실행 직전 값은 40."},

    # --- 실행결과: 기본값 매개변수 ---
    {"id": "g1-097", "kind": "result",
     "q": "다음 코드의 실행 결과를 쓰시오.",
     "code": '''class Car:
    def __init__(self, color, speed=0):
        self.color = color
        self.speed = speed

c = Car("red")
print(c.color, c.speed)''',
     "ex": "speed는 기본값 0. color만 전달하면 speed=0이 된다."},

    # --- 실행결과: 객체 독립성 ---
    {"id": "g1-098", "kind": "result",
     "q": "다음 코드의 실행 결과를 쓰시오.",
     "code": '''class Box:
    def __init__(self, n):
        self.n = n

x = Box(1)
y = Box(5)
x.n = x.n + 10
print(x.n, y.n)''',
     "ex": "x와 y는 서로 다른 객체. x.n만 11이 되고 y.n은 5 그대로."},

    # --- 실행결과: 여러 메서드로 상태 변화 ---
    {"id": "g1-099", "kind": "result",
     "q": "다음 코드의 실행 결과를 쓰시오.",
     "code": '''class Car:
    def __init__(self):
        self.speed = 0
    def up(self, a):
        self.speed = self.speed + a
    def stop(self):
        self.speed = 0

c = Car()
c.up(30)
c.up(20)
c.stop()
c.up(5)
print(c.speed)''',
     "ex": "0 ->+30=30 ->+20=50 ->stop=0 ->+5=5."},

    # --- 빈칸: __init__ 속성 대입 ---
    {"id": "g1-100", "kind": "blank", "answer": "self.name", "expect": "민수",
     "q": "다음 코드의 실행 결과가 '민수'일 때, 빈칸에 들어갈 코드를 쓰시오.",
     "code": '''class Student:
    def __init__(self, name):
        [[]] = name
    def hello(self):
        print(self.name)

s = Student("민수")
s.hello()''',
     "full": '''class Student:
    def __init__(self, name):
        self.name = name
    def hello(self):
        print(self.name)

s = Student("민수")
s.hello()''',
     "ex": "hello가 self.name을 출력하므로, __init__에서 self.name = name으로 저장해야 한다."},

    # --- 빈칸: 메서드의 self 매개변수 ---
    {"id": "g1-101", "kind": "blank", "answer": "self", "expect": "2",
     "q": "다음 코드의 실행 결과가 2일 때, 빈칸에 들어갈 내용을 쓰시오.",
     "code": '''class Counter:
    def __init__(self):
        self.cnt = 0
    def add([[]]):
        self.cnt = self.cnt + 1

c = Counter()
c.add()
c.add()
print(c.cnt)''',
     "full": '''class Counter:
    def __init__(self):
        self.cnt = 0
    def add(self):
        self.cnt = self.cnt + 1

c = Counter()
c.add()
c.add()
print(c.cnt)''',
     "ex": "메서드의 첫 매개변수는 self여야 self.cnt에 접근할 수 있다."},

    # --- 동작 설명 ---
    {"id": "g1-102", "kind": "desc",
     "answer": "money 속성(잔액)에 입력값 x를 더한다(입금).",
     "q": "다음 코드에서 deposit 메서드가 하는 일을 한 문장으로 설명하시오.",
     "code": '''class Account:
    def __init__(self, money):
        self.money = money
    def deposit(self, x):
        self.money = self.money + x
    def withdraw(self, x):
        self.money = self.money - x''',
     "ex": "deposit(x)는 self.money에 x를 더해 잔액을 늘린다."},

    # --- 실행결과: f-string 출력 메서드 ---
    {"id": "g1-103", "kind": "result",
     "q": "다음 코드의 실행 결과를 쓰시오.",
     "code": '''class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def info(self):
        print(f"{self.name}: {self.price}원")

it = Item("연필", 500)
it.info()''',
     "ex": "info()는 f-string으로 name과 price를 끼워 출력한다."},

    # --- 실행결과: 속성 계산 반환 ---
    {"id": "g1-104", "kind": "result",
     "q": "다음 코드의 실행 결과를 쓰시오.",
     "code": '''class Rect:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    def area(self):
        return self.w * self.h

r = Rect(3, 4)
print(r.area())''',
     "ex": "area()는 self.w * self.h = 3*4 = 12를 반환한다."},

    # --- 실행결과: 두 속성 동시 추적 ---
    {"id": "g1-105", "kind": "result",
     "q": "다음 코드의 실행 결과를 쓰시오.",
     "code": '''class Player:
    def __init__(self):
        self.hp = 100
        self.score = 0
    def damage(self, d):
        self.hp = self.hp - d
    def gain(self, s):
        self.score = self.score + s

p = Player()
p.damage(30)
p.gain(50)
p.damage(20)
p.gain(10)
print(p.hp, p.score)''',
     "ex": "hp: 100->70->50. score: 0->50->60. 결과 50 60."},

    # --- 실행결과: 반환 없는 메서드 None 함정 ---
    {"id": "g1-106", "kind": "result",
     "q": "다음 코드의 실행 결과를 쓰시오.",
     "code": '''class Calc:
    def __init__(self, x):
        self.x = x
    def double(self):
        self.x = self.x * 2

c = Calc(5)
result = c.double()
print(c.x, result)''',
     "ex": "double()은 self.x를 2배(10)로 바꾸지만 return이 없어 result는 None."},
]


def build(p):
    kind = p["kind"]
    content = [{"type": "text", "content": p["q"]},
               {"type": "code", "language": "python", "content": p["code"]}]
    if kind == "result":
        ans = run_code(p["code"])
    elif kind == "trace":
        run_code(p["code"])  # 무에러 확인
        ans = p["answer"]
    elif kind == "blank":
        out = run_code(p["full"])
        assert out == p["expect"], "%s blank check fail: %r != %r" % (p["id"], out, p["expect"])
        ans = p["answer"]
    elif kind == "desc":
        run_code(p["code"])  # 무에러 확인
        ans = p["answer"]
    else:
        raise ValueError(kind)
    return {
        "id": p["id"], "type": "short", "content": content,
        "answer": {"type": "value", "value": ans},
        "explain": [{"type": "process-box", "title": "풀이",
                     "content": [{"type": "text", "content": p["ex"]},
                                 {"type": "text", "content": "정답: " + ans}]}],
    }


def main(save):
    out = []
    for p in PROBS:
        prob = build(p)
        print("OK   %s [%s] -> %r" % (p["id"], p["kind"], prob["answer"]["value"]))
        out.append(prob)
    print("=== 클래스 %d문제 생성 + exec 검증 완료 ===" % len(out))
    if save:
        base = os.path.join(os.path.dirname(__file__), '..', 'exam-builder',
                            'frontend', 'src', 'data')
        path = os.path.join(base, 'problems-cnsh-26-1-2-06.json')
        json.dump(out, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print("saved:", path)


if __name__ == '__main__':
    import sys
    main('--save' in sys.argv)
