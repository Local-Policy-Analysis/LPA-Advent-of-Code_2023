import os
from operator import itemgetter

os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 7')

with open('input_jac.txt') as f:
    data = [d.strip().split(' ') for d in f.readlines()]

replacements = {'A': 'a',
                'K': 'b',
                'Q': 'c',
                'J': 'd',
                'T': 'e',
                '9': 'f',
                '8': 'g',
                '7': 'h',
                '6': 'i',
                '5': 'j',
                '4': 'k',
                '3': 'l',
                '2': 'm',
                }    

replacements_pt2 = {'A': 'a',
                    'K': 'b',
                    'Q': 'c',
                    'J': 'z',
                    'T': 'e',
                    '9': 'f',
                    '8': 'g',
                    '7': 'h',
                    '6': 'i',
                    '5': 'j',
                    '4': 'k',
                    '3': 'l',
                    '2': 'm',
                    }    

hands_only = [d[0] for d in data]
bids = [int(d[1]) for d in data]

# replace values in hands so that they are easily alphabetically sorted
hands = '-'.join(hands_only)
for key, value in replacements.items():
    hands = hands.replace(key, value)
hands = hands.split('-')

# replace values in hands so that they are easily alphabetically sorted
hands_pt2 = '-'.join(hands_only)
for key, value in replacements_pt2.items():
    hands_pt2 = hands_pt2.replace(key, value)
hands_pt2 = hands_pt2.split('-')

# recombine data
data = [(hand, bid) for hand, bid in zip(hands, bids)]
data_pt2 = [(hand, bid) for hand, bid in zip(hands_pt2, bids)]

# sort alphabetically
data = sorted(data, key=lambda x: x[0], reverse=True)
data_pt2 = sorted(data_pt2, key=lambda x: x[0], reverse=True)

# sort by hand order
data = sorted(data, key=lambda x: (max([x[0].count(v) for v in set(x[0])]), 0 if len(set(x[0])) == 1 else sorted([x[0].count(v) for v in set(x[0])])[1]))

# 2 pairs
data_pt2 = sorted(data_pt2, key=lambda x: 0 if len(set(x[0])) == 1 else 0 if len(set(x[0]).difference(set('z'))) == 1 else sorted([x[0].count(v) for v in set(x[0]).difference(set('z'))])[-2])
# hand strength
data_pt2 = sorted(data_pt2, key=lambda x: (5 if len(set(x[0])) == 1 else max([x[0].count(v) + x[0].count('z') for v in set(x[0]).difference(set('z'))])))

print(sum([d[1] * (i + 1) for i, d in enumerate(data)]))
print(sum([d[1] * (i + 1) for i, d in enumerate(data_pt2)]))
    
