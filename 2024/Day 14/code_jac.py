import numpy as np

with open('input_jac.txt') as f:
    data = [d.strip() for d in f.readlines()]
    
locations = []
velocities = []
for d in data:
    p, v = d.split(' ')
    px, py = p.split('=')[1].split(',')
    vx, vy = v.split('=')[1].split(',')
    px = int(px)
    py = int(py)
    vx = int(vx)
    vy = int(vy)
    locations.append((px, py))
    velocities.append((vx, vy))

xlim = 101
ylim = 103

for second in range(1, 100000000000):
    new_locations = []
    for location, velocity in zip(locations, velocities):
        px, py = location
        vx, vy = velocity
        if px + vx < xlim and px + vx >= 0:
            px_new = px + vx
        else:
            px_new = (px + vx) % xlim
        if py + vy < ylim and py + vy >= 0:
            py_new = py + vy
        else:
            py_new = (py + vy) % ylim
        new_locations.append((px_new, py_new))
    locations = new_locations
    if len(set(locations)) == 500:
        a = np.zeros((xlim, ylim))
        for location in locations:
            a[location] = 1
        print(second, '\n')
        for _ in a:
            print(''.join([str(int(q)) for q in _]))
    
top_left = 0
top_right = 0
bottom_left = 0
bottom_right = 0
for location in locations:
    px, py = location
    if px < xlim // 2 and py < ylim // 2:
        top_left += 1
    elif px < xlim // 2 and py > ylim // 2:
        top_right += 1
    elif px > xlim // 2 and py < ylim // 2:
        bottom_left += 1
    elif px > xlim // 2 and py > ylim // 2:
        bottom_right += 1
        
print(top_left*top_right*bottom_left*bottom_right)