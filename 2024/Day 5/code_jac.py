with open('input_jac.txt') as f:
    rules, updates = f.read().split('\n\n')
    
rules = [(int(r.split('|')[0]), int(r.split('|')[1])) for r in rules.split('\n')]
updates = [[int(n) for n in u.split(',')] for u in updates.split('\n')]

def check(update):
    for r in rules:
        x, y = r
        if x in u and y in u:
            if u.index(x) > u.index(y):
                return 0
    return update[int((len(update) - 1) / 2)]

def bubbles(update):
    updates = 1
    while updates:
        updates = 0
        for rule in rules:
            x, y = rule
            if x in update and y in update:
                x_index = update.index(x)
                y_index = update.index(y)
                if x_index > y_index:
                    update = update[:y_index] + [x] + update[y_index+1:x_index] + [y] + update[x_index+1:]
                    updates += 1
    return update[int((len(update) - 1) / 2)]

pt1 = 0
pt2 = 0
for u in updates:
    n = check(u)
    pt1 += n
    if not n:
        pt2 += bubbles(u)
    
print(pt1)
print(pt2)