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


def is_valid_brackets(s):
    stack = Stack()
    pairs = {'(': ')', '[': ']', '{': '}'}
    
    for char in s:
        if char in pairs:
            stack.push(char)
        elif char in pairs.values():
            if stack.is_empty():
                return False
            if pairs[stack.pop()] != char:
                return False
    
    return stack.is_empty()


print(is_valid_brackets("()"))
print(is_valid_brackets("([{}])"))
print(is_valid_brackets("([)]"))
print(is_valid_brackets("((("))