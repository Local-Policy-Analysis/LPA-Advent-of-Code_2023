use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashSet;

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Only the one argument please! Just the filename!");
    } 
    let inputloc = &args[1];

    let input = get_inputs(inputloc).unwrap();
    println!("Part 1: {}", p1(&input.0, &input.1, &input.2));
    println!("Part 2: {}", p2(&input.0, &input.1, &input.2));
}

fn get_inputs<P>(filename: P) -> io::Result<(Vec<Vec<char>>, Vec<(i32, i32)>, (usize, usize))>
// return map, instructions, startpos
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut map  = Vec::new();
    let mut dirs = Vec::new();
    let mut dir_time = false;
    let mut startpos: (usize, usize) = (0,0);
    for (i, line) in reader.lines().enumerate() {
            let line = line?;
            if line == "" {
                dir_time = true;
                continue
            }
            if !dir_time {
                let curr_line: Vec<char> = line.chars().collect();
                for j in 0..curr_line.len() {
                    if curr_line[j] == '@'{
                        startpos = (i, j);
                    }
                }
                map.push(curr_line)
            } else {
                for inst in line.chars().into_iter() {
                    let next_inst = match inst {
                        '^' => (-1, 0),
                        '>' => (0, 1),
                        'v' => (1, 0),
                        '<' => (0, -1),
                        _ => (0, 0)
                    };
                    dirs.push(next_inst);
                }
            }
    }
    Ok((map, dirs, startpos))
 }

 fn make_big_map(map: &Vec<Vec<char>>) -> Vec<Vec<char>> {
    let mut big_map = Vec::new();
    for line in map {
        let mut new_line = Vec::new();
        for char in line {
            let mut to_push = match char {
                '#' => vec!['#', '#'],
                '.' => vec!['.', '.'],
                '@' => vec!['@', '.'],
                'O' => vec!['[', ']'],
                _ => vec![]
            };
            new_line.append(&mut to_push)
        }
        big_map.push(new_line);
    }
    big_map
 }

 fn do_input(map: &mut Vec<Vec<char>>,
             instr: (i32, i32),
             robot_loc: (usize, usize)) -> (usize, usize) {

            // Look at the location next to the robot
            let next_y = (robot_loc.0 as i32 + instr.0) as usize;
            let next_x = (robot_loc.1 as i32 + instr.1) as usize;
            let next_loc = map[next_y][next_x];
            if next_loc == '#' {
                return robot_loc
            } else if next_loc == '.' {
                // Strictly not needed, but useful for tracking down errors
                map[robot_loc.0][robot_loc.1] = '.';
                map[next_y][next_x] = '@';
                return (next_y as usize, next_x as usize)
            } else if next_loc =='O' {
                // Find the last stone in the row/column
                let mut last_stone = (next_y, next_x);
                loop {
                    let col_check = ((last_stone.0 as i32 + instr.0) as usize, (last_stone.1 as i32 + instr.1) as usize);
                    let next_check = map[col_check.0][col_check.1];
                    if next_check == '#' { // If there's a wall
                        return robot_loc
                    } else if next_check == 'O' {
                        last_stone = (col_check.0, col_check.1);
                        continue
                    } else if next_check == '.' { //We found the end!
                        // Set this space to be a stone
                        map[col_check.0][col_check.1] = 'O';
                        // move the robot to next_loc
                        map[next_y][next_x] = '@';
                        map[robot_loc.0][robot_loc.1] = '.';
                        return (next_y as usize, next_x as usize)
                    } else {
                        panic!("A DIFFERENT BAD THING HAS HAPPENED!")
                    }
                }
            } else {
                panic!("A BAD THING HAPPENED! {:?} {:?}", instr, robot_loc)
            }
 }

 fn find_big_stones(map: &Vec<Vec<char>>, pos: &(usize, usize), dir: &(i32, i32)) -> Result<HashSet<(usize, usize)>, i32>{
    // Find all stones affected by the move
    // Return the pos of the left brace in each stone
    let mut out = HashSet::new();
    let left_brace: (usize, usize);
    if map[pos.0][pos.1] == '[' {
        left_brace = *pos;
    } else if map[pos.0][pos.1] == ']' {
        left_brace = (pos.0, pos.1 - 1);
    } else {
        panic!("Tried to move block where there was none {:?}", pos);
    }
    out.insert(left_brace);
    let range = match *dir {
        (1, 0) => 0..2,
        (-1, 0) => 0..2,
        (0, 1) => 1..2,
        (0, -1) => 0..1,
        _ => 0..0
    };
    for i in range {
        let checkloc = ((left_brace.0 as i32 + dir.0) as usize, (left_brace.1 as i32 + i + dir.1) as usize);
        let to_check = map[checkloc.0][checkloc.1];
        if to_check == '[' || to_check == ']' {
            let future_stones = find_big_stones(map, &checkloc, dir);
            let _ = match future_stones {
                Ok(more_stones) => out.extend(more_stones),
                Err(e) => return Err(e)
            };
        } else if to_check == '#' {
            return Err(-1)
        } else {
            continue
        }
    }
    Ok(out)
 }

 fn p1(map: &Vec<Vec<char>>, instr: &Vec<(i32, i32)>, startpos: &(usize, usize)) -> usize {
    let mut local_map = map.clone();
    let mut pos = startpos.clone();
    for inst in instr {
        pos = do_input(&mut local_map, *inst, pos); 
    }
    // print_map(&local_map);
    score_map(&local_map)
 }

 fn p2(map: &Vec<Vec<char>>, instr: &Vec<(i32, i32)>, startpos: &(usize, usize)) -> usize {
    let mut local_map = make_big_map(map);
    let mut pos = (startpos.0, startpos.1 * 2);
    for inst in instr {
        // Look at the location next to the robot
        let next_y = (pos.0 as i32 + inst.0) as usize;
        let next_x = (pos.1 as i32 + inst.1) as usize;
        let next_loc = local_map[next_y][next_x];
        if next_loc == '#' {
            continue
        } else if next_loc == '.' {
                // Strictly not needed, but useful for tracking down errors
            local_map[pos.0][pos.1] = '.';
            local_map[next_y][next_x] = '@';
            pos = (next_y as usize, next_x as usize);
        } else if next_loc == '[' || next_loc == ']' {
            let to_move = match find_big_stones(&local_map, &(next_y, next_x), &inst) {
                Ok(blocks) => blocks,
                Err(_e) => continue
            };
            for block in &to_move{
                // Remove the old block
                local_map[block.0][block.1] = '.';
                local_map[block.0][block.1 + 1] = '.';
            } for block in &to_move{
                // Add in the new block. This definitely overwrites once, but that beats error checking.
                local_map[(block.0 as i32 + inst.0) as usize][(block.1 as i32 + inst.1) as usize] = '[';
                local_map[(block.0 as i32 + inst.0) as usize][(block.1 as i32 + inst.1 + 1) as usize] = ']';
            }
            local_map[pos.0][pos.1] = '.';
            local_map[next_y][next_x] = '@';
            pos = (next_y as usize, next_x as usize);
        }  
    }
    //print_map(&local_map);
    score_map(&local_map)
 }

fn score_map(map: &Vec<Vec<char>>) -> usize {
    let mut score = 0;
    for (i, row) in map.into_iter().enumerate() {
        for (j, c) in row.into_iter().enumerate() {
            if *c == 'O' || *c == '[' {
                score += 100 * i + j;
            }
        }
    }
    score
}

 fn print_map(map: &Vec<Vec<char>>) {
    for line in map {
        let p: String = line.into_iter().collect();
        println!("{p}");
    }
 }
