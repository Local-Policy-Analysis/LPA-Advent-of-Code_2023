extern crate regex;

use std::{
    fs::File,
    io::{prelude::*, BufReader},
    path::Path,
    borrow::Cow
};
use regex::{Regex};

fn lines_from_file(filename: impl AsRef<Path>) -> Vec<String> {
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
       .map(|l| l.expect("Could not parse line"))
       .collect()
}

fn main() {
    let lines = lines_from_file("../../inputs/day_1.txt");
    let re = Regex::new(r"\d").unwrap();
    let mut total = 0;
    for line in &lines[..]{
        let matches: Vec<_> = re.find_iter(&line).map(|m| m.as_str()).collect();
        let num = matches[0].parse::<i32>().unwrap()*10 + matches[matches.len()-1].parse::<i32>().unwrap();
        total += num;
    }
    println!("Part 1: {:?}", total);

    let repl = vec![vec!["one", "o1e"],
                    vec!["two", "t2o"],
                    vec!["three", "t3e"],
                    vec!["four", "f4r"],
                    vec!["five", "f5e"],
                    vec!["six", "s6x"],
                    vec!["seven", "s7n"],
                    vec!["eight", "e8t"],
                    vec!["nine", "n9e"]];
    // I am not happy about this, but I don't know how to do the clever regex reduce thing
    // I did in Python in Rust

    let mut total1 = 0;
    for line in &lines[..]{
        let mut tmp = Cow::from(line);
        for rep in &repl[..]{
            tmp = tmp.replace(rep[0], rep[1]).into();
        }
        let matches: Vec<_> = re.find_iter(&tmp).map(|m| m.as_str()).collect();
        let num = matches[0].parse::<i32>().unwrap()*10 + matches[matches.len()-1].parse::<i32>().unwrap();
        total1 +=  num;
    }
    println!("Part 2: {:?}", total1);
}