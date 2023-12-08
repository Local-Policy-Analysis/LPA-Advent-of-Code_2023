# An attempt to do it differently to Peter, currently failing

lines = [line.rstrip().split() for line in open("inputs/day7_majr.txt")]
ex = [['32T3K', '765'],['T55J5', '684'],['KK677', '28'],['KTJJT', '220'],['QQQJA', '483']]

def carddiff(l,r):
    cardvals = "23456789TJQKA"
    try:
        return [d for d in [cardvals.index(l[0][i]) - cardvals.index(r[0][i]) for i in range(5)] if d][0]
    except IndexError:
        return 0

def cmp(l, r):
    n = [len(set(l[0])),len(set(r[0]))] # counts of unique cards /hand 
    d = [max([hand[0].count(card) for card in hand[0]]) for hand in [l,r]] # counts of duplicates /hand 

    if n[0] != sum(n)/2: # types are different
        return n.index(min(n)) > 0 and -1 or 1
    elif (n[0] in [2,3]) and d[0] != sum(n)/2: # one is foak and one is fh OR one is toak and one is 2pair
        return d.index(max(d)) > 0 and -1 or 1
    else: # different card values or hands are the same
        return carddiff(l,r)

from functools import cmp_to_key as ck
ranks = sorted(lines, key=ck(cmp))

#print(ranks)

print(sum([(i+1)*int(h[1]) for i,h in enumerate(ranks)])) 

