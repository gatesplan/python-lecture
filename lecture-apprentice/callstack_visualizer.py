"""
재귀 함수의 콜스택을 시각화하는 데코레이터
"""
import sys
from io import StringIO
from functools import wraps


class CallStackVisualizer:
    def __init__(self):
        self.depth = 0
        self.original_stdout = sys.stdout

    def get_indent(self):
        """현재 깊이에 맞는 들여쓰기 문자열 반환"""
        return "|   " * self.depth

    def visualize(self, func):
        """재귀 함수를 시각화하는 데코레이터"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 함수 호출 시작
            indent = self.get_indent()

            # 함수명과 파라미터 출력
            args_str = ", ".join(repr(arg) for arg in args)
            if kwargs:
                kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
                params = f"{args_str}, {kwargs_str}" if args_str else kwargs_str
            else:
                params = args_str

            print(f"{indent}{func.__name__}({params})", file=self.original_stdout)

            # 깊이 증가
            self.depth += 1

            # stdout 리다이렉션 설정
            original_stdout = sys.stdout
            captured_output = StringIO()

            class IndentedStdout:
                def __init__(self, original, depth_getter):
                    self.original = original
                    self.depth_getter = depth_getter
                    self.buffer = []  # 한 줄씩 모으기 위한 버퍼

                def write(self, text):
                    if not text:
                        return

                    # 개행 문자가 나올 때까지 버퍼에 모음
                    if '\n' in text:
                        parts = text.split('\n')
                        # 마지막 부분 전까지 처리
                        for i, part in enumerate(parts[:-1]):
                            self.buffer.append(part)
                            line = ''.join(self.buffer)
                            if line:  # 빈 줄이 아닌 경우만
                                indent = "|   " * self.depth_getter()
                                self.original.write(f'{indent}"{line}"\n')
                            self.buffer = []
                        # 마지막 부분은 버퍼에 보관
                        if parts[-1]:
                            self.buffer.append(parts[-1])
                    else:
                        self.buffer.append(text)

                def flush(self):
                    # 버퍼에 남아있는 내용 출력
                    if self.buffer:
                        line = ''.join(self.buffer)
                        if line:
                            indent = "|   " * self.depth_getter()
                            self.original.write(f'{indent}"{line}"\n')
                        self.buffer = []
                    self.original.flush()

            sys.stdout = IndentedStdout(self.original_stdout, lambda: self.depth)

            try:
                # 원본 함수 실행
                result = func(*args, **kwargs)
            finally:
                # stdout 복원
                sys.stdout = original_stdout

                # 깊이 감소
                self.depth -= 1

                # 반환값 출력 (None이 아닌 경우만)
                if result is not None:
                    indent = self.get_indent()
                    print(f"{indent}returned {result!r}", file=self.original_stdout)

            return result

        return wrapper


# 전역 visualizer 인스턴스
_visualizer = CallStackVisualizer()

def visualize_callstack(func):
    """
    재귀 함수의 콜스택을 시각화하는 데코레이터

    사용법:
        @visualize_callstack
        def f(n, s, t, w):
            if n >= 1:
                f(n-1, s, w, t)
                print(n, s, t)
                f(n-1, w, t, s)

        f(3, 'A', 'C', 'B')
    """
    return _visualizer.visualize(func)
