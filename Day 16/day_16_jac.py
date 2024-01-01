import os
import numpy as np
import time

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 16')

with open('input_jac.txt') as f:
    data = [list(d.strip()) for d in f.readlines()]
    
visited = set()
def count_energy(coords, direction):
    result = []
    x, y = coords
    while x >= 0 and x < len(data) and y >= 0 and y < len(data[0]):
        state = (x, y, direction)
        if state in visited:
            return True
        else:
            visited.add(state)
        result = result + [(x, y)]
        cell = data[x][y]
        if cell == '-' and direction in ['up', 'down']:
            state = (x, y - 1, 'left')
            if state not in visited:
                count_energy((x, y - 1), 'left')
            state = (x, y + 1, 'right')
            if state not in visited:
                count_energy((x, y + 1), 'right')
            return True
        elif cell == '|' and direction in ['left', 'right']:
            state = (x + 1, y, 'down')
            if state not in visited:
                count_energy((x + 1, y), 'down')
            state = (x - 1, y, 'up')
            if state not in visited:
                count_energy((x - 1, y), 'up')
            return True
        elif cell == '\\' and direction == 'up':
            direction = 'left'
        elif cell == '\\' and direction == 'down':
            direction = 'right'
        elif cell == '\\' and direction == 'left':
            direction = 'up'
        elif cell == '\\' and direction == 'right':
            direction = 'down'
        elif cell == '/' and direction == 'up':
            direction = 'right'
        elif cell == '/' and direction == 'down':
            direction = 'left'
        elif cell == '/' and direction == 'left':
            direction = 'down'
        elif cell == '/' and direction == 'right':
            direction = 'up'
        adjacency_matrix = {'up': (-1, 0),
                            'down': (1, 0),
                            'left': (0, -1),
                            'right': (0, 1)}
        x = x + adjacency_matrix[direction][0]
        y = y + adjacency_matrix[direction][1]
    return True

_ = count_energy((0, 0), 'right')
energised = set([(v[0], v[1]) for v in sorted(visited)])
print(len(energised))

scores = []
for r, row in enumerate(data):
    visited = set()
    _ = count_energy((r, 0), 'right')
    energised = len(set([(v[0], v[1]) for v in sorted(visited)]))
    scores.append(energised)
    visited = set()
    _ = count_energy((r, len(data[0]) - 1), 'left')
    energised = len(set([(v[0], v[1]) for v in sorted(visited)]))
    scores.append(energised)
for c, col in enumerate(data[0]):
    visited = set()
    _ = count_energy((0, c), 'down')
    energised = len(set([(v[0], v[1]) for v in sorted(visited)]))
    scores.append(energised)
    visited = set()
    _ = count_energy((len(data) - 1, c), 'up')
    energised = len(set([(v[0], v[1]) for v in sorted(visited)]))
    scores.append(energised)
    
print(max(scores))