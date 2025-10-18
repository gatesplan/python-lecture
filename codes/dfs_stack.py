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


def dfs_iterative(graph, start):
    visited = set()
    path = []
    stack = Stack()
    
    stack.push(start)
    
    while not stack.is_empty():
        current = stack.pop()
        
        if current in visited:
            continue
        
        visited.add(current)
        path.append(current)
        
        for neighbor in reversed(graph[current]):
            if neighbor not in visited:
                stack.push(neighbor)
    
    return path


graph = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4],
    4: [1, 3, 5],
    5: [2, 4]
}

print(dfs_iterative(graph, 0))
print(dfs_iterative(graph, 2))
print(dfs_iterative(graph, 5))