import re
from functools import reduce

replacements = {
    "one" : "o1e",
    "two" : "t2o",
    "three" : "t3e",
    "four" : "f4r",
    "five" : "f5e",
    "six" : "s6x",
    "seven" : "s7n",
    "eight" : "e8t",
    "nine" : "n9e"
}

with open("day_1.txt") as file:
    lines = [line.rstrip() for line in file]
    
 # I am not sorry
print(sum([int(y[0]) * 10 + int(y[-1]) for y in [re.findall("\d", x) for x in lines]]))


# Still not sorry
print(sum([int(y[0]) * 10 + int(y[-1]) for y in [re.findall("\d", x) for x in [reduce(lambda a, kv: a.replace(*kv), replacements.items(), z) for z in lines]]]))