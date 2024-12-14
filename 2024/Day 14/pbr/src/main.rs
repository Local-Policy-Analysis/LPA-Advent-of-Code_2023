use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use regex::Regex;

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let input = get_inputs(inputloc).unwrap();
    println!("{}", p1(&input, 100, 101, 103));
    p2(&input, 10000, 101, 103);

}

fn get_inputs<P>(filename: P) -> io::Result<Vec<[i64; 4]>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut out = Vec::new();
    let mut buff = [0; 4];
    let re = Regex::new(r"p=(?<px>-?\d+),(?<py>-?\d+) v=(?<vx>-?\d+),(?<vy>-?\d+)").unwrap();
    for line in reader.lines() {
        let line = line?;
        let coords = re.captures(&line).unwrap();
        for i in 0..4 {
            buff[i] = coords[i+1].parse::<i64>().unwrap();
        }
        out.push(buff)
    }
    Ok(out)
}

fn move_robot(init: &[i64; 4], time: i64, max_x: i64, max_y: i64) -> (i64, i64){
    let newpos_x = (((init[0] + time*init[2]) % max_x) + max_x) % max_x;
    let newpos_y = (((init[1] + time*init[3]) % max_y) + max_y) % max_y;
    (newpos_x, newpos_y)
}

fn get_quadrant(pos: (i64, i64), max_x: i64, max_y: i64) -> i64 {
    let x_mid = (max_x + 1) / 2 -1;
    let y_mid = (max_y + 1) / 2 -1;
    let x = pos.0;
    let y = pos.1;
    if x < x_mid {
        if y < y_mid {
            return 0
        } else if y > y_mid {
            return 2
        }
    } else if x > x_mid{
        if y < y_mid {
            return 1
        } else if y > y_mid {
            return 3
        }
    }
    return -1
}

fn p1(input: &Vec<[i64; 4]>, time: i64, max_x: i64, max_y: i64) -> i64 {
    let mut quarters = [0; 4];

    for robot in input {
        let r = move_robot(&robot, time, max_x, max_y);
        let q = get_quadrant(r, max_x, max_y);
        if q >= 0 {
            quarters[q as usize] += 1;
        }
    }
    quarters.iter().fold(1, |acc, x| x * acc)
}

fn guess_tree(input: &Vec<[i64; 4]>, time: i64, max_x: i64, max_y: i64) {
    // Assume it's a mostly contiguous tree, so > 20 of robots
    // are next to another robot
    let mut display = vec![vec!['.'; max_x as usize]; max_y as usize];
    for robot in input {
        let r = move_robot(&robot, time, max_x, max_y);
        display[r.1 as usize][r.0 as usize] = '#'
    }
    let mut adj = 1;
    for row in &display {
        for i in 1..(row.len() - 1) {
            if row[i] != '.' {
                if row[i-1] != '.' && row[i + 1] != '.' {
                    adj += 1;
                }
            }
        }
    }
    if input.len() / adj < 5 {
        println!("---{}---", time);
        for line in display {
            println!("{}", line.into_iter().collect::<String>());
        }
    }
}

fn p2(input: &Vec<[i64; 4]>, max_time: i64, max_x: i64, max_y: i64) {
    for t in 0..max_time {
            guess_tree(input, t, max_x, max_y);
    }
}
