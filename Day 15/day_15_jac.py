import os
import numpy as np

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 15')

with open('input_jac.txt') as f:
    data = f.read().strip().split(',')
    
def hash(chrs):
    current = 0
    for chr in chrs:
        current = ((current + ord(chr)) * 17) % 256
    return current

print(sum(hash(d) for d in data))

box_to_labels = {k: [] for k in range(257)}
box_to_lenses = {k: [] for k in range(257)}
for d in data:
    print(f'instruction is {d}')
    if '-' in d:
        lbl = d[:-1]
        box = hash(lbl)
        # if label is already in box remove it
        if lbl in box_to_labels[box]:
            idx = box_to_labels[box].index(lbl)
            box_to_labels[box].pop(idx)
            box_to_lenses[box].pop(idx)
    else:
        lbl, lens = d.split('=')
        lens = int(lens)
        box = hash(lbl)
        if lbl in box_to_labels[box]:
            # if label is in box replace lens with new one
            idx = box_to_labels[box].index(lbl)
            box_to_lenses[box] = box_to_lenses[box][:idx] + [lens] + box_to_lenses[box][idx + 1:]
        else:
            # if label isn't in box then add it to the end
            box_to_labels[box].append(lbl)
            box_to_lenses[box].append(lens)
            
# calculate focussing power
pt2 = 0
for box, lenses in box_to_lenses.items():
    for i, lens in enumerate(lenses):
        pt2 += (box + 1) * (i + 1) * lens
        
print(pt2)