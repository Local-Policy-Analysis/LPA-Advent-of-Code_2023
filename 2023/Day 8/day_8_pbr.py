from math import lcm
from functools import reduce

with open("inputs/day_8_pbr.txt") as file:
  lines = [line.rstrip() for line in file]

directions = lines[0].replace("L", "0").replace("R", "1")

lookup = {}
for x in lines[2:]:
  s = x.split(" = ")
  lookup[s[0]] = s[1][1:-1].split(", ")

curr = "AAA"
steps = 0
while (curr != "ZZZ") and (steps < 1e6):
  curr = lookup[curr][int(directions[steps % len(directions)])]
  steps += 1

print("Part 1: {}".format(steps))

# From looking at the results, each start only visits one endpoint, so we don't have to deal
# with complicated maths. A more thorough solution could deal with the values if this didn't
# happen, but I will save that energy for future days

# This means that there are no smaller loops inside the big loops. *whew*
#
#

starters = []
for x in lookup.keys():
  if x[-1] == "A": starters.append(x)

ends = []
for curr in starters:
  steps = 0
  visits = {x:[] for x in lookup.keys()}
  while True:
    loop = 0
    dirPeg = steps % len(directions)
    if not(dirPeg in [x % len(directions) for x in visits[curr]]): #This is slow but not that slow
      visits[curr].append(steps)
      curr = lookup[curr][int(directions[dirPeg])]
      steps += 1
    else:
      loop_start = [x for x in visits[curr] if x % len(directions) == dirPeg]
      break
    if steps > 1e7:
      break
  ends.append([curr, [y[0] for y in [visits[x] for x in visits if x[-1] == "Z"] if len(y) == 1][0], steps - loop_start[0]])

# By inspection we just want the lcm of all of the distances. 
# So we don't have to do any complicated maths. Nice, but also annoyingly not in the question
# I would have solved this much sooner if I'd managed to type the numbers correctly into
# Wolfram Alpha when I first tried this.

print("Part 2: {}".format(reduce(lcm, [x[1] for x in ends])))