import re

with open('input_jac.txt') as f:
    data = f.read()

print(sum([int(d[0]) * int(d[1]) for d in re.findall(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)', data)]))

pt2 = 0
flag = True
start = [0]
end = []
for i in range(len(data)):
    if data[i: i + 7] == "don't()" and flag:
        flag = False
        end.append(i)
    elif data[i: i + 4] == "do()" and not flag:
        flag = True
        start.append(i)
if start[-1] > end[-1]:
    end.append(len(data))
    
for s, e in zip(start, end):
    pt2 += sum([int(m[0]) * int(m[1]) for m in re.findall(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)', data[s:e])])
print(pt2)