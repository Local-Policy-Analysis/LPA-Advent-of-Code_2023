## Part1. A chance to igraph in python!
data = open("inputs/day8_majr.txt").read().splitlines()

from collections import deque
pth = deque(data.pop(0))
data.pop(0) # blank line

## nodes
vs = [es.split()[0] for es in data]

## edges 
import re
from itertools import chain
node_re = '([A-Z]{3})'
nodenames = [re.findall(node_re,line) for line in data]
es = list(
    chain.from_iterable(
        [[(nds[0], nds[1], 'L'),(nds[0],nds[2],'R')] for nds in nodenames]
)) 

## graph
import igraph as ig
g = ig.Graph(n=len(vs), edges=[(vs.index(e[0]), vs.index(e[1])) for e in es], directed=True)
g.vs["lbl"] = vs
g.es["fork"] = [e[2] for e in es]

def count_steps(g):
    ## starting conditions
    start_nd = "AAA"
    end_nd = "ZZZ"
    n = 0
    fork = pth[0]
    nd = g.vs.find(lbl = start_nd)

    ## traverse
    while nd["lbl"] != end_nd:
        nd = g.vs[g.es.find(_source=nd,fork=fork).target]
        n = n+1
        pth.rotate(-1)
        fork = pth[0]
    return n

print(count_steps(g))

## Part2
import math

#reset path
pth0 = deque(open("inputs/day8_majr.txt").read().splitlines()[0])

def count_steps2(g,start_nd):
    ## starting conditions
    pth=copy.deepcopy(pth0)
    n = 0
    fork = pth[0]
    nd = start_nd

    ## traverse
    while not nd["lbl"].endswith('Z'):
        nd = g.vs[g.es.find(_source=nd,fork=fork).target]
        n = n+1
        pth.rotate(-1)
        fork = pth[0]
    return n

print(math.lcm(*[count_steps2(g,v) for v in g.vs if v['lbl'].endswith('A')]))
