import os
from itertools import combinations
import re
import numpy as np

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 12')

with open('input_jac.txt') as f:
    data = [d.strip().split(' ') for d in f.readlines()]

arrangements = [np.array(list(d[0])) for d in data]
groups = [[int(n) for n in d[1].split(',')] for d in data]
arrangements_without_spring = [s for s in arrangements if '#' not in s]
arrangements_a = [np.array(list(''.join(a) + ('.' if a[0] == '#' else '?'))) for a in arrangements]
arrangements_b = [np.array(list(('.' if a[-1] == '#' else '?' )+ ''.join(a))) for a in arrangements]

pt1 = []
for arrangement, group in zip(arrangements, groups):
    valid_arrangements = 0
    springs = [int(a) for a in np.argwhere(arrangement == '#')]
    uncertain_springs = [int(a) for a in np.argwhere(arrangement == '?')]
    n_springs = sum(group)
    n_uncertain_springs = n_springs - len(springs)
    candidate_arrangements = [list(combo) for combo in combinations(uncertain_springs, n_uncertain_springs)]
    pttn = r''.join([f'.*#{{{n}}}.+' for n in group])
    pttn = pttn[:-1] + '*'
    for candidate in candidate_arrangements:
        test = ''.join(['#' if x in springs + candidate else '.' for x in range(len(arrangement))])
        if re.match(pttn, test):
            valid_arrangements += 1
    pt1.append(valid_arrangements)
            
print(sum(pt1))

# pt2 presumably creates too many possible combinations to iterate through them all, so need to be smarter
# final repeat does not get a trailing ?
# therefore needs to calculate all possible arrangements for two groups - with and without the final ?
# combos with trailing ? is raised to the power of 4
# then multiply by combos in other group
# proceed by working out possible locations for first group
# it is only the final group that is affected by trailing ?

pt2 = []
for arrangement_b, arrangement_a, group in zip(arrangements_b, arrangements_a, groups):
    valid_arrangements_b = 0
    valid_arrangements_a = 0
    springs_b = [int(a) for a in np.argwhere(arrangement_b == '#')]
    springs_a = [int(a) for a in np.argwhere(arrangement_a == '#')]
    uncertain_springs = [int(a) for a in np.argwhere(arrangement_b == '?')]
    uncertain_springs_a = [int(a) for a in np.argwhere(arrangement_a == '?')]
    n_springs = sum(group)
    n_springs_a = sum(group)
    n_uncertain_springs = n_springs - len(springs_b)
    n_uncertain_springs_a = n_springs - len(springs_a)
    candidate_arrangements = [list(combo) for combo in combinations(uncertain_springs, n_uncertain_springs)]
    candidate_arrangements_a = [list(combo) for combo in combinations(uncertain_springs_a, n_uncertain_springs)]
    pttn = r''.join([f'.*#{{{n}}}.+' for n in group])
    pttn = pttn[:-1] + '*'
    for candidate in candidate_arrangements:
        test = ''.join(['#' if x in springs_b + candidate else '.' for x in range(len(arrangement_b))])
        if re.match(pttn, test):
            valid_arrangements_b += 1
    # print(f'spring_a {springs_a} uncertain springs {uncertain_springs_a} candidate arrangements {candidate_arrangements_a}')
    for candidate in candidate_arrangements_a:
        test = ''.join(['#' if x in springs_a + candidate else '.' for x in range(len(arrangement_a))])
        if re.match(pttn, test):
            valid_arrangements_a += 1
    pt2.append(min(valid_arrangements_b, valid_arrangements_a) * max(valid_arrangements_b, valid_arrangements_a) ** 4)
    
print(pt2)
print(sum(pt2))
