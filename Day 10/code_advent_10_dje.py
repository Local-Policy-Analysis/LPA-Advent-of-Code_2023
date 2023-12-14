import numpy as np
from icecream import ic
import math

#test code
# pattern = [
#     ['.', '.', 'F', '7', '.'],
#     ['.', 'F', 'J', '|', '.'],
#     ['S', 'J', '.', 'L', '7'],
#     ['|', 'F', '-', '-', 'J'],
#     ['L', 'J', '.', '.', '.']
# ]
# test_array = np.array(pattern, dtype='str')

#actual problem
file_path = 'pattern_actual_dje.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()
test_array = np.vstack([list(line.strip()) for line in lines])


#find the starting location of S in the array and return 

S_location = np.concatenate(np.where(test_array=='S'))
S_location = [item.tolist() for item in S_location]
current_location = S_location.copy()

depth, width = test_array.shape

step_count = 0
max_steps = 0
s_moves_list = []

#set up the first 4 moves that are possible
if test_array[S_location[0] - 1][S_location[1]] == '|' or test_array[S_location[0] - 1][S_location[1]] == 'F' or test_array[S_location[0] - 1][S_location[1]] == '7':
    s_moves_list.append([-1,0])
if test_array[S_location[0] + 1][S_location[1]] == '|' or test_array[S_location[0] + 1][S_location[1]] == 'L' or test_array[S_location[0] + 1][S_location[1]] == 'J':
    s_moves_list.append([1,0])
if test_array[S_location[0]][S_location[1] - 1] == '-' or test_array[S_location[0]][S_location[1] - 1]== 'F' or test_array[S_location[0]][S_location[1] - 1] == 'L':
    s_moves_list.append([0,-1])  
if test_array[S_location[0]][S_location[1] + 1] == '-' or test_array[S_location[0]][S_location[1] + 1] == '7' or test_array[S_location[0]][S_location[1] + 1] == 'J':
    s_moves_list.append([0,1])
   
start_move = s_moves_list.pop()
last_move_row = start_move[0]
last_move_col = start_move[1]

while s_moves_list:
    step_count += 1
    current_location[0] = current_location[0] + last_move_row
    current_location[1] = current_location[1] + last_move_col

    if current_location[0] < 0 or current_location[0] > width or current_location[1] < 0 or current_location[1] > depth or current_location == S_location:
        step_count = 0
        current_location = S_location
        start_move = s_moves_list.pop()
        last_move_row = start_move[0]
        last_move_col = start_move[1]

        step_count += 1
        current_location[0] = current_location[0] + last_move_row
        current_location[1] = current_location[1] + last_move_col

    #return the value for the new current location
    current_loc_value = test_array[current_location[0]][current_location[1]]
    #python needs a dplyr case_when function!!
    if current_loc_value == 'J': 
        if last_move_col == 1: #entering from left
            last_move_col = 0
            last_move_row = -1
        else: #entering from the top
            last_move_col = -1
            last_move_row = 0
    elif current_loc_value == 'F':
        if last_move_row == -1: #entering from the bottom
            last_move_row = 0
            last_move_col = 1
        else: #entering from the right
            last_move_row = 1
            last_move_col = 0
    elif current_loc_value == 'L':
        if last_move_row == 1: #entering from the top
            last_move_row = 0
            last_move_col = 1
        else: #entering from the right
            last_move_row = -1
            last_move_col = 0
    elif current_loc_value == '7':
        if last_move_row == -1: #entering from the bottom
            last_move_row = 0
            last_move_col = -1
        else: #entering from the left
            last_move_row = 1
            last_move_col = 0
    elif current_loc_value == '|':
        if last_move_row == -1: #entering from the bottom
            last_move_row = -1
            last_move_col = 0
        else: #entering from the top
            last_move_row = 1
            last_move_col = 0
    elif current_loc_value == '-':
        if last_move_col == 1: #entering from the left
            last_move_row = 0
            last_move_col = 1
        else: #entering from the right
            last_move_row = 0
            last_move_col = -1

    ic(step_count)
    if step_count > max_steps:
        max_steps = step_count

ic(max_steps)
furthest_step =math.ceil(max_steps/2)
ic(furthest_step)