class EightPuzzle:
    def __init__(self, numbers):
        self.numbers = numbers

    def display(self):
        for i in range(3):
            for j in range(3):
                print(self.numbers[3*i + j], end=' ')  # 1. 이 라인 비워놓고 완성하기 (출력예시로 3x3 숫자판 제시)
            print()
        print()

    def find_zero(self):
        for i in range(3):
            for j in range(3):
                if self.numbers[3*i + j] == 0:
                    return i*3 + j
        print("Zero not found")

    def move_up(self):
        pos = self.find_zero()
        if pos > 2:
            self.numbers[pos], self.numbers[pos-3] = self.numbers[pos-3], self.numbers[pos]
        else:
            print("Cannot move up")
        self.display()

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

# 2. 나머지 메서드들 (move_down, left, right) 을 모두 완성하도록 하는 문제