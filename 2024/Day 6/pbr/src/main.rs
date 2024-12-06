use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashSet;

fn main() {
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let input = get_input_rows(inputloc).unwrap();
    let mut visited = HashSet::<(i32, i32)>::new();
    let mut visited_with_dir = HashSet::<(i32, i32, i32)>::new();
    let mut pos = input.1;
    visited.insert(pos);
    let mut dir = 0; // 0 = up, 1 = right, 2 = down, 3 = left, -1 = left map
    while dir >= 0{
        do_step(&input.0, &mut visited, &mut visited_with_dir, &mut pos, &mut dir);
    }
    println!("{}", visited.len());
    let mut part_2 = 0; 
    for path_loc in &visited{
        if *path_loc == input.1 {
            continue;
        }
        let mut map = input.0.clone();
        map[path_loc.1 as usize][path_loc.0 as usize] = '#';
        let mut pos_temp = input.1;
        let mut visited_temp = HashSet::<(i32, i32)>::new();
        let mut visited_with_dir = HashSet::<(i32, i32, i32)>::new();
        let mut dir_temp = 0;
        while dir_temp >= 0{
            do_step(&map, &mut visited_temp, &mut visited_with_dir, &mut pos_temp, &mut dir_temp);
        }
        if dir_temp == -2 {
            part_2 += 1;
        }
    }
    println!("{}", part_2)


}

fn get_input_rows<P>(filename: P) -> io::Result<(Vec<Vec<char>>, (i32, i32))>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut map = Vec::new();

    let mut x = 0;
    let mut y = 0;
    let mut j = 0;
    for line in reader.lines() {
        let line = line?;
        // There has to be a way to do this that doesn't involve reading each line
        // twice
        if line.contains("^") {
            y = j;
            x = line.chars().position(|el| el == '^').unwrap() as i32;
        }
        map.push(line.chars().collect());
        j += 1;
    }

    Ok((map, (x,y)))
}

fn do_step(map: &Vec<Vec<char>>,
           visited: &mut HashSet<(i32, i32)>,
           visited_with_dir: &mut HashSet<(i32, i32, i32)>,
           pos: &mut (i32, i32),
           dir: &mut i32) {

    let newpos = match dir {
        0 => (pos.0, pos.1 - 1),
        1 => (pos.0 + 1, pos.1),
        2 => (pos.0, pos.1 + 1),
        3 => (pos.0 - 1, pos.1),
        _ => (-1, -1)
    };
    if newpos.0 < 0 ||
        newpos.1 < 0 ||
        newpos.0 >= map.len().try_into().unwrap() ||
        newpos.1 >= map[1].len().try_into().unwrap() {

        *dir = -1;
    } else if map[newpos.1 as usize][newpos.0 as usize] == '#'{
        *dir = (*dir + 1) % 4;
    } else if visited_with_dir.contains(&(newpos.0, newpos.1, *dir)) {
        *dir = -2;
    } else {
        visited_with_dir.insert((newpos.0, newpos.1, *dir));
        visited.insert(newpos);
        *pos = newpos;
    }
}