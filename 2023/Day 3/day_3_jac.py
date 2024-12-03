with open('input_jac.txt') as f:
    data = [d.strip() for d in f.readlines()]
    
nums = []
locations = []
asterisks = []
n = ''
l = []
for x, row in enumerate(data):
    for y, char in enumerate(row):
        if char in '0123456789':
            n += char
            l.append((x, y))
        else:
            if char == '*':
                asterisks.append((x, y))
            if n != '':
                locations.append(l)
                nums.append(int(n))
                n = ''
                l = []
            
adjacency_matrix = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]

pt1 = 0
for num, location in zip(nums, locations):
    test = 0
    for co_ord in location:
        x, y = co_ord
        for adjacent in adjacency_matrix:
            new_x, new_y = adjacent
            if x + new_x >= 0 and x + new_x < 140 and y + new_y >= 0 and y + new_y < 140:
                if data[x + new_x][y + new_y] not in '0123456789.':
                    test += 1
    if test:
        pt1 += num
        
location_number_dict = {k: value for key, value in zip(locations, nums) for k in key}

pt2 = 0
for asterisk in asterisks:
    locations = []
    x, y = asterisk
    for adjacent in adjacency_matrix:
        new_x, new_y = adjacent
        if x + new_x >= 0 and x + new_x < 140 and y + new_y >= 0 and y + new_y < 140:
            if data[x + new_x][y + new_y]  in '0123456789':
                locations.append((x + new_x, y + new_y))
    adjacent_numbers = set()
    for location in locations:
        adjacent_numbers.add(location_number_dict[location])
    if len(adjacent_numbers) == 2:
        a, b = adjacent_numbers
        pt2 += a * b
        
print(pt1)
print(pt2)