class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self):
        return len(self.items) == 0


def sort_stack(stack):
    temp_stack = Stack()
    
    while not stack.is_empty():
        temp = stack.pop()
        
        while not temp_stack.is_empty() and temp_stack.peek() > temp:
            stack.push(temp_stack.pop())
        
        temp_stack.push(temp)
    
    while not temp_stack.is_empty():
        stack.push(temp_stack.pop())


stack = Stack()
for num in [5, 2, 8, 1, 9, 3]:
    stack.push(num)

print("Before:", stack.items)
sort_stack(stack)
print("After:", stack.items)