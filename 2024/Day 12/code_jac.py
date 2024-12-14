import numpy as np
with open('input_jac.txt') as f:
    data = np.array([list(d.strip()) for d in f.readlines()])
    
visited = set()

def score_region(region):
    area = len(region)
    perimeter = 0
    for r in region:
        x, y = r
        if (x + 1, y) not in region:
            perimeter += 1
        if (x - 1, y) not in region:
            perimeter += 1
        if (x, y + 1) not in region:
            perimeter += 1
        if (x, y - 1) not in region:
            perimeter += 1
    return area * perimeter

def score_region_differently(region):
    area = len(region)
    sides = 0
    edges = set()
    for r in region:
        x, y = r
        if (x + 1, y) not in region and (x, y, "U") not in edges:
            edges.add((x, y, "U"))
            sides += 1
            is_edge = True
            i = 1
            while is_edge:
                if (x, y + i) in region and (x + 1, y + i) not in region:
                    edges.add((x, y + i, "U"))
                    i += 1
                else:
                    is_edge = False
            is_edge = True
            i = 1
            while is_edge:
                if (x, y - i) in region and (x + 1, y - i) not in region:
                    edges.add((x, y - i, "U"))
                    i += 1
                else:
                    is_edge = False
        if (x - 1, y) not in region and (x, y, "D") not in edges:
            edges.add((x, y, "D"))
            sides += 1
            is_edge = True
            i = 1
            while is_edge:
                if (x, y + i) in region and (x - 1, y + i) not in region:
                    edges.add((x, y + i, "D"))
                    i += 1
                else:
                    is_edge = False
            is_edge = True
            i = 1
            while is_edge:
                if (x, y - i) in region and (x - 1, y - i) not in region:
                    edges.add((x, y - i, "D"))
                    i += 1
                else:
                    is_edge = False
        if (x, y + 1) not in region and (x, y, "R") not in edges:
            edges.add((x, y, "R"))
            sides += 1
            is_edge = True
            i = 1
            while is_edge:
                if (x + i, y) in region and (x + i, y + 1) not in region:
                    edges.add((x + i, y, "R"))
                    i += 1
                else:
                    is_edge = False
            is_edge = True
            i = 1
            while is_edge:
                if (x - i, y) in region and (x - i, y + 1) not in region:
                    edges.add((x - i, y, "R"))
                    i += 1
                else:
                    is_edge = False
        if (x, y - 1) not in region and (x, y, "L") not in edges:
            edges.add((x, y, "L"))
            sides += 1
            is_edge = True
            i = 1
            while is_edge:
                if (x + i, y) in region and (x + i, y - 1) not in region:
                    edges.add((x + i, y, "L"))
                    i += 1
                else:
                    is_edge = False
            is_edge = True
            i = 1
            while is_edge:
                if (x - i, y) in region and (x - i, y - 1) not in region:
                    edges.add((x - i, y, "L"))
                    i += 1
                else:
                    is_edge = False
    return area * sides
    
visited = set()
def get_region(x, y, region, value, visited):
    if (x, y) not in visited:
        if (x, y) not in region and data[x, y] == value:
            visited.add((x,y))
            region.add((x, y))
            if x + 1 < data.shape[0]:
                get_region(x + 1, y, region, data[(x, y)], visited)
            if x - 1 >= 0:
                get_region(x - 1, y, region, data[(x, y)], visited)
            if y + 1 < data.shape[1]:
                get_region(x, y + 1, region, data[(x, y)], visited)
            if y - 1 >= 0:
                get_region(x, y - 1, region, data[(x, y)], visited)
        return region
    else:
        return None

pt1 = 0
pt2 = 0
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        region = get_region(i, j, set(), data[i, j], visited)
        if region:
            pt1 += score_region(region)
            pt2 += score_region_differently(region)
        
print(pt1)
print(pt2)
    
