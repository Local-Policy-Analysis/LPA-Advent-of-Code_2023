use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashMap;
use std::cmp;

const DIR4: [(i32, i32); 4] = [(0, -1),(1,0),(0,1),(-1,0)];

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Only the one argument please! Just the filename!");
    } 
    let inputloc = &args[1];

    let input = get_inputs(inputloc).unwrap();
    let map_mirror = make_mirror(&input.0, &input.1);
    let cheats = find_jumps(&map_mirror);
    let mut p1 = 0;
    for key in cheats.keys() {
        if *key >= 100 {
            p1 += cheats[key];
        }
    }
    println!("Part 1: {p1}");
    println!("Part 2: {}", p2(&map_mirror, 100))
}

fn get_inputs<P>(filename: P) -> io::Result<(Vec<Vec<char>>, usize, usize)>
// return map, instructions, startpos
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut map  = Vec::new();
    let mut startpos = 0;
    let mut endpos = 0;
    for (i, line) in reader.lines().enumerate() {
        let line = line?;
        let curr_line: Vec<char> = line.chars().collect();
        for j in 0..curr_line.len() {
            if curr_line[j] == 'S'{
                startpos = i * line.len() + j;
            } else if curr_line[j] == 'E' {
                endpos = i * line.len() + j;
            }
        }
        map.push(curr_line)
        }
    Ok((map, startpos, endpos))
}

fn make_mirror(map: &Vec<Vec<char>>, start: &usize) -> Vec<Vec<i32>> {
    let map_width = map[0].len();
    let map_height = map.len();
    let mut map_mirror = vec![vec![-1; map_width];map_height];

    // There's only one path from beginning to end, so 
    // no complicated pathfinding

    let mut pos = (start % map_width, start / map_width);
    let mut count = 0;
    map_mirror[pos.1][pos.0] = count;
    while map[pos.1][pos.0]!= 'E' {
        count += 1;
        for dir in &DIR4 {
            let newpos = ((pos.0 as i32 + dir.0) as usize,
                           (pos.1 as i32 + dir.1) as usize);
            if map[newpos.1][newpos.0] != '#' &&
                map_mirror[newpos.1][newpos.0] < 0{
                // move to it
                pos = (newpos.0, newpos.1);
                map_mirror[pos.1][pos.0] = count;
                break
            }
        }
    }
    map_mirror
}

fn find_jumps(map_mirror: &Vec<Vec<i32>>) -> HashMap<i32, i32>{
    let map_width = map_mirror[0].len();
    let map_height = map_mirror.len();
    let mut cheats = Vec::new();

    for y in 0..map_height{
        for x in 0..map_width{
            if map_mirror[y][x] == -1 {
                let mut vals = Vec::new();
                for dir in DIR4{
                    let newpos = ((x as i32 + dir.0) as usize,
                    (y as i32 + dir.1) as usize);
                    if newpos.0 > 0 && newpos.0 < map_width && newpos.1 > 0 && newpos.1 < map_height {
                        let v = map_mirror[newpos.1][newpos.0];
                        if v != -1 {vals.push(v)}
                    }
                }
                if vals.len() > 1 {
                    vals.sort();
                // laziness
                    cheats.push(vals[1]-vals[0] - 2);
                    if vals.len() > 2 {
                        cheats.push(vals[2] - vals[1] - 2);
                        cheats.push(vals[2] - vals[0] - 2);
                        if vals.len() > 3 {
                            panic!("I did not expect this");
                        }
                    } 
                } else {
                    continue;
                }
            }

        }
    }
    let mut freq = HashMap::new();
    for cheat in &cheats {
        if *cheat != 0 {
            freq.entry(*cheat)
                .and_modify(|e| {*e += 1})
                .or_insert(1_i32);
        }
    }
    freq
}

// There is surely a faster way to do this
fn p2(map: &Vec<Vec<i32>>, min_cheat: i32) -> i32 {
    let map_width = map[0].len();
    let map_height = map.len();
    let mut count = 0;

    for y in 0..map_height{
        for x in 0..map_width{
            let curr_val = map[y][x];
            if curr_val < 0 { 
                continue;
            }
            // Stupid off-by-one errors!
            let far_left = cmp::max(0, x as i32 - 21) as usize;
            let far_right = cmp::min(map_width, x + 21);
            let far_up = cmp::max(0, y as i32 - 21) as usize;
            let far_down = cmp::min(map_height, y + 21);
            // sorry
            for cy in far_up..far_down {
                for cx in far_left..far_right{
                    let m_distance = (cy as i32 - y as i32).abs() +
                                     (cx as i32 - x as i32).abs();
                    if m_distance <= 20 {
                        let test_val = map[cy][cx];
                        if test_val >= (curr_val + min_cheat + m_distance) {
                            count += 1;
                        }
                    }
                }
            }

        }
    }
    count

}