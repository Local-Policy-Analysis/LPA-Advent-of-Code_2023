import string
import re

# data = 'hxbxwxba'
data = 'hxbxxyzz'

num_to_str = {n:c for n, c in zip(range(26), string.ascii_lowercase)}
str_to_num = {c:n for n, c in zip(range(26), string.ascii_lowercase)}

consecutive = [string.ascii_lowercase[i: i+3] for i, s in enumerate(string.ascii_lowercase[:-2])]

def increment(in_str):
    out_str = in_str
    for i, chr in enumerate(reversed(in_str)):
        if chr != 'z':
            if i == 0:
                return out_str[:-(i + 1)] + num_to_str[str_to_num[chr] + 1]
            else:
                return out_str[:-(i + 1)] + num_to_str[str_to_num[chr] + 1] + out_str[-i:]
        else:
            if i == 0:
                out_str = in_str[:-(i + 1)] + 'a'
            else:
                out_str = in_str[:-(i + 1)] + 'a' + out_str[-i:]
        
def check(in_str):
    if any(['i' in in_str, 'o' in in_str, 'l' in in_str]):
        return False
    elif len(re.findall(r'(.)\1{1}', in_str)) < 2:
        return False
    else:
        for c in consecutive:
            if c in in_str:
                return True
    return False

data = increment(data)
while not check(data):
    data = increment(data)
    
print(data)