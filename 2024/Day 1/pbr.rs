// Run `rustc pbr.rs` then `.\pbr input.txt` 

use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashMap;

fn main() {
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let nums = get_input_cols(inputloc).unwrap();
    let number_diffs = get_number_diffs(&nums);

    println!("Part 1: {}", number_diffs.iter().sum::<i32>());
    println!("Part 2: {}", get_similarity(&nums));
}

fn get_input_cols<P>(filename: P) -> io::Result<(Vec<i32>,Vec<i32>)>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut num1 = Vec::new();
    let mut num2 = Vec::new();

    for line in reader.lines() {
        let line = line?;

        let nums: Vec<i32> = line
            .split_whitespace()
            .map(|s| s.parse().unwrap_or(0))
            .collect();

        if nums.len() == 2{
            num1.push(nums[0]);
            num2.push(nums[1]);
        }
    }    
    num1.sort();
    num2.sort();

    Ok((num1, num2))
}

fn get_number_diffs(cols: &(Vec<i32>, Vec<i32>)) -> Vec<i32> {
    let mut out = Vec::new();

    let mut i = 0;
    while i < cols.0.len(){
        out.push((cols.0[i] - cols.1[i]).abs());
        i = i + 1;
    }

    out
}

fn get_similarity(cols: &(Vec<i32>, Vec<i32>)) -> i32{

let mut memos = HashMap::new();
let mut out = 0;

for &i in &cols.1 {
    memos.entry(i)
        .and_modify(|count| *count += 1)
        .or_insert(1);
}

for int in &cols.0{
    if memos.contains_key(&int){
        out = out + memos[int] * int
    }
}

out

}