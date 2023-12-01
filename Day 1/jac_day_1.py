import re

with open('input_jac.txt') as f:
    data = [d.strip() for d in f.readlines()]
    
print(sum([int(re.findall(r'\d', row)[0] + re.findall(r'\d', row)[-1]) for row in data]))

text_to_digit_dict = {'one': '1',
                      'two': '2',
                      'three': '3',
                      'four': '4',
                      'five': '5',
                      'six': '6',
                      'seven': '7',
                      'eight': '8',
                      'nine': '9',
                      '1': '1',
                      '2': '2',
                      '3': '3',
                      '4': '4',
                      '5': '5',
                      '6': '6',
                      '7': '7',
                      '8': '8',
                      '9': '9',
                      'eno': '1',
                      'owt': '2',
                      'eerht': '3',
                      'ruof': '4',
                      'evif': '5',
                      'xis': '6',
                      'neves': '7',
                      'thgie': '8',
                      'enin': '9'}

pttn = r'\d|one|two|three|four|five|six|seven|eight|nine|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin'
print(sum([int(text_to_digit_dict[re.findall(pttn, row)[0]] + text_to_digit_dict[re.findall(pttn, row[::-1])[0]]) for row in data]))

    

