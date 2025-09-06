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


def infix_to_postfix(infix):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    stack = Stack()
    output = []
    tokens = infix.split()
    
    for token in tokens:
        if token.isalnum():
            output.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                output.append(stack.pop())
            if not stack.is_empty():
                stack.pop()
        elif token in precedence:
            while (not stack.is_empty() and 
                   stack.peek() != '(' and
                   stack.peek() in precedence and
                   precedence[stack.peek()] >= precedence[token]):
                output.append(stack.pop())
            stack.push(token)
    
    while not stack.is_empty():
        output.append(stack.pop())
    
    return ' '.join(output)


print(infix_to_postfix("2 + 3 * 4"))
print(infix_to_postfix("( 2 + 3 ) * 4"))
print(infix_to_postfix("A + B * C - D"))
print(infix_to_postfix("( A + B ) * ( C - D )"))