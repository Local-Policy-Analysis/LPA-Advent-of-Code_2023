import numpy as np

with open('input_jac.txt') as f:
    data = np.array([[list(r) for r in d.strip()] for d in f.readlines()])[:,:,0]
data = np.array([[int(c) for c in d] for d in data]) 

potential_trailheads = [(x, y) for x, y in zip(np.nonzero(data==0)[0], np.nonzero(data==0)[1])]

def count_trailheads(coords, previous, memo):
    x, y = coords
    if data[coords] == 9 and previous == 8:
        memo.add(coords)
    elif data[coords] - previous == 1:
        if x + 1 < data.shape[0]:
            count_trailheads((x + 1, y), data[coords], memo)
        if x - 1 >= 0:
            count_trailheads((x - 1, y), data[coords], memo)
        if y + 1 < data.shape[1]:
            count_trailheads((x, y + 1), data[coords], memo)
        if y - 1 >= 0:
            count_trailheads((x, y - 1), data[coords], memo)
    return len(memo)

def count_trailheads_again(coords, previous, result):
    x, y = coords
    if data[coords] == 9 and previous == 8:
        result += 1
    elif data[coords] - previous == 1:
        if x + 1 < data.shape[0]:
            result += count_trailheads_again((x + 1, y), data[coords], 0)
        if x - 1 >= 0:
            result += count_trailheads_again((x - 1, y), data[coords], 0)
        if y + 1 < data.shape[1]:
            result += count_trailheads_again((x, y + 1), data[coords], 0)
        if y - 1 >= 0:
            result += count_trailheads_again((x, y - 1), data[coords], 0)
    return result
        
pt1 = 0
pt2 = 0
for trail in potential_trailheads:
    pt1 += count_trailheads(trail, -1, set())
    pt2 += count_trailheads_again(trail, -1, 0)
print(pt1)
print(pt2)