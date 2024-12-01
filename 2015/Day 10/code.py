data = '1113222113'

def look_say(in_str):
    if len(in_str) == 1:
        out_str = '1' + in_str
        return out_str
    else:
        out_str = ''
        previous_chr = in_str[0]
        counter = 0
        for i, chr in enumerate(in_str):
            if chr == previous_chr and i < len(in_str) - 1:
                counter += 1
            elif chr == previous_chr and i == len(in_str) - 1:
                counter += 1
                out_str += str(counter) + chr
                return out_str
            elif chr != previous_chr and i == len(in_str) - 1:
                out_str += str(counter) + previous_chr + '1' + chr
                return out_str
            else:
                out_str += str(counter) + previous_chr
                counter = 1
            previous_chr = chr
        
for x in range(50):
    data = look_say(data)
    
print(len(data))