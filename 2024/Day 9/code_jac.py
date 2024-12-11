with open('input_jac.txt') as f:
    data = f.read()
    
file_sizes = [int(d) for d in data[::2]]
space_sizes = [int(d) for d in list(data[1::2])]
expanded_files = ''.join(['#' * int(f) + '.' * int(s) for f, s in zip(file_sizes, space_sizes)] + ['#'] * int(file_sizes[-1]))
file_ids_with_size = []
for i, s in enumerate(file_sizes):
    for _ in range(s):
        file_ids_with_size.append(i)
sorted_ids = []
for char in expanded_files:
    if char != '.':
        if file_ids_with_size:
            sorted_ids.append(file_ids_with_size.pop(0))
    else:
        if file_ids_with_size:
            sorted_ids.append(file_ids_with_size.pop())

print(sum([i * id for i, id in enumerate(sorted_ids)]))

file_ids = [0] * file_sizes[0]
for i, space_file in enumerate(zip(space_sizes, file_sizes[1:])):
    for _ in range(space_file[0]):
        file_ids.append('.')
    for _ in range(space_file[1]):
        file_ids.append(i + 1)
        
for i, fs in enumerate(reversed(file_sizes)):
    id_being_sorted = len(file_sizes) - 1 - i
    first_idx_of_id_being_sorted = file_ids.index(id_being_sorted)
    for pos in range(first_idx_of_id_being_sorted - fs + 1):
        enough_space = True
        for x in range(pos, pos + fs):
            if file_ids[x] != '.':
                enough_space = False
                break
        if enough_space:
            file_ids = file_ids[:pos] + [id_being_sorted] * fs + file_ids[pos + fs:first_idx_of_id_being_sorted] + ['.'] * fs + file_ids[first_idx_of_id_being_sorted + fs:]
            break
        
print(sum([i * id for i, id in enumerate(file_ids) if id != '.']))