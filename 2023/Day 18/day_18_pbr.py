with open("inputs/day_18_pbr.txt") as file:
  lines = [line.rstrip().split() for line in file]

turns = {"C" : [("U","R"), ("R", "D"), ("D", "L"), ("L", "U")],
         "A" : [("U","L"), ("L", "U"), ("U", "R"), ("L", "D")]}

# Use "Surveyor's Formula"
# Strictly speaking this won't always work as it assumes that the path
# is clockwise from the start rather than anticlockwise, but running it twice
# is faster than checking chirality.
def surveyor(lines, chiral):
  corners = [(0,0)]
  x = 0
  y = 0
  for line in lines:
    if line[0] == "U": y += int(line[1])
    if line[0] == "D": y -= int(line[1])
    if line[0] == "L": x -= int(line[1])
    if line[0] == "R": x += int(line[1])
    corners.append((x,y))
  area = corners[-1][0]*corners[0][1] - corners[0][0]*corners[-1][1]
  for i in range(len(corners) -1):
    area += corners[i][0]*corners[i+1][1] - corners[i+1][0]*corners[i][1]
  outside = 0
  for i in range(len(lines)):
    outside += int(lines[i][1]) - 1
    if i > 0:
      if ((lines[i-1][0], lines[i][0]) in turns[chiral]):
        outside += 1.5
      else: outside += 0.5
  if (lines[-1][0], lines[0][0]) in turns[chiral]:
    outside += 1.5
  else: outside += 0.5
  return(abs(area//2) + outside//2)

print(f"Part 1: {surveyor(lines,'C')}")

dirs = ["R", "D", "L", "U"]
lines_2 = [[dirs[int(l[-1][-2])], int("0x" + l[-1][2:7], 16)] for l in lines]

print(f"Part 2: {surveyor(lines_2, 'C')}")


# My original solution for Part 1
# It's much too slow for Part 2, but it does make a pretty map

from PIL import Image
import numpy as np

# Get bounds
v = 0
h = 0
bounds = [0,0,0,0]
for line in lines:
  if line[0] == "U": v-= int(line[1])
  if line[0] == "D": v+= int(line[1])
  if line[0] == "L": h-= int(line[1])
  if line[0] == "R": h+= int(line[1])
  if v < bounds[0]: bounds[0] = v
  if v > bounds[1]: bounds[1] = v
  if h < bounds[2]: bounds[2] = h
  if h > bounds[3]: bounds[3] = h


grid = [[[] for _ in range(bounds[3] - bounds[2] + 1)] for _ in range(bounds[1] - bounds[0] + 1)]

inside = 0
curr = [abs(bounds[0]), abs(bounds[2])]
for line in lines:
  for _ in range(int(line[1])):
    if line[0] == "U": curr[0] -= 1
    if line[0] == "D": curr[0] += 1
    if line[0] == "L": curr[1] -= 1
    if line[0] == "R": curr[1] += 1
    grid[curr[0]][curr[1]] = ["#"]
    inside += 1


for i, row in enumerate(grid):
  count = 0
  wall = 0
  down = 0
  for j, item in enumerate(row):
    if len(item) > 0:
      if not wall:
        if i == 0 or len(grid[i-1][j]) == 0 or (len(grid[i-1][j]) > 0 and grid[i-1][j][0] == 0.5):
          down = 1
        count += 1
      wall += 1
    else:
      if wall >= 1:
        if wall > 1:
          if (i == 0 or len(grid[i-1][j-1]) == 0 or (len(grid[i-1][j-1]) > 0 and grid[i-1][j-1][0] == 0.5)):
            if down:
              count += 1
          else:
            if not down:
              count += 1
        down = 0
        wall = 0
      if count % 2: 
        inside += 1
        grid[i][j] = [0.5]
#print(inside)

for j, row in enumerate(grid):
  for i, x in enumerate(row):
    if len(x) > 0:
      if grid[j][i][0] == "#":
        grid[j][i] = (0,0,0)
      else:
        grid[j][i] = (1,0,0)
    else:
      grid[j][i] = (0,1,0)
a = np.array(grid, dtype=np.uint8)*255
im = Image.fromarray(a)
im.save("path.png")
