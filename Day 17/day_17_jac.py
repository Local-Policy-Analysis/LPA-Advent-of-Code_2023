import os
import numpy as np
import heapq

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 17')

with open('test_jac.txt') as f:
    data = [list(d.strip()) for d in f.readlines()]
data = np.array([[int(c) for c in d] for d in data])

def get_neighbours(coords, dir, previous, consecutive):
    adjacent = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    current_x, current_y = coords
    return ([(current_x + a[0], current_y + a[1]) for a in adjacent 
             if (not consecutive == 3 and a == dir)                                                     # checking for consecutive moves in same direction
             and 0 <= current_x + a[0] < data.shape[0] and 0 <= current_y + a[1] < data.shape[1]])		# checking in bounds

def update_costs(candidate_coords, candidate_dir, consecutive, neighbours, tentative):
    x, y = candidate_coords
    cost = tentative[(candidate_coords, candidate_dir, consecutive)] + data[x, y]
    for n in neighbours:
        if n in tentative and cost >= tentative[n]:
            continue
        yield n, cost, (n[0] - x, n[1] - y), consecutive + 1 if candidate_dir == (n[0] - x, n[1] - y) else 1
        
def find_path():
    # set start and finish co-ordinates
    start = (0, 0)
    finish = (data.shape[0] - 1, data.shape[1] - 1)
    # initialise variables
    candidates = [(0, start, (0, 0), 1)]                    # list -> cost, coords, dir, consecutive similar directions
    tentative = {(start, (0, 0), 1): 0}                     # dict -> coords, dir, consecutive similar directions: cost
    previous = {(start, (0, 0), 1): (start, (0, 0), 1)}     # dict -> cost, coords, dir, consecutive similar directions: previous cost, coords, dir, consecutive similar directions
    certain = set()
    while finish not in certain and len(candidates) > 0:
        candidate_cost, candidate_coords, candidate_dir, consecutive = heapq.heappop(candidates)
        if (candidate_coords, candidate_dir, consecutive) in certain:
            continue
        certain.add((candidate_coords, candidate_dir, consecutive))
        neighbours = set(get_neighbours(candidate_coords, candidate_dir, consecutive, previous)) - certain
        updates = update_costs(candidate_coords, candidate_dir, consecutive, neighbours, tentative)
        for coords, cost, dir, cons in updates:
            tentative[(coords, dir, cons)] = cost
            previous[(coords, dir, cons)] = candidate_coords, candidate_dir
            heapq.heappush(candidates, (cost, coords, dir, cons))
        if (finish, (0, 1), 1) in tentative:
            return tentative[(finish, (0, 1))] + data[-1, -1]
        elif (finish, (1, 0), 1) in tentative:
            return tentative[(finish, (1, 0))] + data[-1, -1], previous, tentative
        elif (finish, (0, 1), 2) in tentative:
            return tentative[(finish, (1, 0))] + data[-1, -1], previous, tentative
        elif (finish, (1, 0), 2) in tentative:
            return tentative[(finish, (1, 0))] + data[-1, -1], previous, tentative
        elif (finish, (0, 1), 3) in tentative:
            return tentative[(finish, (1, 0))] + data[-1, -1], previous, tentative
        elif (finish, (1, 0), 3) in tentative:
            return tentative[(finish, (1, 0))] + data[-1, -1], previous, tentative
        
cost, previous, tentative = find_path()
print(cost)