with open('input_jac.txt') as f:
    patterns, designs = f.read().split('\n\n')
    
patterns = patterns.split(', ')
designs = designs.split('\n')
    
valid = 0
for design in designs:
    valid += 1
    
print(valid)
