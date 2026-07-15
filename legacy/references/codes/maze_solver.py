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


def solve_maze(maze):
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    stack = Stack()
    
    start_path = [(0, 0)]
    stack.push(start_path)
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while not stack.is_empty():
        path = stack.pop()
        row, col = path[-1]
        
        if visited[row][col]:
            continue
        
        visited[row][col] = True
        
        if row == rows - 1 and col == cols - 1:
            return path
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < rows
                    and 0 <= new_col < cols
                    and maze[new_row][new_col] == 0
                    and not visited[new_row][new_col]):
                new_path = path + [(new_row, new_col)]
                stack.push(new_path)
    
    return []


maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

result = solve_maze(maze)
print("Path found:" if result else "No path found")
for pos in result:
    print(pos)