class Student:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def avg(self):
        return sum(self.scores) / len(self.scores)      # 1. 평균 점수 계산 구현 문제

    def grade(self):
        avg = self.avg()                                # 2. 학점 계산 구현 문제
        if avg >= 90:
            return 'A'
        elif avg > 80:
            return 'B'
        elif avg > 70:
            return 'C'
        elif avg > 60:
            return 'D'
        elif avg > 50:
            return 'E'
        else:
            return 'F'

student1 = Student('홍길동', [90, 75, 80])
print(f"{student1.name}의 평균 점수는 {student1.avg():.2f}이고, 등급은 {student1.grade()}입니다.")
# 3. 출력제어 형식 문제 - 소수점 2자리까지 나오도록 {} 내부를 올바르게 채우기
# 4. print() 출력 형식 문제 - P의 평균 점수는 Q(소수점2자리까지)이고, 등급은 R입니다. 형식으로 출력되도록 print 채우는 문항
