# It's James' Favourite! Djikstra!
# I think the time it's taken me to learn to use igraph probably made it slower than just writing my own solution
# But not I know a bit about igraph...
import igraph
from itertools import chain

#with open("inputs/day_17_pbr.txt") as file:
with open("Day 17/test.txt") as file:
  lines = [line.rstrip() for line in file]

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

directions = ((1,0),(0,1),(-1,0),(0,-1))
max_x = len(lines)
max_y = len(lines[0])

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