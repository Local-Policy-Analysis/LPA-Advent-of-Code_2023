from math import ceil
from functools import reduce

with open("inputs/day_6_pbr.txt") as file:
  lines = [line.rstrip() for line in file]

input = list(zip(lines[0].split(":")[1].split(),lines[1].split(":")[1].split()))


def solve_quadratic(a,b,c):
  desc = pow(pow(b,2) - (4 * a * c), 0.5)
  return(((desc - b)/(2*a), (-desc-b)/2*a))


ranges = [solve_quadratic(-1, int(race[0]), -int(race[1])) for race in input]
ranges = [abs(int(x[0]) - ceil(x[1])) -1 for x in ranges]
print("Part 1: {}".format(reduce(lambda x, y: x * y, ranges)))

input_2 = (lines[0].split(":")[1].replace(" ", ""), lines[1].split(":")[1].replace(" ", ""))
sols_2 = solve_quadratic(-1, int(input_2[0]), -int(input_2[1]))
print("Part 2: {}".format(abs(int(sols_2[0]) - ceil(sols_2[1])) - 1))
