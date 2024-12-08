with open('input_jac.txt') as f:
    data = [d.strip().split(': ') for d in f.readlines()]
  
  
def merge(x, y):
    return int(str(x) + str(y))

pt1 = 0  
for d in data:
    result = int(d[0])
    arguments = [int(n) for n in d[1].split(' ')]
    running_totals = [arguments[0]]
    for a in arguments[1:]:
        temp_totals = [total + a for total in running_totals]
        temp_totals.extend([total * a for total in running_totals])
        # for part2
        temp_totals.extend([merge(total, a) for total in running_totals])
        running_totals = temp_totals.copy()
    if result in running_totals:
        pt1 += result
        
print(pt1)
