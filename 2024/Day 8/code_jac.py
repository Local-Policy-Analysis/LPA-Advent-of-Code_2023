import numpy as np
from itertools import combinations

with open('input_jac.txt') as f:
    data = np.array([[list(n) for n in d.strip()] for d in f.readlines()])[:, :, 0]
    
antinodes = set([(x, y) for x, y in zip(np.nonzero(data != '.')[0], np.nonzero(data != '.')[1])])
antennaes = list(np.unique(data))
antennaes.remove('.')
for a in antennaes:
    locations = [(x, y) for x, y in zip(np.nonzero(data == a)[0], np.nonzero(data == a)[1])]
    for p in combinations(locations, 2):
        vertical_distance = abs(p[0][0] - p[1][0])
        horizontal_distance = abs(p[0][1] - p[1][1])
        for x in range(1, 50):
            if p[0][0] >= p[1][0] and p[0][1] >= p[1][1]:
                antinode1_x = p[0][0] + vertical_distance * x
                antinode1_y = p[0][1] + horizontal_distance * x
                antinode2_x = p[1][0] - vertical_distance * x
                antinode2_y = p[1][1] - horizontal_distance * x
            elif p[0][0] < p[1][0] and p[0][1] < p[1][1]:
                antinode1_x = p[0][0] - vertical_distance * x
                antinode1_y = p[0][1] - horizontal_distance * x
                antinode2_x = p[1][0] + vertical_distance * x
                antinode2_y = p[1][1] + horizontal_distance * x
            elif p[0][0] < p[1][0] and p[0][1] >= p[1][1]:
                antinode1_x = p[0][0] - vertical_distance * x
                antinode1_y = p[0][1] + horizontal_distance * x
                antinode2_x = p[1][0] + vertical_distance * x
                antinode2_y = p[1][1] - horizontal_distance * x
            elif p[0][0] >= p[1][0] and p[0][1] < p[1][1]:
                antinode1_x = p[0][0] + vertical_distance * x
                antinode1_y = p[0][1] - horizontal_distance * x
                antinode2_x = p[1][0] - vertical_distance * x
                antinode2_y = p[1][1] + horizontal_distance * x
            if 0 <= antinode1_x < data.shape[0] and 0 <= antinode1_y < data.shape[1]:
                antinodes.add((antinode1_x, antinode1_y))
            if 0 <= antinode2_x < data.shape[0] and 0 <= antinode2_y < data.shape[1]:
                antinodes.add((antinode2_x, antinode2_y))
            if (antinode1_x < 0 or antinode1_x >= data.shape[0] or antinode1_y < 0 or antinode1_y > data.shape[1]) and (antinode2_x < 0 or antinode2_x >= data.shape[0] or antinode2_y < 0 or antinode2_y > data.shape[1]):
                break
            
print(len(antinodes))