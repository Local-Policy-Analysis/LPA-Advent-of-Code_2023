import os
import numpy as np
from itertools import combinations

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 11')

with open('input_jac.txt') as f:
    data = np.array([list(d.strip()) for d in f.readlines()])
    
# just change the value after else to 1 to get back to pt 1
col_counts = [0 if n > 0 else 1000000 - 1 for n in np.count_nonzero(data == '#', axis=0)]
row_counts = [0 if n > 0 else 1000000 - 1 for n in np.count_nonzero(data == '#', axis=1)]
galaxies = np.argwhere(data == '#')
galaxy_pairs = list(combinations(galaxies, 2))

answer = 0
for pair in galaxy_pairs:
    start, end = pair
    x_start, y_start = start
    x_end, y_end = end
    distance = (abs(x_start - x_end) + abs(y_start - y_end) +
                sum(row_counts[min(x_start, x_end): max(x_start, x_end)]) +
                sum(col_counts[min(y_start, y_end): max(y_start, y_end)]))
    answer += distance
    
print(answer)