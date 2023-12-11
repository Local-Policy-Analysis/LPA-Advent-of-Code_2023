import copy

# This is terrible and I'm very sorry

with open("inputs/day_10_pbr.txt") as file:
  lines = [line.rstrip() for line in file]

pipe = [[i for i in range(len(lines[0]))] for _ in range(len(lines))]


# Assume there's only the one loop and just remove all other characters that aren't connected. 
# Use James' excellent adjacency matrix idea to check

adj = {"|" : [(-1,0), (1,0)],
       "-" : [(0,-1), (0,1)],
       "L" : [(-1,0), (0,1)],
       "J" : [(-1,0), (0,-1)],
       "7" : [(1,0), (0,-1)],
       "F" : [(1,0), (0,1)],
       "." : [],
       "S" : []}

start = ()
prev = ()
curr = ()
dist = 0
# find S
for i in range(len(lines)):
  for j in range(len(lines[i])):
    if lines[i][j] == "S":
      start = (i, j)
      break
  if start != ():
    break

# Make a second cleaner map that contains just the pipe
pipe[start[0]][start[1]] = lines[start[0]][start[1]]
# find a surrounding tile that leads to S
for i in range(start[0] - 1,start[0] + 2):
  for j in range(start[1] - 1,start[1] + 2):
    myadj = adj[lines[i][j]]
    if myadj == "dot":
      pass
    if any([all([pair[0] == pair[1] for pair in zip([sum(x) for x in zip((i,j), y)],start)]) for y in myadj]): #no
      curr = (i, j)
      pipe[i][j] = lines[i][j]
      prev = start
      dist = 1
      break
loops = 0
while (not all(x[0] == x[1] for x in zip(curr, start))) and loops < 1e5:
  for i in adj[lines[curr[0]][curr[1]]]:
    if (i[0] + curr[0] != prev[0]) or (i[1] + curr[1] != prev[1]):
      prev = copy.copy(curr)
      curr = (curr[0] + i[0], curr[1] + i[1])
      pipe[curr[0]][curr[1]] = lines[curr[0]][curr[1]]
      dist += 1
      break
  loops += 1
print(f"Part 1: {dist//2}")    

# Cells are inside if when you go directly west from them, you pass an odd number of pipes
# What counts as passing a pipe is a bit of a pain
rays = {"|" : 1,
       "-" : 0,
       "L" : 1,
       "J" : 1,
       "7" : 0,
       "F" : 0,
       "S" : 1, # Here we cheat by knowing that for my input, S is |
       "@" : 0}

inside = 0
for row in pipe:
  out = ""
  passed = 0
  for i in range(len(row)):
    if (isinstance(row[i], int)) and (passed % 2 == 1):
      out += str(passed)
      inside += 1
      pass
    elif row[i] in rays.keys():
        passed += rays[row[i]]
        out += "0"
    else:
      out += "F"
print(f"Part 2: {inside}")