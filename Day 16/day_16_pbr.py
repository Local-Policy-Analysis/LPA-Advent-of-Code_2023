with open("inputs/day_16_pbr.txt") as file:
  lines = [line.rstrip() for line in file]

# Could try and use parallel processing, but actually Python doesn't support it anyway

def try_start(vector):
  memo = [[[] for _ in lines[0]] for _ in lines]
  memo[vector[0][0]][vector[0][1]] = [vector[1]]

  # Store each ray as (curr tile(y,x), direction vector(y,x))
  rays = [vector]

  loop = 0
  while len(rays) > 0 and loop < 1000:
    for i in range(len(rays)):
      ray = rays[i]
      curr = lines[ray[0][0]][ray[0][1]]
      match curr:
        case ".":
          rays[i] = ((ray[0][0] + ray[1][0],ray[0][1] + ray[1][1]),ray[1])
        case "/":
          rays[i] = ((ray[0][0] - ray[1][1], ray[0][1] - ray[1][0]),(-ray[1][1],-ray[1][0]))
        case "\\":
          rays[i] = ((ray[0][0] + ray[1][1], ray[0][1] + ray[1][0]),(ray[1][1],ray[1][0]))
        case "|":
          if abs(ray[1][1]) == 1:
            rays.append(((ray[0][0] - 1,ray[0][1]),(-1,0)))
            rays[i] = ((ray[0][0] + 1,ray[0][1]),(1,0))
          else:
            rays[i] = ((ray[0][0] + ray[1][0],ray[0][1] + ray[1][1]),ray[1])
        case "-":
          if abs(ray[1][0]) == 1:
            rays.append(((ray[0][0],ray[0][1] - 1),(0,-1)))
            rays[i] = ((ray[0][0],ray[0][1] + 1),(0,1))
          else:
            rays[i] = ((ray[0][0] + ray[1][0],ray[0][1] + ray[1][1]),ray[1])
    rays = [ray for ray in rays if (all([i >= 0 for i in ray[0]]) and (ray[0][0] < len(lines)) and (ray[0][1] < len(lines[1])))]
    rays = [ray for ray in rays if (not (ray[1] in memo[ray[0][0]][ray[0][1]]))]
    for ray in rays:
      memo[ray[0][0]][ray[0][1]].append(ray[1])
    loop += 1

  energised = 0
  for x in memo:
    for y in x:
      if len(y) > 0:
        energised += 1
  return(energised)

best = [((0,0),(0,1)), try_start(((0,0),(0,1)))]

print(f"Part 1: {best[1]}")

for x in range(len(lines[0])):
  t = try_start(((0,x),(1,0)))
  q = try_start(((len(lines) - 1, x),(-1,0)))
  if t > best[1]:
    best = [((0,x),(0,1)),t]
  if q > best[1]:
    best = [((len(lines) - 1, x),(-1,0)),q]
for y in range(len(lines)):
  t = try_start(((y,0),(0,1)))
  q = try_start(((y, len(lines[0]) - 1),(0,-1)))
  if t > best[1]:
    best = [((y,0),(0,1)),t]
  if q > best[1]:
    best = [((y, len(lines[0]) - 1),(0,-1)),q]
print(f"Part 2: {best[1]}")