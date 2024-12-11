use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashMap;

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("remember to include the file!");
    }
    let inputloc = &args[1];

    let input = get_input_rows(inputloc).unwrap();
    println!("Part 1: {}", p1(input.clone(), 25));


    let mut _hms = 0;
    let mut memo = HashMap::new();
    println!("Part 2: {}", p2(&input.clone(), 75, &mut memo));
}

fn p1(stones: Vec<f64>, blinks: i32) -> usize{
    // It seems unlikley this will work for p2
    if blinks == 0 {
        return stones.len()
    }
    else {
        stones.into_iter().map(|x| p1(blink(x), blinks -1 )).sum()
    }
}


fn p2(stones: &[f64], blinks: i32, memo: &mut HashMap<(Vec<i64>, i32), usize>) -> usize {
    let stones_fixed : Vec<i64> = stones.iter().map(|&x| x as i64).collect();

    if let Some(&result) = memo.get(&(stones_fixed.clone(), blinks)) {
        return result;
    }

    if blinks == 0 {
        let result = stones.len();
        memo.insert((stones_fixed, blinks), result);
        return result;
    }

    let mut out = 0;
    for &stone in stones {
        out += p2(&blink(stone), blinks - 1, memo);
    }

    memo.insert((stones_fixed, blinks), out);
    out
}



fn get_input_rows<P>(filename: P) -> io::Result<Vec<f64>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let line: String;
    // Should only be one line?
    let mut lines = reader.lines();
    if let Some(first_line) = lines.next() {
        line = first_line?;
    } else {
        line = "".to_string();
        println!("disaster!")
    }
    let s = line.split_whitespace().map(|x| x.parse::<f64>().unwrap()).collect();

    Ok(s)
}

fn blink(stone: f64) -> Vec<f64>{
    if stone == 0.0{
        return vec![1.0]
    }
    let rounded = stone.log10().trunc();
    if rounded % 2.0 == 1.0 {
        return vec![
            (stone / (10.0_f64.powf((rounded + 1.0)/2.0))).trunc(), //error-prone
            stone % (10.0_f64.powf((rounded + 1.0)/2.0))
        ]
    }
    vec![stone * 2024.0]
}