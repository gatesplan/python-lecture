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


def decimal_to_binary(num):
    stack = Stack()
    
    if num == 0:
        return "0"
    
    while num > 0:
        remainder = num % 2
        stack.push(remainder)
        num = num // 2
    
    binary = ""
    while not stack.is_empty():
        binary += str(stack.pop())
    
    return binary


print(decimal_to_binary(10))
print(decimal_to_binary(25))
print(decimal_to_binary(0))
print(decimal_to_binary(255))