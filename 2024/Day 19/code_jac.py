with open('input_jac.txt') as f:
    patterns, designs = f.read().split('\n\n')
    
patterns = patterns.split(', ')
designs = designs.split('\n')

memo = {}
def backtrack(design):
    if design not in memo:
        if not design:
            return 1
        else:
            solutions = 0
        candidates = [p for p in patterns if len(p) <= len(design)]
        for candidate in candidates:
            if design[:len(candidate)] != candidate:
                continue
            solutions += backtrack(design[len(candidate):])
        memo[design] = solutions
    return memo[design]

pt1 = 0
pt2 = 0
for design in designs:
    used = []
    valid = backtrack(design)
    if valid:
        pt1 += 1
        pt2 += valid
        
print(pt1)
print(pt2)
    