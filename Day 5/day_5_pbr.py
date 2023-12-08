with open("inputs/day_5_pbr.txt") as file:
    lines = [line.rstrip() for line in file]

seeds = list(map(int, lines[0].split(": ")[1].split()))

maps = []
peg = -1
for x in range(1,len(lines)):
    if ":" in lines[x]:
        maps.append([])
        peg += 1
    elif len(lines[x]) > 0:
        maps[peg].append(list(map(int, lines[x].split())))
maps = [sorted(x, key = lambda x: x[1]) for x in maps]

def lookup(x, maps):
    temp = x
    for z in maps:
        for y in z:
            if temp >= y[1] and temp < y[1] + y[2]:
                temp = temp + (y[0] - y[1])
                break
    return(temp)

print("Part 1: {}".format(min([lookup(seed, maps) for seed in seeds])))

# there's definitely a way to do this in only one pass but at this point
# it would have been faster to just brute force it

seeds = sorted(zip(seeds[0::2], seeds[1::2]), key = lambda x: x[0])



def do_pass(seeds, layer):
    tester = sorted(set([0] + [x[1] for x in layer] + [x[1] + x[2] for x in layer]))
    breaks = []
    gaps = []
    for x in tester:
        for y in range(len(seeds)):
            if x > seeds[y][0] and x < seeds[y][0]+ seeds[y][1]:
                breaks.append(x)
    breaks = sorted(set(breaks + [x[0] for x in seeds]))
    i = 0
    for x in range(len(seeds)):
        while (i < len(breaks) - 1) and (breaks[i+1] < seeds[x][0] + seeds[x][1]):
            gaps.append(breaks[i+1] - breaks[i])
            i += 1
        gaps.append(seeds[x][0] + seeds[x][1] - breaks[i])
        i += 1
    breaks = [lookup(x, [layer]) for x in breaks]
    new_seeds = sorted(list(zip(breaks, gaps)), key = lambda x: x[0])
    return(new_seeds)

new_seeds = seeds
# Should use reduce here but what can you do
for i, x in enumerate(maps):
    new_seeds = do_pass(new_seeds, x)
print("Part 2: {}".format(min(seed[0] for seed in new_seeds)))
