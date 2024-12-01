import re

with open('input.txt') as f:
    data = [d.strip() for d in f.readlines()]
    
result = 0
result2 = 0
for d in data:
    backslashes = len(re.findall(r'\\\\', d))
    quotes = len(re.findall(r'\\\"(?=.)', d))
    hexidec = len(re.findall(r'[\"|\w]\\x(?=\w{2})', d)) * 3 + len(re.findall(r'\\\\\\x\w{2}', d)) * 3
    result += 2 + backslashes + quotes + hexidec
    result2 += 4 + backslashes * 2 + quotes * 2 + hexidec / 3

print(result)
print(int(result2))
