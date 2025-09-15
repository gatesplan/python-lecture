class Movie:
    def __init__(self, name, seat):
        self.name = name
        self.total_seats = seat

    def reserve(self):
        if self.total_seats > 0:
            self.total_seats -= 1
            return True
        else:
            return False

seat1 = Movie('ET', 5)
result = seat1.reserve()
print('예약 성공' if result else '예약 실패')
