import os
import re
from functools import reduce
from operator import mul

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 6')

with open('input_jac.txt') as f:
    data = [d.strip().split(':')[1] for d in f.readlines()]
    
data = [re.findall(r'\d+', d) for d in data]
time, distance = [[int(n) for n in d] for d in data]

print(reduce(mul, [sum([1 if x * (t - x) > d else 0 for x in range(t)]) for t, d in zip(time, distance)], 1))
print(sum([1 if x * (57726992 - x) > 291117211762026 else 0 for x in range(57726992)]))






