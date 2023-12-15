with open("inputs/day_14_pbr.txt") as file:
  lines = [line.rstrip() for line in file]

rounds = []
blocks = []
tops = [-1 for _ in lines[0]]
for i in range(len(lines)):
  for j in range(len(lines[i])):
    if lines[i][j] == "#":
      tops[j] = i
      blocks.append([i,j])
    if lines[i][j] == "O":
      tops[j] = tops[j] + 1
      rounds.append([tops[j],j])

s = sum([len(lines) - x[0] for x in rounds])
print(f"Part 1: {s}")

map = [list(line) for line in lines]

def tiltv(map, dir):
  if dir == 1: 
    tops = [-1 for _ in lines[0]]
  else:
    tops = [len(lines) for _ in lines[0]]
  if dir == 1: #tilt up
    vrange =  range(len(lines)) 
  else:
    vrange = reversed(range(len(lines)))
  for i in vrange:
    for j in range(len(lines[i])):
      if map[i][j] == "#":
        tops[j] = i
      if map[i][j] == "O":
        if (tops[j]) != i:
          map[i][j] = "."
        map[tops[j] + dir][j] = "O"
        tops[j] = tops[j] + dir

def tilth(map, dir):
  count = 0
  if dir == 1:
    tops = [len(lines[0]) for _ in lines[0]]
  else:
    tops = [-1 for _ in lines]
  if dir == 1: #tilt right
    hrange = reversed(range(len(lines[0])))
  else:
    hrange = range(len(lines[0]))
  for j in hrange:
    for i in range(len(lines)):
      if map[i][j] == "#":
        tops[i] = j
      if map[i][j] == "O":
        if (tops[i]) != j:
          map[i][j] = "."
        map[i][tops[i] - dir] = "O"
        tops[i] = tops[i] - dir
        count += 1

def spin():
  tiltv(map, 1)
  tilth(map, -1)
  tiltv(map, -1)
  tilth(map, 1)

i = 0
# This is quite a slow data structure for this, but hey-ho
h = []
while i < 1000000:
  spin()
  h_s = str(map)
  if h_s in [x[1] for x in h]:
    lp_start = [x[0] for x in h if x[1] == h_s][0]
    lp_len = i - lp_start
    extra = (1000000000 - lp_start) % lp_len
    for _ in range(extra - 1):
      spin()
    break
  h.append((i, h_s))
  i += 1
load = 0
for x in range(len(map)):
  load += map[x].count("O")*(len(map)-x)
print(load)
