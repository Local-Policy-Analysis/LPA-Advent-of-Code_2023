import numpy as np
import heapq

with open('input_jac.txt') as f:
    data = np.array([list(d.strip()) for d in f.readlines()])
    
# translate orientation to movement
orientations = set(['N', 'E', 'S', 'W'])
moves = {'N': (-1, 0),
         'S': (1, 0),
         'W': (0, -1),
         'E': (0, 1),
         }

# find start and end coordinates
start_x = np.nonzero(data=='S')[0][0]
start_y = np.nonzero(data=='S')[1][0]
end_x = np.nonzero(data=='E')[0][0]
end_y = np.nonzero(data=='E')[1][0]

def print_grid(grid):
    for g in grid:
        print(''.join(g))
    print('\n')

# find neighbours
def find_neighbours(x, y, o):
    neighbours = []
    dx, dy = moves[o]
    # if you can move forward in current orientation then add new position with current orientation
    if data[x + dx, y + dy] == '.':
        neighbours.append((x + dx, y + dy, o))
    # if you can move in new orientation, then add current pos with new orientation
    for orientation in orientations - set([o]):
        dx, dy = moves[orientation]
        if data[x + dx, y + dy] == '.':
            neighbours.append((x, y, orientation))
    return neighbours

# does cost need to be included in candidates?

def update_tentative(neighbours, candidate, tentative):
    candidate_cost, candidate_x, candidate_y, candidate_orientation = candidate
    for n in neighbours:
        neighbour_x, neighbour_y, neighbour_orientation = n
        if neighbour_orientation == candidate_orientation:
            cost = tentative[(candidate_x, candidate_y, candidate_orientation)] + 1
        else:
            cost = tentative[(candidate_x, candidate_y, candidate_orientation)] + 1000
        if n in tentative and cost > tentative[n]:
            continue
        # if n in parents:
        #     parents[n] += [(candidate_x, candidate_y, candidate_orientation)]
        # else:
        #     parents[n] = [(candidate_x, candidate_y, candidate_orientation)]
        yield n, cost

path = set([(end_x, end_y, 'N')])
def count_path(parents, child, tentative):
    if parents[child] == ['start']:
        return True
    for parent in parents[child]:
        path.add(child)
        count_path(parents, parent, tentative)
            
def find_cheapest_path():
    parents = {(start_x, start_y, 'E'): ['start']}
    candidates = [(0, start_x, start_y, 'E')]
    tentative = {(start_x, start_y, 'E'): 0}
    visited = set()
    while ((end_x, end_y, 'N') not in visited and 
           (end_x, end_y, 'E') not in visited and 
           (end_x, end_y, 'S') not in visited and 
           (end_x, end_y, 'W') not in visited and 
           len(candidates) > 0):
        candidate = heapq.heappop(candidates)
        candidate_cost, candidate_x, candidate_y, candidate_orientation = candidate
        if candidate in visited:
            continue
        visited.add(candidate)
        neighbours = find_neighbours(candidate_x, candidate_y, candidate_orientation)
        updates = update_tentative(neighbours, candidate, tentative)
        for update in updates:
            u, c = update
            u_x, u_y, u_orientation = u
            if u in parents and tentative[u] == c:
                parents[u] += [(candidate_x, candidate_y, candidate_orientation)]
            elif u in parents and tentative[u] > c:
                parents[u] = [(candidate_x, candidate_y, candidate_orientation)]
            else:
                parents[u] = [(candidate_x, candidate_y, candidate_orientation)]
            tentative[u] = c
            heapq.heappush(candidates, (c, u_x, u_y, u_orientation))
        if (end_x + 1, end_y, 'N') in tentative:
            parents[(end_x, end_y, 'N')] = (end_x + 1, end_y, 'N')
            return tentative[(end_x + 1, end_y, 'N')] + 1, tentative, parents
        elif (end_x, end_y - 1, 'E') in tentative:
            parents[(end_x, end_y, 'E')] = (end_x, end_y - 1, 'E')
            return tentative[(end_x, end_y - 1, 'E')] + 1, tentative, parents
        elif (end_x - 1, end_y, 'S') in tentative:
            parents[(end_x, end_y, 'S')] = (end_x - 1, end_y, 'S')
            return tentative[(end_x - 1, end_y, 'S')] + 1, tentative, parents
        elif (end_x, end_y + 1, 'W') in tentative:
            parents[(end_x, end_y, 'W')] = (end_x, end_y + 1, 'W')
            return tentative[(end_x, end_y + 1, 'W')] + 1, tentative, parents
      
cost, tentative, parents = find_cheapest_path()  
print(cost)
count_path(parents, (end_x + 1, end_y, 'N'), tentative)
for p in path:
    data[(p[0], p[1])] = 0
print(np.count_nonzero(data=='0'))

# test -> 7036
# test1 -> 11048