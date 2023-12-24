import os
import numpy as np

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 14')

with open('input_jac.txt') as f:
    data = np.array([list(d.strip()) for d in f.readlines()])
    
pt1 = 0
for col in data.T:
    dot_counter = 0
    for r, row in enumerate(col):    
        if col[r] == '.':
            dot_counter += 1
        elif col[r] == '#':
            dot_counter = 0
        elif col[r] == 'O':
            pt1 += data.shape[0] - r + dot_counter

print(f'pt1 is {pt1}')

def tilt_up():
    for c, col in enumerate(data.T):
        dot_counter = 0
        for r, row in enumerate(col):
            if row == '.':
                dot_counter += 1
            elif row == '#':
                dot_counter = 0
            else:
                data[r, c] = '.'
                data[r - dot_counter, c] = 'O'

def tilt_left():
    for r, row in enumerate(data):
        dot_counter = 0
        for c, col in enumerate(row):
            if col == '.':
                dot_counter += 1
            elif col == '#':
                dot_counter = 0
            else:
                data[r, c] = '.'
                data[r, c - dot_counter] = 'O'

def tilt_right():
    for r, row in enumerate(data):
        dot_counter = 0
        for c, col in enumerate(reversed(row)):
            if col == '.':
                dot_counter += 1
            elif col == '#':
                dot_counter = 0
            else:
                data[r, data.shape[1] - c - 1] = '.'
                data[r, data.shape[1] - (c - dot_counter) - 1] = 'O'

def tilt_down():
    for c, col in enumerate(data.T):
        dot_counter = 0
        for r, row in enumerate(reversed(col)):
            if row == '.':
                dot_counter += 1
            elif row == '#':
                dot_counter = 0
            else:
                data[data.shape[0] - r - 1, c] = '.'
                data[data.shape[0] - (r - dot_counter) - 1, c] = 'O'

state = ''.join(data.flatten())
states = {state: (0, sum([data.shape[0] - coords[0] for coords in np.argwhere(data == 'O')]))}

for x in range(1, 300):
    tilt_up()
    tilt_left()
    tilt_down()
    tilt_right()
    state = ''.join(data.flatten())
    if state in states:
        period = x - states[state][0]
        start = states[state][0]
        break
    states[state] = (x, sum([data.shape[0] - coords[0] for coords in np.argwhere(data == 'O')]))
    
idx = (1000000000 - start) % period + start
for key, value in states.items():
    if value[0] == idx:
        print(f'pt2 is {value[1]}')