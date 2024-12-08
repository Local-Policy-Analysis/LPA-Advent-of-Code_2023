import numpy as np

with open('input_jac.txt') as f:
    data = np.array([[list(r) for r in d.strip()] for d in f.readlines()])[:, :, 0]
    
x_start, y_start = np.nonzero(data == '^')
x_start = x_start[0]
y_start = y_start[0]

change_direction = {'up': 'right',
                    'right': 'down',
                    'down': 'left',
                    'left': 'up'}
steps = {'up': (-1, 0),
         'down': (1, 0),
         'left': (0, -1),
         'right': (0, 1)}

x = x_start
y = y_start
obstacles = set()
temp_data = data.copy()
direction = 'up'
while x < temp_data.shape[0] and x >= 0 and y < temp_data.shape[1] and y >= 0:
    if temp_data[x, y] == '#':
        x -= steps[direction][0]
        y -= steps[direction][1]
        direction = change_direction[direction]
    else:
        obstacles.add((x, y))
        x += steps[direction][0]
        y += steps[direction][1]

print(len(obstacles))

pt2 = 0
for o in obstacles:
    x = x_start
    y = y_start
    direction = 'up'
    visited = set()
    temp_data = data.copy()
    temp_data[o] = '#'
    while x < temp_data.shape[0] and x >= 0 and y < temp_data.shape[1] and y >= 0:
        if (x, y, direction) in visited:
            pt2 += 1
            break
        if temp_data[x, y] == '#':
            x -= steps[direction][0]
            y -= steps[direction][1]
            direction = change_direction[direction]
        else:
            visited.add((x, y, direction))
            x += steps[direction][0]
            y += steps[direction][1]
            
print(pt2)
