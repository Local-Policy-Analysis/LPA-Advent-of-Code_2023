import igraph
from functools import reduce
#with open("inputs/day_19_pbr.txt") as file:
with open("Day 19/test.txt") as file:
  lines = [line.rstrip() for line in file]

# Deeply unsafe solution
wf = {}
x,m,a,s = (0,0,0,0)
i = 0
names = []

while lines[i] != "":
  nm, inst = lines[i].split("{")
  wf[nm] = [x.split(":") for x in inst[:-1].split(",")]
  i += 1


i += 1
t = 0
tot = 0
while i < len(lines):
  for text in lines[i][1:-1].split(","):
    exec(text)
  out = "in"
  while not(out in ["A", "R"]):
    for y in wf[out]:
      if len(y) > 1: 
        exec("t= " + y[0])
        if t:
            out = y[1]
            break
        else:
          pass
      else:
        out = y[0]
  if out == "A":
    n = x + m + a + s
    tot += n
  i += 1
print(f"Part 1: {tot}")

g = igraph.Graph(directed = True)
g.add_vertices(list(wf.keys()), attributes = {"restrictions" : [[[4000,0], [4000,0],[4000,0],[4000,0]]], "to_combine": [[]]})
g.add_vertices(["A", "R"], attributes = {"restrictions" : [[[0, 4000], [0,4000],[0,4000],[0,4000]]], "to_combine" : [[]]})

def parse_requirement(r, inv):
  xmap = "xmas"
  letter = r[0]
  sign = r[1]
  num = int(r[2:])
  out = [[1,4000],[1,4000],[1,4000],[1,4000]]
  if sign == "<": sign = 1
  else: sign = -1
  if not inv:
    num -= sign
  else:
    sign = -sign
  if sign == -1 : sign = 0
  out[xmap.index(letter)][sign] = num
  return(out)

# These combination functions miss when there's a gap, e.g.
# 1-10 or 12-4000 will go to A

def combine_requirements_red(r_1, r_2):
  return([[max(y[0]), min(y[1])]for y in [list(zip(*x)) for x in zip(r_1,r_2)]])

def combine_requirements_inc(r_1, r_2):
  return([[min(y[0]), max(y[1])]for y in [list(zip(*x)) for x in zip(r_1,r_2)]])

for key, value in wf.items():
  g.add_edges([(key, x[1]) for x in value[:-1]], attributes = {"restrictions": [parse_requirement(x[0], 0) for x in value[:-1]]})
  g.add_edges([(key,value[-1][0])], attributes = {"restrictions": [reduce(combine_requirements_red, [parse_requirement(x[0], 1) for x in value[:-1]])]})


g.delete_vertices("R")
t = g.vcount()
print(f"t : {t}")
while True:
  for n in g.vs:
    if g.degree(n, mode ="out") == 0 and n["name"] != "A":
      g.delete_vertices(n)
  q = g.vcount()
  if t == q:
    break
  t = q
igraph.plot(g, "out1.png")
l = 0
# The remaining node with no nodes leaving must be A
while g.vcount() > 1 and l < 1000:
  visited = []
  for n in g.vs:
    if g.degree(n, mode = "out") == 0:
      if len(n["to_combine"]) > 0:
        n["restrictions"] = reduce(combine_requirements_inc, n["to_combine"] + [n["restrictions"]])
      print(f'{n["name"]} {n["restrictions"]}')
      print(n["to_combine"])
      for z in g.es.select(_target=n):
        z["restrictions"] = combine_requirements_red(z["restrictions"], n["restrictions"])
        g.vs[z.source]["to_combine"] = g.vs[z.source]["to_combine"] + [z["restrictions"]]
        g.vs[z.source]["restrictions"] = combine_requirements_inc(g.vs[z.source]["restrictions"], z["restrictions"])
      print("--")
      visited.append(n)
  g.delete_vertices(visited)
  l += 1

for n in g.vs:
  print("beep")
  print(n)
print(f"t : {t}")

# This doesn't order things properly. Sorry future Peter
def combine_requirements_test(r_1, r_2):
  rt = []
  for i in range(4):
    out = []
    j = 0
    for x in r_1[i]:
      while r_2[i][j][0] < x[0] and j < len(r_2[i]) - 1:
        out = out + [r_2[i][j]]
        j += 1
      out = out + [x]
    if j < len(r_2[i]):
      out = out + r_2[i][j:]
    if len(out) > 1:
      tmp = []
      i = 0
      while i < len(out) - 1:
        j = 1
        while out[i][1] > out[i+j][0] and i + j < len(out) - 1:
            j += 1
        tmp = tmp + [(out[i][0], out[i+j][1])]
        print(tmp)
        i += 1


    rt +=  [out]
  return(rt)

  return([[max(y[0]), min(y[1])]for y in [list(zip(*x)) for x in zip(r_1,r_2)]])

t1 = [[(1, 200), (1450,4000)], [(1, 4000)], [(1, 4000)], [(1, 4000)]]
t2 = [[(1400, 4000)], [(1, 4000)], [(1, 4000)], [(1, 4000)]]
print(combine_requirements_test(t1,t2))