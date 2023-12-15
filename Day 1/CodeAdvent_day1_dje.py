import re
import numpy as np
from icecream import ic

#test inputs

input_list = []

total = 0

file_path = '../inputs/day_1_dje.txt'
with open(file_path, 'r') as file:
    for line in file:
        input_list.append(line.strip())

for row in input_list:
    numbers = re.findall(r'\d+', row)
    first_num = numbers[0][0]
    last_num = numbers[-1][-1]
    output = first_num + last_num
    output = int(output)
    total = total + output
    ic(total)

ic(total)