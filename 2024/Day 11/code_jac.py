data = '5 62914 65 972 0 805922 6521 1639064'

stones = data.split(' ')
stone_babies = {'0': ['1']}
stone_counter = {stone:1 for stone in stones}
for blink in range(75):
    stone_list = list(stone_counter.keys())
    new_counter = {}
    for s in stone_list:
        if s in stone_babies:
            for baby in stone_babies[s]:
                if baby in new_counter:
                    new_counter[baby] += stone_counter[s]
                else:
                    new_counter[baby] = stone_counter[s]
        else:
            if len(s) % 2 == 0:
                l = str(int(s[:len(s) // 2]))
                r = str(int(s[len(s) // 2:]))
                stone_babies[s] = [l, r]
            else:
                stone_babies[s] = [str(int(s) * 2024)]
            for baby in stone_babies[s]:
                if baby in new_counter:
                    new_counter[baby] += stone_counter[s]
                else:
                    new_counter[baby] = stone_counter[s]
    stone_counter = new_counter
                
print(sum([x[1] for x in stone_counter.items()]))