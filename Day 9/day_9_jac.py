import os

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 9')

with open('input_jac.txt') as f:
    data = [d.strip().split(' ') for d in f.readlines()]
data = [[int(n) for n in d] for d in data]
    
def get_next(series):
    result = series[-1]
    expanded_series = []
    expansion = series
    while expansion.count(0) != len(expansion):
        expansion = [expansion[i + 1] - expansion[i] for i in range(len(expansion[:-1]))]
        expanded_series.append(expansion)
    last_terms = [expanded[-1] for expanded in expanded_series]
    return series[-1] + sum(last_terms)


print(sum(get_next(series) for series in data))
print(sum(get_next(series[::-1]) for series in data))