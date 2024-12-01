import numpy as np

with open('input_jac.txt') as f:
    data = [(int(d.strip().split('   ')[0]), int(d.strip().split('   ')[1])) for d in f.readlines()]
    
list1 = sorted([x[0] for x in data])
list2 = sorted([x[1] for x in data])

print(sum([abs(x - y) for x, y in zip(list1, list2)]))

unique, counts = np.unique(list2, return_counts=True)
list2_counts = dict(zip(unique, counts))

print(sum([n * list2_counts[n] for n in list1 if n in list2_counts]))