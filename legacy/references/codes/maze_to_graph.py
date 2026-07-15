def maze_to_graph(maze):
    rows, cols = len(maze), len(maze[0])
    graph = {}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 0:
                pos = (i, j)
                graph[pos] = []
                
                for dr, dc in directions:
                    new_row, new_col = i + dr, j + dc
                    if (0 <= new_row < rows and 0 <= new_col < cols and 
                        maze[new_row][new_col] == 0):
                        graph[pos].append((new_row, new_col))
    
    return graph


maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

graph = maze_to_graph(maze)
for pos, neighbors in graph.items():
    print(f"{pos}: {neighbors}")