#[allow(unused_variables)]
use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashSet;
use std::collections::HashMap;

fn main () {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let input = get_input_str(inputloc).unwrap();
    let test = follow_trail(&(0,2), &input);
    let mut m = input.clone();
    for y in 0..8 {
        for x in 0..8 {
            if !(test.contains(&(x,y))) {
                m[y as usize][x as usize] = 0
            }
        }
    }
    println!("Part 1 {}", p1(&input));
    println!("Part 2 {}", p2(&input));
    trail_rating(&(0,2), &input);
}

fn p1(map: &Vec<Vec<i32>>) -> i32 {
    let mut out = 0;
    for y in 0..map.len() {
        for x in 0..map[0].len(){
            if map[y][x] == 0{
                let trail = follow_trail(&(y as i32,x as i32), map);
                for point in trail{
                    if map[point.0 as usize][point.1 as usize] == 9 {
                        out += 1;
                    }
                }
            }
        }
    }
    out
}

fn p2(map: &Vec<Vec<i32>>) -> i32 {
    let mut out = 0;
    for y in 0..map.len(){
        for x in 0..map[0].len(){
            if map[y][x] == 0{
                out += trail_rating(&(y as i32, x as i32), map);

            }
        }
    }
    out
}

fn get_input_str<P>(filename: P) -> io::Result<Vec<Vec<i32>>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut out = Vec::new();

    for line in reader.lines() {
        let line = line?;
        let mut line_nums = Vec::new();

        for c in line.chars().into_iter() {
            line_nums.push(c.to_digit(10).unwrap() as i32);
        }
        out.push(line_nums);
    }  

    Ok(out)
}

//fn printmap(map: &Vec<Vec<i32>>) {
//    for line in map{
//        println!("{}", line.into_iter().map(|x| x.to_string()).collect::<String>());
//    }
//}

fn follow_trail(point: &(i32, i32), map: &Vec<Vec<i32>>) -> Vec<(i32, i32)>{
    let mut previous_points = HashSet::new();
    let mut new_points = vec![*point];
    let mut valid_points = [(-1, -1); 4];
    while new_points.len() > 0 {
        let to_explore = new_points.clone();
        
        previous_points.extend(new_points);
        new_points = Vec::new();
        for ex_point in to_explore{
            valid_points = get_reachable(&ex_point, &map);
            for v_point in valid_points.iter() {
                if v_point.0 != -1 {
                    new_points.push(*v_point)
                }
            }
        }
    }
    previous_points.into_iter().collect::<Vec<(i32, i32)>>()

}

// Djikstra again I guess
fn trail_rating(point: &(i32, i32), map: &Vec<Vec<i32>>) -> i32 {
    let mut visited = HashMap::new();
    let mut points = HashSet::new();
    points.insert(*point);
    let mut valid_points = [(-1, -1); 4];
    for point in &points {
        visited.insert((point.0, point.1), 1);
    }

    while points.len() > 0 {
        let to_explore = points.clone();
        points = HashSet::new();
        for ex_point in to_explore {
            valid_points = get_reachable(&ex_point, map);
            for v_point in valid_points.iter() {
                let pt_value = visited[&ex_point];
                if v_point.0 != -1 {
                    visited.entry(*v_point)
                           .and_modify(|e| {*e += pt_value})
                           .or_insert(pt_value);
                    points.insert(*v_point);
                }
            }
        }

    }
    let mut out = 0;
    for key in visited.keys(){
        if map[key.0 as usize][key.1 as usize] == 9 {
            out += visited[key];
        }
    }
    out
}

fn get_reachable(point: &(i32, i32), map: &Vec<Vec<i32>>) -> [(i32, i32); 4] {
    let directions = [(0,1), (1,0), (0,-1), (-1, 0)];
    let mut out = [(-1, -1); 4];
    let point_value = map[point.0 as usize][point.1 as usize] + 1;
    for i in 0..4 {
        let new_y = point.0 + directions[i].0;
        let new_x = point.1 + directions[i].1;
        if new_x >= 0 && new_y >= 0 && new_y < map.len() as i32 && new_x < map[0].len() as i32 {
            if map[new_y as usize][new_x as usize] == point_value {
                out[i] = (new_y, new_x);
            }
        }
    }
    out

}