use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashSet;
use gcd::Gcd;

fn main(){
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        println!("Insufficient arguments. Expected `inputfile` `xmax` `ymax`")
    } else {
    let inputloc = &args[1];
    // Too lazy to count the inputs
    // test is 10 x 10
    // input is 50 x 60
    let xmax = &args[2].parse::<usize>().unwrap() - 1;
    let ymax = &args[3].parse::<usize>().unwrap() - 1;

    let input = get_antenna(inputloc).unwrap();
    println!("Part 1: {}", p1(&input, &xmax, &ymax));
    println!("Part 2: {}", p2(&input, &xmax, &ymax));
    }
}

fn get_antenna<P>(filename: P) -> io::Result<Vec<(char, usize, usize)>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut out = Vec::new();

    for (y, line) in reader.lines().enumerate() {
        let line = line?;
        for (x, c) in line.chars().into_iter().enumerate() {
            if c != '.' {
                out.push((c, x, y));
            }
        }
    }
    Ok(out)
}

fn get_antinodes(node1: &(char, usize, usize), node2: &(char, usize, usize), max_x: &usize, max_y: &usize) -> Option<Vec<(usize, usize)>> {
    let n1 = (node1.1 as i32, node1.2 as i32);
    let n2 = (node2.1 as i32, node2.2 as i32);
    let x_max = *max_x as i32;
    let y_max = *max_y as i32;
    let mut out = Vec::new();
    // If there are antinodes between the two antennae
    // Apparently we don't count those...
    //if ((n1.0 - n2.1 as i32) % 3 == 0) && ((n1.1 as i32 - n2.1 as i32) % 3 == 0) {
    //    out.push(((n1.0 + (n2.0 - n1.0)/3) as usize, (n1.1 + (n2.1 - n1.1)/3) as usize));
    //    out.push(((n2.0 + (n1.0 - n2.0)/3) as usize, (n2.1 + (n1.1 - n2.1)/3) as usize));
    //}
    // If outer antinodes are in the map add them
    let guess1 = (2*n2.0 - n1.0, 2*n2.1 - n1.1);
    let guess2 = (2*n1.0 - n2.0, 2*n1.1 - n2.1);
    if guess1.0 >= 0 && guess1.0 <= x_max && guess1.1 >= 0 && guess1.1 <= y_max{
        out.push((guess1.0 as usize, guess1.1 as usize));
    }
    if guess2.0 >= 0 && guess2.0 <= x_max && guess2.1 >= 0 && guess2.1 <= y_max{
        out.push((guess2.0 as usize, guess2.1 as usize));
    }
    Some(out)
}

fn p1(input: &Vec<(char, usize, usize)>, xmax: &usize, ymax: &usize) -> usize {
    let mut antinodes: HashSet<(usize, usize)> = HashSet::new();
    let mut antennae = input.clone();
    while antennae.len() > 0{
        let focus = antennae.pop().unwrap();
        for antenna in &antennae {
            if antenna.0 == focus.0 {
                antinodes.extend(get_antinodes(&antenna, &focus, xmax, ymax).unwrap())
            }
        }
    }
    antinodes.len()
}

fn get_antinodes_2(node1: &(char, usize, usize), node2: &(char, usize, usize), max_x: &usize, max_y: &usize) -> Option<Vec<(usize, usize)>> {
    let n1 = (node1.1 as i32, node1.2 as i32);
    let n2 = (node2.1 as i32, node2.2 as i32);
    let x_max = *max_x as i32;
    let y_max = *max_y as i32;
    let mut out = Vec::new();
    let mut vec_between = (n2.0 - n1.0, n2.1 - n1.1);
    let gcd = (vec_between.0.abs() as u32).gcd(vec_between.1.abs() as u32) as i32;
    vec_between.0 = vec_between.0/gcd;
    vec_between.1 = vec_between.1/gcd;

    for i in -x_max..x_max{
        let guess = (n1.0 + vec_between.0 * i, n1.1 + vec_between.1 * i);
        if guess.0 >= 0 && guess.0 <= x_max && guess.1 >= 0 && guess.1 <= y_max{
            out.push((guess.0 as usize, guess.1 as usize));
        }
    }
    Some(out)
}

fn p2(input: &Vec<(char, usize, usize)>, xmax: &usize, ymax: &usize) -> usize {
    let mut antinodes: HashSet<(usize, usize)> = HashSet::new();
    let mut antennae = input.clone();
    while antennae.len() > 0{
        let focus = antennae.pop().unwrap();
        for antenna in &antennae {
            if antenna.0 == focus.0 {
                antinodes.extend(get_antinodes_2(&antenna, &focus, xmax, ymax).unwrap())
            }
        }
    }
    antinodes.len()
}