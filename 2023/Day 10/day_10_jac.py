import os

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 10')

with open('../inputs/day_10_jac.txt') as f:
    data = [list(d.strip()) for d in f.readlines()]
    
def get_start(input):
    for i, x in enumerate(input):
        if 'S' in x:
            return (i, x.index('S'))
        
def get_neighbours(co_ords):
    x, y = co_ords
    pipe = data[x][y]
    if pipe == 'S':
        return [(x, y - 1)]
    else:
        return [(x + neighbour[0], y + neighbour[1]) for neighbour in pipes[pipe] if 0 <= x + neighbour[0] < len(data) and 0 <= y + neighbour[1] < len(data[0])]
        
start = get_start(data)

# down is up
pipes = {
         '-': [(0, 1), (0, -1)],
         '|': [(1, 0), (-1, 0)],
         '7': [(0, -1), (1, 0)],
         'J': [(-1, 0), (0, -1)],
         'F': [(1, 0), (0, 1)],
         'L': [(-1, 0), (0, 1)],
         '.': [(0, 1), (0, -1)]
         }

def get_length(current):
    start = current
    current = get_neighbours(start)[0]
    path = set()
    path.update([start])
    while start != current:
        neighbours = set(get_neighbours(current))
        try:
            current = tuple(neighbours.difference(path))[0]
        except:
            current = start
        path.update(neighbours)
    return path

path = get_length(start)
print(len(path) // 2)

counter = 0
for x, d in enumerate(data):
    for y, col in enumerate(data[0]):
        pipe_counter = 0
        if (x, y) not in path:
            for c in range(y + 1, len(data[0])):
                if data[x][c] in ['|', 'J', 'L'] and (x, c) in path:    # i spent a long time wondering why it wasn't working till I realised I had a typo ('' instead of 'L') in this line. Karma for laughing at Peter's day 9 trauma
                    pipe_counter += 1
            if pipe_counter % 2 != 0:
                counter += 1

print(counter)