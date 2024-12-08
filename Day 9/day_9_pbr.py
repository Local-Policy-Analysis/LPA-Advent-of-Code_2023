# The actual solution uses none of these
import numpy as np
from numpy.linalg import inv, solve
from collections import deque

with open("inputs/day_9_pbr.txt") as file:
  lines = [[int(x) for x in line.rstrip().split()] for line in file]

# If Part 2 isn't some large nth term, this has been such a waste of time!

def p1(series:list):
    if len(series) < 2:
        return([0])
    elif all([x == series[0] for x in series]):
        series.append(series[0])
        return(series)
    else:
        series.append(series[-1] + p1([series[1:][x] - series[x] for x in range(len(series) - 1)])[-1])
        return(series)

print(f"Part 1: {sum([p1(line)[-1] for line in lines])}")

print(f"Part 2: {sum([p1(line[::-1])[-1] for line in lines])}")

#
# Apparently it was indeed a huge waste of time. 
# I'm keeping this anyway because while it will always run into rounding errors,
# The code might be useful later
#
#
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡭⠥⠐⠒⠒⠒⠒⠂⠤⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⢀⣤⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⣤⡀⠀⠀⠀⠀⠀
#⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢦⡀⠀⠀⠀
#⠀⠀⢠⠟⠀⠀⠀⠀⠀⣠⣤⣤⡀⠀⠀⠀⠀⠀⣤⣤⣄⠀⠀⠀⠀⠈⠻⡄⠀⠀
#⠀⣠⠋⠀⠀⠀⠀⠀⠀⣿⣿⣿⣧⠀⠀⠀⠀⣼⣿⣿⣿⠀⠀⠀⠀⠀⠀⠹⣄⠀
#⠀⡏⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡟⠀⠀⠀⠀⢻⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⢹⠀
#⢰⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠀⠀⠀⠀⠀⠀⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⡆
#⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
#⠸⠀⠀⠀⠀⠀⠀⠀⣠⣴⡿⠟⠛⠋⠉⠉⠙⠛⠻⢷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠇
#⠀⣇⠀⠀⠀⠀⢀⣼⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣷⡀⠀⠀⠀⠀⣸⠀
#⠀⠘⣆⠀⠒⠲⣾⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⡷⠖⠒⠀⣰⠃⠀
#⠀⠀⠘⣦⡀⠀⠈⠳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⠁⠀⠀⣴⠃⠀⠀
#⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀
#⠀⠀⠀⠀⠀⠈⠛⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠛⠁⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠒⠠⠤⠤⠤⠤⠄⠒⠚⠉⠀⠀⠀⠀

def diffs(series: list, layer: int):
    if len(series) < 2:
        return((-1,-1))
    elif all([x == series[0] for x in series]):
        return((series[0], layer))
    else:
        return(diffs([series[1:][x] - series[x] for x in range(len(series) - 1)], layer + 1))

# This runs into stupid rounding errors
def nthTerm(series:list, n:int):
    order = diffs(series, 0)[1] + 1
    a = [[pow(i+1,x) for x in range(order)] for i in range(order)]
    ainv = inv(np.float64(a))
    powers = (np.matmul(ainv,np.array(series)[:order]))
    out = sum([powers[i]*pow(n,i) for i in range(order)])
    return(out)

# This also runs into rounding errors, but fewer of them
def betterNthTerm(series:list, n:int):
    order = diffs(series, 0)[1] + 1
    a = [[pow(i+1,x) for x in range(order)] for i in range(order)]
    powers = solve(np.float64(a), np.array(series)[:order])
    #powers = (np.matmul(ainv,np.array(series)[:order]))
    out = sum([powers[i]*pow(n,i) for i in range(order)])
    return(round(out))

