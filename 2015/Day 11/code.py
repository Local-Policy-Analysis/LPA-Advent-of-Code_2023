import string
data = 'hxbxwxba'

num_to_str = {n:c for n, c in zip(range(26), string.ascii_lowercase)}
str_to_num = {c:n for n, c in zip(range(26), string.ascii_lowercase)}

# must have at least 1 run of 3 consecutive letters
# must not contain 1, o, or l
# must have at least 2 non-overlapping pairs of letters

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
    pass