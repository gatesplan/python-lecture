import math         # 1. 올바른 라이브러리 임포트 채우기 문제

class Distance:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def distance(self):
        return math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
    # 2. distance() 메서드 - 거리 나오도록 구현하기 문제

distance1 = Distance(2, 3, 3, 5)
print(f"두 점 사이의 거리는 {distance1.distance():.2f}")
# 3. Distance 클래스 사용해서 (2,3), (3,5), (5,6), (-1, 2) 점들 사이의 거리를 모두 구하여
# 그 중 가장 먼 거리를 소수점 2자리로 출력하는 함수를 작성하는 문제