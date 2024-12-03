with open("inputs/day_15_pbr.txt") as file:
  lines = [line.rstrip().split(",") for line in file][0]

def hash_1(s):
  out = 0
  for x in s:
    out += ord(x)
    out *= 17
    out %= 256
  return out

print(f"Part 1: {sum([hash_1(x) for x in lines])}")

# This is not space efficient, but it is easy
hm = [[] for _ in range(256)]
for x in lines:
  if x.count("=") > 0:
    var, num = x.split("=")
    h = hash_1(var)
    replaced = 0
    for i in range(len(hm[h])):
      if hm[h][i][0] == var:
        hm[h][i] = (var, num)
        replaced = 1
        break
    if not replaced:
      hm[h].append((var, num))
  else:
    var = x[:-1]
    h = hash_1(var)
    for i in range(len(hm[h])):
      if hm[h][i][0] == var:
        del hm[h][i] #This only works because we know that each element cannot occur twice
        break

out = 0
for i, _ in enumerate(hm):
  for j, y in enumerate(hm[i]):
    out += (1 + i) * (1 + j) * int(y[1])
print(f"Part 2: {out}")