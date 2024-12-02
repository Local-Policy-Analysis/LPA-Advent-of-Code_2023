with open('input_jac.txt') as f:
    data = [[int(n) for n in d.strip().split(' ')] for d in f.readlines()]
    
differences = [[x - y for x, y in zip(d[:-1], d[1:])] for d in data]

pt1 = 0
pt2 = 0
for d, diff in zip(data, differences):
    abs_diff = [abs(n) for n in diff]
    if max(abs_diff) < 4 and (max(diff) < 0 or min(diff) > 0):
        pt1 += 1
    else:
        for i in range(len(d)):
            temp_d = d[:i] + d[i + 1:]
            temp_diff = [x - y for x, y in zip(temp_d[:-1], temp_d[1:])]
            temp_abs_diff = [abs(n) for n in temp_diff]
            if max(temp_abs_diff) < 4 and (max(temp_diff) < 0 or min(temp_diff) > 0):
                pt2 += 1
                break
        
print(pt1)
print(pt1 + pt2)
