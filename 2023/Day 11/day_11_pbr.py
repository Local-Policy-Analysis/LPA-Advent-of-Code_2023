with open("inputs/day_11_pbr.txt") as file:
  lines = [line.rstrip() for line in file]

# find indices of columns with only dots.
dotCols = [-1] + [i for i in range(len(lines[0])) if all([lines[j][i] == "." for j in range(len(lines))])]
dotRows = [-1] + [i for i in range(len(lines)) if all([lines[i][j] == "." for j in range(len(lines[0]))])]

def makeStars(size):
  stars = []
  i, j, colsPeg, rowsPeg = (0, 0, 0, 0)
  while i < len(lines):
    while (rowsPeg <  len(dotRows) - 1) and dotRows[rowsPeg + 1] < i:
      rowsPeg += 1
    while j < len(lines[i]):
      if lines[i][j] == "#":
        while (colsPeg <  len(dotCols) - 1) and dotCols[colsPeg + 1] < j:
          colsPeg += 1
        stars.append((i + rowsPeg*size, j + colsPeg*size))
      j += 1
    colsPeg = 0
    j = 0
    i += 1
  return(stars)

stars = makeStars(1)
dist = 0
for i in range(len(stars) - 1):
  for j in range(len(stars) - i - 1):
    dist += abs(stars[j + i + 1][0] - stars[i][0]) + abs(stars[j + i + 1][1] - stars[i][1])
print(f"Part 1: {dist}")

stars1 = makeStars(1e6 -1)
dist1 = 0
for i in range(len(stars1) - 1):
  for j in range(len(stars1) - i - 1):
    dist1 += abs(stars1[j + i + 1][0] - stars1[i][0]) + abs(stars1[j + i + 1][1] - stars1[i][1])
print(f"Part 2: {dist1}")