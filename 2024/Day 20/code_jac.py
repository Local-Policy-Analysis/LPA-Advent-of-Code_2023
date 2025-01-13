import numpy as np
import heapq

with open('input_jac.txt') as f:
    grid = np.array([list(d.strip()) for d in f.readlines()])
    
start_x = np.nonzero(grid == 'S')[0][0]
start_y = np.nonzero(grid == 'S')[1][0]
end_x = np.nonzero(grid == 'E')[0][0]
end_y = np.nonzero(grid == 'E')[1][0]

moves = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

def print_grid(grid):
    for g in grid:
        print(''.join(g))
    print('\n')
    
def find_neighbours(x, y, grid):
    neighbours = []
    for m in moves.keys():
        dx, dy = moves[m]
        if 0 <= x + dx < grid.shape[0] and 0 <= y + dy < grid.shape[1]:
            if grid[x + dx, y + dy] in ['.', 'E']:
                neighbours.append((x + dx, y + dy))
    return neighbours

def update_tentative(neighbours, candidate, tentative):
    candidate_cost, candidate_x, candidate_y = candidate
    for n in neighbours:
        cost = tentative[(candidate_x, candidate_y)] + 1
        if n in tentative and cost >= tentative[n]:
            continue
        yield n, cost

def find_cheapest_path(grid):
    candidates = [(0, start_x, start_y)]
    tentative = {(start_x, start_y): 0}
    visited = set()
    while len(candidates) > 0:
        candidate = heapq.heappop(candidates)
        candidate_cost, candidate_x, candidate_y = candidate
        if candidate in visited:
            continue
        visited.add(candidate)
        neighbours = find_neighbours(candidate_x, candidate_y, grid)
        updates = update_tentative(neighbours, candidate, tentative)
        for update in updates:
            u, c = update
            ux, uy = u
            tentative[u] = c
            heapq.heappush(candidates, (c, ux, uy))
    if (end_x, end_y) in tentative:
        return tentative[(end_x, end_y)], tentative
    else:
        return False, tentative
    
def get_cheat():
    return 1, 1
    
base_cost, t = find_cheapest_path(grid)
saving = 100
blockages = [(x, y) for x, y in zip(np.nonzero(grid=='#')[0], np.nonzero(grid=='#')[1])]

cheats = {}
for block in blockages:
    x, y = block
    if 0 < x < grid.shape[0] - 1:
        if grid[x - 1, y] != '#' and grid[x + 1, y] != '#':
            if max(t[(x - 1, y)], t[x + 1, y]) - min(t[(x - 1, y)], t[x + 1, y]) - 2 in cheats:
                cheats[max(t[(x - 1, y)], t[x + 1, y]) - min(t[(x - 1, y)], t[x + 1, y]) - 2] += 1
            else:
                cheats[max(t[(x - 1, y)], t[x + 1, y]) - min(t[(x - 1, y)], t[x + 1, y]) - 2] = 1
    if 0 < y < grid.shape[1] - 1:
        if grid[x, y - 1] != '#' and grid[x, y + 1] != '#':
            if max(t[(x, y - 1)], t[x, y + 1]) - min(t[(x, y - 1)], t[x, y + 1]) - 2 in cheats:
                cheats[max(t[(x, y - 1)], t[x, y + 1]) - min(t[(x, y - 1)], t[x, y + 1]) - 2] += 1
            else:
                cheats[max(t[(x, y - 1)], t[x, y + 1]) - min(t[(x, y - 1)], t[x, y + 1]) - 2] = 1
     
print(sum([cheats[x] for x in cheats.keys() if x >= saving]))

cheat_length = 21
cheats2 = {}
visited = set()       
for x in range(grid.shape[0]):
    for y in range(grid.shape[1]):
        if grid[x, y] != '#':
            for i in range(cheat_length):
                for j in range(cheat_length - i):
                    if x + i < grid.shape[0] and y + j < grid.shape[1]:
                        route = sorted([(x, y), (x + i, y + j)], key=lambda x: (x[0], x[1]))
                        route = tuple([x for xs in route for x in xs])
                        if grid[x + i, y + j] != '#':
                            if abs(t[x, y] - t[x + i, y + j]) - i - j in cheats2:
                                if route not in visited:
                                    cheats2[abs(t[x, y] - t[x + i, y + j]) - i - j] += 1
                                    visited.add(route)
                            else:
                                if route not in visited:
                                    cheats2[abs(t[x, y] - t[x + i, y + j]) - i - j] = 1
                                    visited.add(route)
                    if x - i >=  0 and y + j < grid.shape[1]:
                        route = sorted([(x, y), (x - i, y + j)], key=lambda x: (x[0], x[1]))
                        route = tuple([x for xs in route for x in xs])
                        if grid[x - i, y + j] != '#':
                            if abs(t[x, y] - t[x - i, y + j]) - i - j in cheats2:
                                if route not in visited:
                                    cheats2[abs(t[x, y] - t[x - i, y + j]) - i - j] += 1
                                    visited.add(route)
                            else:
                                if route not in visited:
                                    cheats2[abs(t[x, y] - t[x - i, y + j]) - i - j] = 1
                                    visited.add(route)
                    if x + i < grid.shape[0] and y - j >= 0:
                        route = sorted([(x, y), (x + i, y - j)], key=lambda x: (x[0], x[1]))
                        route = tuple([x for xs in route for x in xs])
                        if grid[x + i, y - j] != '#':
                            if abs(t[x, y] - t[x + i, y - j]) - i - j in cheats2:
                                if route not in visited:
                                    cheats2[abs(t[x, y] - t[x + i, y - j]) - i - j] += 1
                                    visited.add(route)
                            else:
                                if route not in visited:
                                    cheats2[abs(t[x, y] - t[x + i, y - j]) - i - j] = 1
                                    visited.add(route)
                    if x - i >= 0 and y - j >= 0:
                        route = sorted([(x, y), (x - i, y - j)], key=lambda x: (x[0], x[1]))
                        route = tuple([x for xs in route for x in xs])
                        if grid[x - i, y - j] != '#':
                            if abs(t[x, y] - t[x - i, y - j]) - i - j in cheats2:
                                if route not in visited:
                                    cheats2[abs(t[x, y] - t[x - i, y - j]) - i - j] += 1
                                    visited.add(route)
                            else:
                                if route not in visited:
                                    cheats2[abs(t[x, y] - t[x - i, y - j]) - i - j] = 1
                                    visited.add(route)
                        
print(sum([cheats2[x] for x in cheats2.keys() if x >= saving]))