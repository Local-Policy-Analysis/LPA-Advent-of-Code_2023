import numpy as np
import heapq

def print_grid(grid):
    for g in grid:
        print(''.join(g))
    print('\n')

with open('input_jac.txt') as f:
    data = [[int(_) for _ in d.strip().split(',')] for d in f.readlines()]
    
dim = 71
byte_limit = 1024
grid = np.full((dim, dim), '.')

for byte in data[:byte_limit]:
    y, x = byte
    grid[x, y] = '#'
    
moves = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    
def find_neighbours(x, y):
    neighbours = []
    for m in moves.keys():
        dx, dy = moves[m]
        if 0 <= x + dx < dim and 0 <= y + dy < dim:
            if grid[x + dx, y + dy] == '.':
                neighbours.append((x + dx, y + dy))
    return neighbours

def update_tentative(neighbours, candidate, tentative):
    candidate_cost, candidate_x, candidate_y = candidate
    for n in neighbours:
        cost = tentative[(candidate_x, candidate_y)] + 1
        if n in tentative and cost >= tentative[n]:
            continue
        yield n, cost

def find_cheapest_path():
    candidates = [(0, 0, 0)]
    tentative = {(0, 0): 0}
    visited = set()
    while ((dim - 1, dim - 1) not in visited and len(candidates) > 0):
        candidate = heapq.heappop(candidates)
        candidate_cost, candidate_x, candidate_y = candidate
        if candidate in visited:
            continue
        visited.add(candidate)
        neighbours = find_neighbours(candidate_x, candidate_y)
        updates = update_tentative(neighbours, candidate, tentative)
        for update in updates:
            u, c = update
            ux, uy = u
            tentative[u] = c
            heapq.heappush(candidates, (c, ux, uy))
    if (dim - 1, dim - 1) in tentative:
        return tentative[(dim - 1, dim - 1)]
    else:
        return False
 
cost = find_cheapest_path() 
print(cost)

for byte in data[byte_limit:]:
    y, x = byte
    grid[x, y] = '#'
    c = find_cheapest_path()
    if not c:
        print(f'{y},{x}')
        break
    