import re

with open('input_jac.txt') as f:
    data = [d.strip().split(':')[-1].split('|') for d in f.readlines()]
    
winning_candidate_num_lists = [([int(n) for n in re.findall(r'\d+', d[0])], [int(n) for n in re.findall(r'\d+', d[-1])]) for d in data]

print(sum([1*2**(len(set(i[0]) & set(i[1])) - 1) if len(set(i[0]) & set(i[1])) > 0 else 0 for i in winning_candidate_num_lists]))

scores = [len(set(i[0]) & set(i[1])) for i in winning_candidate_num_lists]

card_count = {k: 1 for k in range(len(scores))}
for i, score in enumerate(scores):
    for c in range(i + 1, i + score + 1):
        card_count[c] += card_count[i]
        
print(sum(card_count.values()))