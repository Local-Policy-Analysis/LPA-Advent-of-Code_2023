# It's James' Favourite! Djikstra!
import heapq
from math import copysign
with open("inputs/day_17_pbr.txt") as file:
#with open("Day 17/test.txt") as file:
  lines = [line.rstrip() for line in file]

directions = ((1,0),(0,1),(-1,0),(0,-1))
max_x = len(lines)
max_y = len(lines[0])

"""
# store[min distance, remaining restriction in the form
#    (# of moves left up,
#     # of moves left right,
#     # of moves left down,
#     # of moves left left)]
s = [[[1e8,[3,3,3,3]] for _ in line]for line in lines] #distance matrix
q = [[[]for _ in line] for line in lines] #used matrix

s[0][0][0] = 0
q[0][0] = []
s[0][1] = [int(lines[0][1]), [3,2,3,3]]
s[1][0] = [int(lines[1][0]), [3,3,2,3]]



def djikstra_sub_step(x,y):
  q[x][y].append(tuple(s[x][y][1]))
  valid_steps = s[x][y][1]
  for i, z in enumerate(zip(directions, valid_steps)):
    if z[1] > 0: # if you can step in that direction
      new_space = [sum(z) for z in zip(z[0], (x,y)) if sum(z) >=0]
      if len(new_space) < 2 or (new_space[0] > (max_x - 1)) or (new_space[1] > (max_y - 1)):
        break
      if True:
        new_dist = s[x][y][0] + int(lines[new_space[0]][new_space[1]])
        if new_dist < s[new_space[0]][new_space[1]][0]:
          s[new_space[0]][new_space[1]][0] = new_dist
          s[new_space[0]][new_space[1]][1][i] = s[x][y][1][i] - 1
"""
def get_min_djk():
  min_d = 1e8
  coord = [-1,-1]
  for x in range(max_x):
    for y in range(max_y):
      if s[x][y][0] < min_d and (tuple(s[x][y][1]) not in q[x][y]):
        min_d = s[x][y][0]
        coord = [x, y]
  print(coord)
  return(coord)
 
def djk_heap(start, stop):
  q, seen = [(0, start[0], start[1], 0, 0, 0)], set()
  loop = 0
  while q:
    loop += 1
    if loop % 10000 == 0:
      print(loop)
      print(len(q))
      if loop > 286163:
        return(0)
    heat,x,y,delta,xdist,ydist = heapq.heappop(q)

    if (x,y) == stop:
      return((heat))

    if (heat,x,y,delta,xdist,ydist) not in seen:
      seen.add((heat,x,y,delta,xdist,ydist))
      i = 0
      for d in directions:
        coords = (x + d[0], y + d[1])
        delta = max(abs(xdist + d[0]), abs(ydist + d[1]))
        if delta == 4 or coords[0] < 0 or coords[1] < 0 or (xdist != 0 and d[0] == -copysign(1,xdist)) or (ydist != 0 and d[1] == -copysign(1,ydist)) or coords[0] == max_x or coords[1] == max_y:
          continue
        xdist_o = (d[0] + xdist)*abs(d[0])
        ydist_o = (d[1] + ydist)*abs(d[1])
        heapq.heappush(q, (heat + int(lines[coords[0]][coords[1]]), coords[0], coords[1], delta, xdist_o, ydist_o))

print(djk_heap((0,0),(max_x-1,max_y-1)))

"""
loops = 0
coord = [0,0]
while coord[0] != -1 and loops < 200:
  coord = get_min_djk()
  djikstra_sub_step(*coord)
  loops += 1

def prints():
  for x in s:
    for y in x:
      print(y[0], end=",")
    print("")
  print(loops)

prints()
"""