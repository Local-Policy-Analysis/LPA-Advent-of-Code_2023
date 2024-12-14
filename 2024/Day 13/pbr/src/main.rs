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
    println!("Part 1: {}", p1(&input));
    println!("Part 2: {}", p2(&input));
    
}

fn get_inputs<P>(filename: P) -> io::Result<Vec<[(i64, i64); 3]>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut out = Vec::new();
    let mut a = (0,0);
    let mut b = (0,0);
    let mut prize = (0,0);
    let re = Regex::new(r"X[+=](?<x>\d+)\,\sY[+=](?<y>\d+)").unwrap();
    for (i, line) in reader.lines().enumerate() {
        let line = line?;
        let linemod = i % 4;
        if line.len() > 0 {
            let coords = re.captures(&line).unwrap();
        // There's probably a function for this
            if linemod == 0 {
                a.0 = coords[1].parse::<i64>().unwrap();
                a.1 = coords[2].parse::<i64>().unwrap();
            } else if linemod == 1 {
                b.0 = coords[1].parse::<i64>().unwrap();
                b.1 = coords[2].parse::<i64>().unwrap();
            } else if linemod == 2 {
                prize.0 = coords[1].parse::<i64>().unwrap();
                prize.1 = coords[2].parse::<i64>().unwrap();
            } 
        } else {
         out.push([a,b,prize]);   
        }
    }
    // lazy!
    out.push([a,b,prize]);  
    Ok(out)
}


fn solve_equation(a: (i64, i64), b: (i64, i64), prize: (i64, i64)) -> Option<(i64, i64)> {
    // Take in movement vectors for a and b and position vector for prize
    // output number of a and b pushes to get prize

    let det = a.0 * b.1 - b.0 * a.1;
    let x_top = b.1 * prize.0 - b.0 * prize.1;
    let y_top = -a.1 * prize.0 + a.0 * prize.1;


    if x_top % det == 0 && y_top % det == 0 {
        return Some((x_top/det, y_top/det))
    } else {
        None
    }
}

fn p1(input: &Vec<[(i64, i64); 3]>) -> i64 {
    let mut out = 0;
    for machine in input{
        if let Some((x, y)) = solve_equation(machine[0], machine[1], machine[2]) {
            out += 3 * x + y
        } else {
            continue
        }
    }
    out
}

fn p2(input: &Vec<[(i64, i64); 3]>) -> i64 {
    const BIGERROR: i64 = 10000000000000;
    let mut out = 0;
    for machine in input{
        if let Some((x, y)) = solve_equation(machine[0],
                                             machine[1], 
                                             (BIGERROR + machine[2].0, BIGERROR + machine[2].1)) {
            out += 3 * x + y
        } else {
            continue
        }
    }
    out
}