with open('test_jac.txt') as f:
    data = [d.strip() for d in f.readlines()]
    
A = int(data[0].split(': ')[1])
B = int(data[1].split(': ')[1])
C = int(data[2].split(': ')[1])
opcodes = [int(d) for d in data[4].split(': ')[1].split(',')]
pointer = 0
outputs = []
combo = {0:0, 1:1, 2:2, 3:3, 4:A, 5:B, 6:C, 7:None}

while pointer < len(opcodes):
    opcode = opcodes[pointer]
    operand = opcodes[pointer + 1]
    if opcode == 0:
        operand = combo[operand]
        combo[4] = int(combo[4] / 2 ** operand)
    elif opcode == 1:
        combo[5] = combo[5] ^ operand
    elif opcode == 2:
        operand = combo[operand]
        combo[5] = operand % 8
    elif opcode == 3 and combo[4] != 0:
        pointer = operand
    elif opcode == 3 and combo[4] == 0:
        pointer += 2
    elif opcode == 4:
        combo[5] = combo[5] ^ combo[6]
    elif opcode == 5:
        operand = combo[operand]
        outputs.append(str(operand % 8))
    elif opcode == 6:
        operand = combo[operand]
        combo[5] = int(combo[4] / 2 ** operand)
    elif opcode == 7:
        operand = combo[operand]
        combo[6] = int(combo[4] / 2 ** operand)
    if opcode != 3:
        pointer += 2
    
print(','.join(outputs))

    
# test -> 4,6,3,5,6,3,5,2,1,0