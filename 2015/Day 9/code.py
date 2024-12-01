from itertools import permutations

with open('input.txt') as f:
    data = [[d.strip().split(' = ')[0].split(' to '), int(d.strip().split(' = ')[1])] for d in f.readlines()]
    
distances = {d[0][0] + ' ' + d[0][1]: d[1] for d in data}
distances_reversed = {d[0][1] + ' ' + d[0][0]: d[1] for d in data}
distances = {**distances, **distances_reversed}
locations = set([d[0][0] for d in data] + ['Arbre'])
perms = permutations(locations)

def find_cost(perms):
    lowest_cost = 10000
    highest_cost = 0
    for p in perms:
        temp_cost = sum([distances[str(p[n] + ' ' + p[n + 1])] for n, i in enumerate(p[:-1])])
        temp_cost2 = sum([distances[str(p[n] + ' ' + p[n + 1])] for n, i in enumerate(p[:-1])])
        if temp_cost < lowest_cost:
            lowest_cost = temp_cost
        if temp_cost2 > highest_cost:
            highest_cost = temp_cost2
    return lowest_cost, highest_cost

low, high = find_cost(perms)
print(low)
print(high)