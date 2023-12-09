import os
os.chdir('d:\\Users\\jcaddick\\github\\LPA-Advent-of-Code_2023\\Day 5')

with open('input_jac.txt') as f:
    data = f.read().split('\n\n')
    
seeds, *data = [d.split(':')[-1].lstrip() for d in data]
seeds = [int(n) for n in seeds.split(' ')]
seed_ranges = [seeds[i:i + 2] for i in range(0, len(seeds), 2)]
     
seed_to_soil, soil_to_fertiliser, fertiliser_to_water, water_to_light, light_to_temp, temp_to_humidity, humidity_to_location = [[[int(n) for n in s.split(' ')] for s in d.split('\n')] for d in data]

def map_input(input, mapping):
    for m in mapping:
        destination, source, span = m
        if input in range(source, source + span):
            return destination - source + input
    return input

def map_input_range(input_ranges, mapping):
    output = []
    unmapped = []
    while input_ranges:
        start, spread = input_ranges.pop()
        unmapped_flag = True
        for m in mapping:
            destination, source, span = m
            # test for no overlap:
            if start + spread < source or start > source + span:
                pass
            elif start >= source and start + spread <= source + span:
                output.append([destination - source + start, spread])
                unmapped_flag = False
            # test for underhang
            elif start < source and start + spread <= source + span:
                output.append([destination, start + spread - source])
                # add underhang to list of ranges to be checked
                input_ranges.append([start, source - start - 1])
                unmapped_flag = False
            # test for overhang
            elif start >= source and start + spread > source + span:
                output.append([start + destination - source, source + span - start])
                # add overhang to list of ranges to be checked
                input_ranges.append([source + span + 1, start + spread - source - span - 1])
                unmapped_flag = False
            # test for doublehang
            elif start < source and start + spread > source + span:
                output.append([destination, span])
                # add underhang and overhang to list of ranges to be checked
                input_ranges.extend([[start, source - start - 1], [source + span + 1, start + spread - source - span - 1]])
                unmapped_flag = False
        # add to unmapped_flag
        if unmapped_flag:
            unmapped.append([start, spread])
    output.extend(unmapped)
    return output
    
def get_location(seed):
    soil = map_input(seed, seed_to_soil)
    fertiliser = map_input(soil, soil_to_fertiliser)
    water = map_input(fertiliser, fertiliser_to_water)
    light = map_input(water, water_to_light)
    temp = map_input(light, light_to_temp)
    humidity = map_input(temp, temp_to_humidity)
    location = map_input(humidity, humidity_to_location)
    return location

def get_location_range(seed):
    soil = map_input_range(seed, seed_to_soil)
    fertiliser = map_input_range(soil, soil_to_fertiliser)
    water = map_input_range(fertiliser, fertiliser_to_water)
    light = map_input_range(water, water_to_light)
    temp = map_input_range(light, light_to_temp)
    humidity = map_input_range(temp, temp_to_humidity)
    location = map_input_range(humidity, humidity_to_location)
    return location

print(min([get_location(seed) for seed in seeds]))
print(min([location[0] for location in get_location_range(seed_ranges)]))