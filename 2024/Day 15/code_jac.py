import numpy as np

with open('input_jac.txt') as f:
    grid, directions = f.read().split('\n\n')
    
narrow_grid = np.array([list(g) for g in grid.split('\n')])
directions = directions.replace('\n', '')

# construct grid for part 2
wider_grid = np.array(list(''.join([col * 2 if col in ['#', '.', '@'] else '[]' for row in narrow_grid for col in row]))).reshape((narrow_grid.shape[0], narrow_grid.shape[1] * 2))
wider_grid[np.nonzero(wider_grid == '@')[0][1], np.nonzero(wider_grid == '@')[1][1]] = '.'

moves = {'^': (-1, 0),
         'v': (1, 0),
         '<': (0, -1),
         '>': (0, 1)}

rx, ry = np.nonzero(wider_grid == '@')[0][0], np.nonzero(wider_grid == '@')[1][0]

def print_grid(grid):
    for g in grid:
        print(''.join(g))
    print('\n')
    
def move_into_space(x, y, dx, dy, grid):
    grid[x, y] = '.'
    grid[x + dx, y + dy] = '@'
    
def push_horizontally(x, y, dx, dy, grid):
    counter = 0
    i = y + dy
    space = False
    while not space:
        if grid[x, i] in '[]':
            counter += 1
        elif grid[x, i] == '#':
            return grid
        elif grid[x, i] == '.':
            space = True
        i += dy
    if dy > 0:
        new_col = ['[', ']'] * (counter // 2)
        for n in range(counter):
            grid[x, y + 2 + n] = new_col.pop(0)
    else:
        new_col = [']', '['] * (counter // 2)
        for n in range(counter):
            grid[x, y - 2 - n] = new_col.pop(0)
    grid[x, y] = '.'
    grid[x, y + dy] = '@'
    return grid

def push_vertically(x, y, dx, dy, grid):
    unblocked_cols = set()
    heights = {k: 0 for k in range(grid.shape[1])}
    starts = {y: x + dx}
    if grid[x + dx, y] == '[':
        starts[y + 1] = x + dx
        obstructed_cols = set([y, y + 1])
    elif grid[x + dx, y] == ']':
        starts[y - 1] = x + dx
        obstructed_cols = set([y, y - 1])
    i = x + dx
    while True:
        if not obstructed_cols:
            for col in list(unblocked_cols):
                new_col = ['.']
                if dx > 0:
                    for h in range(starts[col], heights[col] + 1):
                        new_col.append(grid[h, col])
                else:
                    for h in range(starts[col], heights[col] - 1, -1):
                        new_col.append(grid[h, col])
                if dx > 0:
                    for h in range(starts[col], heights[col] + 2):
                        grid[h, col] = new_col.pop(0)
                else:
                    for h in range(starts[col], heights[col] - 2, -1):
                        grid[h, col] = new_col.pop(0)
            # reposition robot
            grid[x, y] = '.'
            grid[x + dx, y] = '@'
            return grid
        else:
            for col in list(obstructed_cols):
                if grid[i, col] == '[':
                    obstructed_cols.add(col + 1)
                    if col not in starts:
                        starts[col] = i
                    if col + 1 not in starts:
                        starts[col + 1] = i
                    heights[col + 1] = i
                    heights[col] = i
                elif grid[i, col] == ']':
                    obstructed_cols.add(col - 1)
                    if col not in starts:
                        starts[col] = i
                    if col - 1 not in starts:
                        starts[col - 1] = i
                    heights[col - 1] = i
                    heights[col] = i
                elif grid[i, col] == '.':
                    obstructed_cols.remove(col)
                    unblocked_cols.add(col)
                elif grid[i, col] == '#':
                    return grid
        i += dx

# print_grid(wider_grid)
for d in directions:
    dx, dy = moves[d]
    if wider_grid[rx + dx, ry + dy] == '.':
        move_into_space(rx, ry, dx, dy, wider_grid)
    elif wider_grid[rx + dx, ry + dy] in '[]' and d in '<>':
        wider_grid = push_horizontally(rx, ry, dx, dy, wider_grid)
    elif wider_grid[rx + dx, ry + dy] in '[]' and d in 'v^':
        wider_grid = push_vertically(rx, ry, dx, dy, wider_grid)
    rx, ry = np.nonzero(wider_grid == '@')[0][0], np.nonzero(wider_grid == '@')[1][0]
    # print_grid(wider_grid)
    
pt2 = 0
blocks = np.nonzero(wider_grid == '[')
for b in blocks[0]:
    pt2 += b * 100
for b in blocks[1]:
    pt2 += b
    
print(pt2)