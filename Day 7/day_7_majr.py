# Using a comparator function from the old days...

lines = [line.rstrip().split() for line in open("inputs/day_7_pbr.txt")]

def handcardval(h):
    cardvals = "23456789TJQKA"
    return int( ''.join( str(x) for x in [cardvals.index(c) for c in h[0]]))

def cmp(l, r):
    h = [l,r] #hands
    u = [set(l[0]), set(r[0])] # unique cards /hand
    ul = [len(u[0]),len(u[1])] # counts of unique cards /hand 
    c = [max([hand[0].count(card) for card in hand[0]]) for hand in h] # counts of duplicates /hand (for toak vs 2pair)
    bvc = [handcardval(l), handcardval(r)] # best value card /hand
    return ul[0] != sum(ul)/2 and (ul.index(min(ul)) > 0 and -1 or 1)  or (ul[0] == 3 and c[0] != sum(c)/2) and (c.index(max(c)) > 0 and -1 or 1) or bvc[0] != sum(bvc)/2 and (bvc.index(max(bvc)) > 0 and -1 or 1) or 0


from functools import cmp_to_key as ck
ranks = sorted(lines, key=ck(cmp))

print(sum([(i+1)*int(h[1]) for i,h in enumerate(ranks)])) 
## Different answer to Peter's

