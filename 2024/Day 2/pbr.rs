// Run `rustc pbr.rs` then `.\pbr input.txt` 

use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let nums = get_input_rows(inputloc).unwrap();

    let mut s = 0;
    let mut d = 0;
    for num in nums{
        if is_safe(&num) {
            s = s + 1;
        }
        if is_damped_safe(&num){
            d = d + 1
        }
    }
    println!("Part 1: {}", s);
    println!("Part 2: {}", d);
    
}

fn get_input_rows<P>(filename: P) -> io::Result<Vec<Vec<i32>>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut out = Vec::new();

    for line in reader.lines() {
        let line = line?;

        let nums: Vec<i32> = line
            .split_whitespace()
            .map(|s| s.parse().unwrap_or(0))
            .collect();

        out.push(nums.clone())
    }  

    Ok(out)
}

fn is_safe(report: &Vec<i32>) -> bool {
    let mut i = 0;
    let mut diff;
    let mut sign = false;
    // Assume they're all at least length 2
    while i < report.len() - 1 {
        diff = report[i] - report[i + 1];
        if (diff.abs() > 3) | (diff.abs() < 1) {
            return false ;
        }
        if i == 0 {
            sign = diff < 0;
        }
        if (diff < 0) != sign {
            return false;
        }
        i = i + 1
    }

    true
}

// There is probably a more efficient way to do this
// Where you compare the difference and the difference to the next but one
// But this will work and it's late
fn is_damped_safe(report: &Vec<i32>) -> bool {
    if is_safe(&report){
        return true
    }
    let mut i = 0;
    while i < report.len(){
        let mut removed = Vec::new();
        let mut j = 0;
        while j < report.len(){
            if j != i {
                removed.push(report[j])
            }
            j = j + 1;
        }
        if is_safe(&removed){
            return true
        }
        i = i + 1;
    }
    return false
}