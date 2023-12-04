with open("../inputs/day_3.txt") as file:
  lines = [line.rstrip() for line in file]

def getSurrounds(arr, line, start, stop):
    surrounds = ""
    if start > 0:
        surrounds += arr[line][start - 1]
    else: start += 1
    if stop < (len(arr[0]) - 1):
        surrounds += arr[line][stop + 1]
    else:  stop -= 1
    if line > 0:
        surrounds += arr[line - 1][start-1:stop+2]
    if line < len(arr) - 1:
        surrounds += arr[line + 1][start-1:stop+2]
    return(surrounds)     

total = 0
for x in range(len(lines)):
    start, stop = (-1,-1)
    for y in range(len(lines[x])):
        if lines[x][y].isnumeric():
            stop = y
            if start == -1:
                start = y
        if (not(lines[x][y].isnumeric()) or (y == len(lines[x]) - 1)) and start != -1 :
            sur = getSurrounds(lines, x, start, stop)
            if sur != (len(sur) * "."):
                total += int(lines[x][start:stop+1])
            start, stop = (-1, -1)
print(total)