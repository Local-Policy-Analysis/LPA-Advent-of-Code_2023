# This isn't a very good solution. I'm tired :(

import re

with open("../inputs/day_2.txt") as file:
  lines = [line.rstrip() for line in file]

def parseCubes(game):
  out = {"red": 0, "green": 0, "blue" : 0}
  for s in game.strip().split(","):
    out[s.strip().split(" ")[1]] = int(s.strip().split(" ")[0])
  return(out)

# Part 1
tot1 = 0

for line in lines:
  no = int(line.split(":")[0].split(" ")[1])
  valid = no
  cubes = [parseCubes(x) for x in line.split(":")[1].split(";")]
  for game in cubes:
    if len(set(game.keys()).difference({"red", "green", "blue"})) > 0:
      valid = 0
    else:
      if (game.get("red") > 12) | (game.get("green") > 13) | (game.get("blue") > 14):
        valid = 0
      else:
        pass
  tot1 += valid
print(tot1)

# Part 2
tot2 = 0

for line in lines:
    minCubes = {"red": 0, "green": 0, "blue": 0}
    cubes = [parseCubes(x) for x in line.split(":")[1].split(";")]
    for game in cubes:
        minCubes["red"] = max(game["red"], minCubes["red"])
        minCubes["green"] = max(game["green"], minCubes["green"])
        minCubes["blue"] = max(game["blue"], minCubes["blue"])
    power = minCubes["red"] * minCubes["green"] * minCubes["blue"]
    tot2 += power
print(tot2)
