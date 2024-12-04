import numpy as np

with open('input_jac.txt') as f:
    data = np.array([list(d.strip()) for d in f.readlines()])
    
pt1 = 0
for x in range(data.shape[0]):
    for y in range(data.shape[1]):
        if x + 4 <= data.shape[0]:
            if ''.join(data[x:x+4, y]) == 'XMAS' or ''.join(data[x:x+4, y]) == 'SAMX':
                pt1 += 1
        if y + 4 <= data.shape[1]:
            if ''.join(data[x, y:y+4]) == 'XMAS' or ''.join(data[x, y:y+4]) == 'SAMX':
                pt1 += 1
        if x + 4 <= data.shape[0] and y + 4 <= data.shape[1]:
            if ''.join(np.diag(data[x:x+4, y:y+4])) == 'XMAS' or ''.join(np.diag(data[x:x+4, y:y+4])) == 'SAMX':
                pt1 += 1
        if x + 4 <= data.shape[0] and y + 4 <= data.shape[1]:
            if ''.join(np.diag(np.rot90(data[x:x+4, y:y+4]))) == 'XMAS' or ''.join(np.diag(np.rot90(data[x:x+4, y:y+4]))) == 'SAMX':
                pt1 += 1

pt2 = 0
pttm = np.array([])
for x in range(data.shape[0]):
    for y in range(data.shape[1]):
        if x + 3 <= data.shape[0] and y + 3 <= data.shape[1]:
            box = data[x: x+3, y: y+3]
            if (''.join(np.diag(box)) == 'MAS' or ''.join(np.diag(box)) == 'SAM') and (''.join(np.diag(np.rot90(box))) == 'MAS' or ''.join(np.diag(np.rot90(box))) == 'SAM'):
                pt2 += 1
            
print(pt1)
print(pt2)