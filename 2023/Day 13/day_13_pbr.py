from functools import reduce
import copy

with open("inputs/day_13_pbr.txt") as file:
  lines = [line.rstrip() for line in file]

def findmirror(array, avoid = -1):
  # try and find it vertically
  for i in range(len(array)-1):
    if i+1 == avoid:
      continue
    if reduce(lambda x,y : x and y, map(lambda p, q: p == q, array[i], array[i+1])):
      bottom = array[i+1:]
      top = array[i-(min(i,len(bottom)-1)):i+1]
      bottom = bottom[:len(top)][::-1]
      if(all([reduce(lambda x,y : x and y, map(lambda p, q: p == q, top[j], bottom[j])) for j in range(len(bottom))])):
        return(i + 1)
  return(0)

def swap(x):
  if x == ".":
    return("#")
  else:
    return(".")

def tryswaps(array):
  out = 0
  # Instead of doing this, we could check to see if the mirror could be 
  # affected by the smudge, but that's harder
  v = findmirror(array)
  h = findmirror([[x[i] for x in array]for i in range(len(array[1]))])
  for i in range(len(array)):
    for j in range(len(array[i])):
      new_array = copy.deepcopy(array)
      new_row = list(new_array[i]) # This part can definitely be done in fewer lines
      new_row[j] = swap(new_row[j])
      new_array[i] = "".join(new_row)
      s_v = findmirror(new_array, v)
      if s_v > 0 and s_v != v:
        return(s_v*100)
      s_h = findmirror([[x[i] for x in new_array]for i in range(len(new_array[1]))], h)
      if s_h > 0 and s_h != h:
        return(s_h)

p1 = 0
p2 = 0
array = []
for i, line in enumerate(lines):
  if line == "" or i == (len(lines) - 1):
    if i == (len(lines) - 1): # no
      array.append(line)
    p1 += findmirror(array)*100 #Horizontal mirrors
    p1 += findmirror([[x[i] for x in array]for i in range(len(array[1]))]) # Vertical mirrors
    p2 += tryswaps(array)
    array = []
  else:
    array.append(line)

print(f"Day 1: {p1}")
print(f"Day 2: {p2}")


