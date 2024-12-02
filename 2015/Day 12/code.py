import re

with open('input_jac.txt') as f:
    data = f.read()
    
negatives = sum([int(n) for n in re.findall('-[0-9]+', data)])
positives = sum([int(n) for n in re.findall('[^-|0-9]([0-9]+)', data)])
print(negatives + positives)