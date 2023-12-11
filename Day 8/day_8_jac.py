import os
import re
from itertools import cycle
from math import gcd

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 8')

with open('input_jac.txt') as f:
    data = [d.strip() for d in f.readlines()]
    
directions, _, *nodes = data
nodes = [re.findall(r'[A-Z0-9]+', n) for n in nodes]

graph = {}
for n in nodes:
    graph[n[0]] = (n[1], n[2])
    
current_node = 'AAA'
step_count = 0
direction_cycle = cycle(directions)
for direction in direction_cycle:
    step_count += 1
    if direction == 'L':
        current_node = graph[current_node][0]
    else: 
        current_node = graph[current_node][1]
    if current_node == 'ZZZ':
        break
            
print(step_count)

start_nodes = [n[0] for n in nodes if n[0][-1] == 'A']

cycle_lenghts = []
direction_cycle = cycle(directions)
for node in start_nodes:
    step_count = 0
    for direction in direction_cycle:
        step_count += 1
        if direction == 'L':
            node = graph[node][0]
        else: 
            node = graph[node][1]
        if node[-1] == 'Z':
            break
    cycle_lenghts.append(step_count)
    
def find_lcm(cycles):
    lcm = 1
    for c in cycles:
        lcm = lcm * c // gcd(lcm, c)
    return lcm
    
print(find_lcm(cycle_lenghts))