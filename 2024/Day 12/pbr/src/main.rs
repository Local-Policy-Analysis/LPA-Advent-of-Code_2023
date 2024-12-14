use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let input = get_input_str(inputloc).unwrap();
    let (map, nextcrop) = get_plot_status(&input);
    println!("Part 1: {}", p1(&map, nextcrop));
    println!("Part 2: {}", p2(&map, nextcrop));
}

fn get_input_str<P>(filename: P) -> io::Result<Vec<String>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut out = Vec::new();

    for line in reader.lines() {
        let line = line?;
        out.push(line);
    }  

    Ok(out)
}

fn get_plot_status(map: &Vec<String>) -> (Vec<Vec<(i32, i32, i32)>>, i32) {
    let directions: [[i32;2];8] = [[-1,0], [-1, 1], [0,1], [1,1], [1, 0], [1,-1], [0,-1], [-1, -1]];

    let max_y = map.len();
    let max_x = map[0].len();
    let mut nextcrop = 0;
    // region, fences, corners for each location
    let mut regionmap = vec![vec![(-1, 0, 0); max_x]; max_y];
    for (y, row) in map.into_iter().enumerate() {
        for (x, crop) in row.chars().into_iter().enumerate() {
            // if unmarked
            if regionmap[y as usize][x as usize].0 == -1{
                // fill space and mark everything as the same group
                let mut tocheck = vec![(y,x)];
                while tocheck.len() > 0 {
                    let mut fences = [false; 4];
                    let mut numfences = 0;
                    let mut corners = 0;
                    let nextval = tocheck.pop().unwrap();
                    // If we haven't been here yet
                    if regionmap[nextval.0 as usize][nextval.1 as usize].0 == -1 {
                        // check all of the adjacent directions
                        for (i, dir) in directions.iter().enumerate() {
                            let cx: i32 = nextval.1 as i32 + dir[1];
                            let cy: i32 = nextval.0 as i32 + dir[0];
                            if i % 2 == 0 { // Cardinals
                                if cx >= 0 && cy >= 0 && cx < max_x as i32 && cy < max_y as i32 {
                                    if map[cy as usize].chars().nth(cx as usize).unwrap() != crop {
                                        fences[i /2] = true;
                                        
                                    } else {
                                        tocheck.push((cy as usize, cx as usize));
                                    } 
                                } else {

                                    fences[i / 2] = true;
                                }
                            } else if cx >= 0 && cy >= 0 && cx < max_x as i32 && cy < max_y as i32 { //intercardinals to check for concave corners
                                if map[cy as usize].chars().nth(cx as usize).unwrap() != crop {
                                    let oneside = directions[(i - 1) % 8];
                                    let otherside = directions[(i + 1) % 8];
                                    if map[(nextval.0 as i32 + otherside[0]) as usize].chars().nth((nextval.1 as i32 + otherside[1]) as usize).unwrap() == crop &&
                                       map[(nextval.0 as i32 + oneside[0]) as usize].chars().nth((nextval.1 as i32 + oneside[1]) as usize).unwrap() == crop {
                                        corners += 1;
                                       }
                                }
                            }
                        }
                        for (i, is_fence) in fences.iter().enumerate() {
                            if *is_fence {
                                numfences += 1;
                                if fences[(i + 1) % 4] {
                                    corners += 1
                                }
                            }
                        }
                        regionmap[nextval.0 as usize][nextval.1 as usize] = (nextcrop, numfences, corners);
                        }
                    }
                    nextcrop += 1;
                }
            }
        
    }
    (regionmap, nextcrop)
}


fn p1(regionmap: &Vec<Vec<(i32, i32, i32)>>, nextcrop: i32) -> i32 {
    // could do something clever, but we're instead just going to loop through
    // once for each region because there aren't that many
    let mut out = 0;
    for region in 0..nextcrop {
        let mut area = 0;
        let mut fences = 0;
        for row in regionmap.clone().into_iter() { //slow
            for crop in row {
                if crop.0 == region {
                    area += 1;
                    fences += crop.1;
                }
            }
        }
        out += area * fences;
        // println!("{region} {area} {fences} {} {}", area * fences, t);
    }
    out
}

fn p2(regionmap: &Vec<Vec<(i32, i32, i32)>>, nextcrop: i32) -> i32 {
    let mut out = 0;
    for region in 0..nextcrop {
        let mut area = 0;
        let mut sides = 0;
        for row in regionmap.clone().into_iter() {
            for crop in row{
                if crop.0 == region {
                    area += 1;
                    sides += crop.2
                }
            }
        }
        out += area * sides;
   //     println!("{region} {area} {sides} {}", area * sides);
    }
    out
}