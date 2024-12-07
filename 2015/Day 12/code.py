import re

with open('input_jac.txt') as f:
    data = f.read()
    
negatives = sum([int(n) for n in re.findall('-[0-9]+', data)])
positives = sum([int(n) for n in re.findall('[^-|0-9]([0-9]+)', data)])
print(negatives + positives)

# if encounter a second opening brace before a red flag then reset opening brace count and
# remove last element from starts

open_brackets = 0
close_brackets = 0
red_flag = False
starts = []
ends = []
reds = []
red_flag = False
for x in range(len(data)):
    if data[x] == '{' and  open_brackets == 0:
        open_brackets += 1
        starts.append(x)
    elif data[x] == '{' and  open_brackets != 0:
        open_brackets += 1
    elif data[x] == '}' and close_brackets + 1 == open_brackets:
        ends.append(x)
        reds.append(red_flag)
        open_brackets = 0
        close_brackets = 0
        red_flag = False
    elif data[x] == '}' and close_brackets + 1 != open_brackets:
        close_brackets += 1
    elif data[x:x+6] == ':"red"':
        red_flag = True
    
pt2 = 0        
for s, e, r in zip(starts, ends, reds):
    if r:
        pt2 += sum([int(n) for n in re.findall('-[0-9]+', data[s:e])]) + sum([int(n) for n in re.findall('[^-|0-9]([0-9]+)', data[s:e])])

print(negatives + positives - pt2)    