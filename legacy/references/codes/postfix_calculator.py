class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)


def evaluate_postfix(postfix):
    stack = Stack()
    tokens = postfix.split()
    
    for token in tokens:
        if token.replace('.', '').replace('-', '').isdigit():
            stack.push(float(token))
        elif token in ['+', '-', '*', '/']:
            if stack.size() < 2:
                raise ValueError("Invalid expression")
            
            right = stack.pop()
            left = stack.pop()
            
            if token == '+':
                result = left + right
            elif token == '-':
                result = left - right
            elif token == '*':
                result = left * right
            elif token == '/':
                if right == 0:
                    raise ValueError("Division by zero")
                result = left / right
            
            stack.push(result)
    
    if stack.size() != 1:
        raise ValueError("Invalid expression")
    
    return stack.pop()


print(evaluate_postfix("2 3 4 * +"))
print(evaluate_postfix("2 3 + 4 *"))
print(evaluate_postfix("5 2 - 3 * 4 +"))
print(evaluate_postfix("15 7 1 1 + - * 3 /"))