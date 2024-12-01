import re

with open('input_7.txt') as f:
    data = [d.strip() for d in f.readlines()]

def bitwise_not(n):
    return (1 << 16) - 1 - n
        
wires = {}
while 'a' not in wires:
    for d in data:
        if 'AND' in d:
            arg1, logic, arg2, arrow, wire = d.split(' ')
            if arg1 in wires and arg2 in wires:
                wires[wire] = wires[arg1] & wires[arg2]
            elif re.findall(r'[0-9]', arg1) and arg2 in wires:
                wires[wire] = int(arg1) & wires[arg2]
        elif 'OR' in d:
            arg1, logic, arg2, arrow, wire = d.split(' ')
            if arg1 in wires and arg2 in wires:
                wires[wire] = wires[arg1] | wires[arg2]
        elif 'LSHIFT' in d:
            arg1, logic, arg2, arrow, wire = d.split(' ')
            if arg1 in wires:
                wires[wire] = wires[arg1] << int(arg2)
        elif 'RSHIFT' in d:
            arg1, logic, arg2, arrow, wire = d.split(' ')
            if arg1 in wires:
                wires[wire] = wires[arg1] >> int(arg2)
        elif 'NOT' in d:
            logic, arg1, arrow, wire = d.split(' ')
            if arg1 in wires:
                wires[wire] = bitwise_not(wires[arg1])
        else:
            arg1, arrow, wire = d.split(' ')
            if arg1 in wires:
                wires[wire] = wires[arg1]
            elif re.findall(r'[0-9]', arg1):
                wires[wire] = int(arg1)
            
print(wires['a'])