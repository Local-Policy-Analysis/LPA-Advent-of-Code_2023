// Run `cargo run input.txt`

use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use regex::Regex;

fn main() {
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let input = get_input_str(inputloc).unwrap();

    let p1 = get_mults(&input).into_iter().fold(0, |acc, (x1, x2)| acc + x1 * x2);

    println!("Part 1: {}", p1);

    let mut tot = 0;
    let mut state = true;
    for pair in get_instr_mults(&input).into_iter() {
        if pair.0 == -1 {
            state = true
        } else if pair.1 == -1 {
            state = false
        } else if state {
            tot = tot + (pair.0 * pair.1);
        } else {
            // nonop
        }
    }

    println!("Part 2: {}", tot)
    
}

fn get_input_str<P>(filename: P) -> io::Result<String>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut out: String = Default::default();

    for line in reader.lines() {
        let line = line?;

        out.push_str("\n");
        out.push_str(&line);
    }  

    Ok(out)
}

fn get_mults(instr: &String) -> Vec<(i32, i32)>{
    let re = Regex::new(r"mul\((?<n1>\d{1,3}),(?<n2>\d{1,3})\)").unwrap();

    let pairs: Vec<(i32, i32)> = re.captures_iter(&instr).map(|caps| {
        let n1 = caps.name("n1").unwrap().as_str().parse::<i32>().unwrap();
        let n2 = caps.name("n2").unwrap().as_str().parse::<i32>().unwrap();
        (n1,n2)
    }).collect();

    return pairs
}

fn get_instr_mults(instr: &String) -> Vec<(i32, i32)>{
    // Return pairs, but return (-1, 0) for do and (0, -1) for don't
    let re = Regex::new(r"(mul\((?<n1>\d{1,3}),(?<n2>\d{1,3})\))|(?<do>do\(\))|(?<dont>don't\(\))").unwrap();

    let pairs: Vec<(i32, i32)> = re.captures_iter(&instr).map(|caps| {
        if let Some(n1) = caps.name("n1") {
            let n1_parse = n1.as_str().parse::<i32>().unwrap();
            let n2_parse = caps.name("n2").unwrap().as_str().parse::<i32>().unwrap();
            (n1_parse, n2_parse)
        } else if let Some(_start) = caps.name("do"){
            (-1, 0)
        } else if let Some(_end) = caps.name("dont"){
            (0, -1)
        } else {
            (-2, -2)
        }
    }).collect();

    return pairs
}