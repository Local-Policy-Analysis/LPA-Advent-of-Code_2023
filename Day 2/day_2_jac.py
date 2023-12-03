import re

with open('input_jac.txt') as f:
    data = [d.strip().split(':')[-1] for d in f.readlines()]
    
r = 12
g = 13
b = 14

pt1 = 0
pt2 = 0
for i, d in enumerate(data):
    reds = max([int(n) for n in re.findall(r'(\d+) red', d)])
    greens = max([int(n) for n in re.findall(r'(\d+) green', d)])
    blues = max([int(n) for n in re.findall(r'(\d+) blue', d)])
    pt2 += reds * blues * greens
    if reds <= r and greens <= g and blues <= b:
        pt1 += i + 1

print(pt1)
print(pt2)