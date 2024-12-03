import copy

with open("inputs/day_3_pbr.txt") as file:
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

part2 = 0
nums = []
stars = []
for x in range(len(lines)):
    nums.append([])
    at_num = False
    curr_count = [0,0]
    for y in range(len(lines[x])):
        if lines[x][y].isnumeric() and not(at_num):
            curr_count[0] = y
            at_num = True
        if (at_num and not(lines[x][y].isnumeric())):
                curr_count[1] = y
                at_num = False
                nums[x].append(copy.deepcopy(curr_count))
                curr_count = [0,0]
        elif (at_num and y == (len(lines[x]) - 1)):
                curr_count[1] = y + 1
                at_num = False
                nums[x].append(copy.deepcopy(curr_count))
                curr_count = [0,0]
        if lines[x][y] == "*":
            stars.append([x,y])
for star in stars:
    surrounds = []
    if (star[0] > 0):
        for num in nums[star[0] - 1]:
            if (num[0] <= star[1] + 1) and (num[1] >= star[1]):
                surrounds.append(lines[star[0]-1][num[0]:num[1]])
    for num in nums[star[0]]:
        if(num[0] == star[1] + 1) or (num[1] == star[1]):
            surrounds.append(lines[star[0]][num[0]:num[1]])
    if (star[0] < len(lines) - 1):
        for num in nums[star[0] + 1]:
            if (num[0] <= star[1] + 1) and (num[1] >= star[1]):
                surrounds.append(lines[star[0]+1][num[0]:num[1]])
    if len(surrounds) == 2:
        part2 += int(surrounds[0]) * int(surrounds[1])
print(part2)