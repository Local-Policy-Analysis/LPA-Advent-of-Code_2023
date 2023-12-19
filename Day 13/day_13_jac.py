import os
import numpy as np

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 13')

with open('input_jac.txt') as f:
    data = [d.split('\n') for d in f.read().split('\n\n')]
    
data = [np.array([[1 if cell == '#' else 0 for cell in list(r)] for r in d]) for d in data]

def get_symmetry(d):
    for x in range(d.shape[1] - 1):
        # test left right symmetry
        if (d[:, x:] == np.fliplr(d[:, x:])).all():
            if d[:, x:].shape[1] % 2 == 0:
                return x + d[:, x:].shape[1] // 2
    for x in range(d.shape[0] - 1):
        # test up down symmetry
        if (d[x:, :] == np.flipud(d[x:, :])).all():
            if d[x:, :].shape[0] % 2 == 0:
                return (x + d[x:, :].shape[0] // 2) * 100
    for x in range(d.shape[1], 1,  -1):
        # test left right symmetry
        if (d[:, :x] == np.fliplr(d[:, :x])).all():
            if d[:, :x].shape[1] % 2 == 0:
                return d[:, :x].shape[1] // 2
    for x in range(d.shape[0], 1, -1):
        # test up down symmetry
        if (d[:x, :] == np.flipud(d[:x, :])).all():
            if d[:x, :].shape[0] % 2 == 0:
                return (d[:x, :].shape[0] // 2) * 100
    return 0

def get_new_symmetry(d):
    for x in range(d.shape[1] - 1):
        # test left right symmetry
        if np.sum(d[:, x:] != np.fliplr(d[:, x:])) == 2:
            if d[:, x:].shape[1] % 2 == 0:
                return x + d[:, x:].shape[1] // 2
    for x in range(d.shape[0] - 1):
        # test up down symmetry
        if np.sum(d[x:, :] != np.flipud(d[x:, :])) == 2:
            if d[x:, :].shape[0] % 2 == 0:
                return (x + d[x:, :].shape[0] // 2) * 100
    for x in range(d.shape[1], 1,  -1):
        # test left right symmetry
        if np.sum(d[:, :x] != np.fliplr(d[:, :x])) == 2:
            if d[:, :x].shape[1] % 2 == 0:
                return d[:, :x].shape[1] // 2
    for x in range(d.shape[0], 1, -1):
        # test up down symmetry
        if np.sum(d[:x, :] != np.flipud(d[:x, :])) == 2:
            if d[:x, :].shape[0] % 2 == 0:
                return (d[:x, :].shape[0] // 2) * 100
    return 0

pt1 = 0
pt2 = 0
for d in data:
    pt1 += get_symmetry(d)
    pt2 += get_new_symmetry(d)

print(pt1)
print(pt2)