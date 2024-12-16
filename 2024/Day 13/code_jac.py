with open('input_jac.txt') as f:
    data = [d.split('\n') for d in f.read().split('\n\n')]
   
tokens = 0
for d in data:
    a, b, prize = d
    ax, ay = int(a.split('+')[1].split(',')[0]), int(a.split('+')[-1])
    bx, by = int(b.split('+')[1].split(',')[0]), int(b.split('+')[-1])
    px, py = int(prize.split('=')[1].split(',')[0]), int(prize.split('=')[-1])
    px = px + 10000000000000
    py = py + 10000000000000
    
    # ax * ay + bx * ay = px * ay
    # ay * ax + by * ax = py * ax
    # bx * ay = px * ay
    # by * ax = py * ax
    # bx * ay - by * ax = px * ay - py * ax
    # B = (px * ay - py * ax) / (bx * ay - by * ax)
    # ax * A + bx * B = px
    # A = (px - bx * B) / ax
    
    B = (px * ay - py * ax) // (bx * ay - by * ax)
    A = (px - bx * B) // ax
    if ax * A + bx * B == px and ay * A + by * B == py:
        tokens += 3 * A + B
    
    # I am ashamed of the below pt 1, but retain it as a reminder
    # of my inadequacies
    # A = 0
    # possible = False
    # min_tokens = 1000
    # x = 0
    # y = 0
    # while x < prize[0] and y < prize[1]:
    #     x = ax * A
    #     y = ay * A
    #     B = (prize[0] - x) // bx
    #     if ax * A + bx * B == prize[0] and ay * A + by * B == prize[1]:
    #         if A * 3 + B < min_tokens:
    #             min_tokens = A * 3 + B
    #             possible = True
    #     A += 1
    # if possible:
    #     tokens += min_tokens
        
print(tokens)