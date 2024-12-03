data = [[int(e) for e in l.split(" ")] for l in open("inputs/day9_majr.txt").read().splitlines()]

### Part 1
def predict(series):
    if all(e==0 for e in series):
        return 0
    else:
        return series[-1] + predict([series[i]-series[i-1] for i in range(1,len(series))])

print(sum([predict(l) for l in data]))

### Part 2
def redict(series):
    if all(e==0 for e in series):
        return 0
    else:
        return series[0] - redict([series[i]-series[i-1] for i in range(1,len(series))])

print(sum([redict(l) for l in data]))