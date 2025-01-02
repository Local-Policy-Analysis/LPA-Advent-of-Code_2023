use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::{HashMap, HashSet, VecDeque};

const PRUNE: i64 = 2_i64.pow(24);

fn main () {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Only the one argument please! Just the filename!");
    } 
    let inputloc = &args[1];

    let input = get_input(inputloc).unwrap();
    println!("Part 1: {}", p1(&input));
    println!("Part 2: {}", p2(&input));
}

fn get_input<P>(filename: P) -> io::Result<Vec<i64>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut out = Vec::new();

    for line in reader.lines() {
        let line = line?;
        out.push(line.parse::<i64>().unwrap());
    }  

    Ok(out)
}

fn prng(input: i64) -> i64 {
    let mut out = input * 64;
    out = out ^ input;
    out = out % PRUNE;
    let out1 = out / 32;
    out = out ^ out1;
    out = out % PRUNE;
    let out2 = out * 2_i64.pow(11);
    out = out ^ out2;
    out = out % PRUNE;
    out
}

// This works, but I suspect not for part 2
fn p1(input: &Vec<i64>) -> i64 {
    let mut out = 0;
    for i in input{
        let mut v = *i;
        for _ in 0..2000{
            v = prng(v);
        }
         out += v
    }
    out
}

fn p2(input: &Vec<i64>) -> i64 {
    // I'm sure I should use rayon to parallel process this but I don't know how!
    // just store all of the possible sets of directions and the number of bananas you'd get if you
    // used those directons
    let mut values: HashMap<(i8, i8, i8, i8), i64> = HashMap::new();
    for i in input{
        let mut v = *i;
        let mut u: i64;
        let mut recent_diff = VecDeque::new();
        let mut diff_used = HashSet::new();
        for _ in 0..2000{
            u = prng(v);
            recent_diff.push_back((u % 10 - v % 10) as i8);
            v = u;
            if recent_diff.len() > 4{
                recent_diff.pop_front();
            }
            if recent_diff.len() == 4{
                let diffs = (recent_diff[0], recent_diff[1], recent_diff[2], recent_diff[3]);
                if diff_used.insert(diffs.clone()){
                    values.entry(diffs).and_modify(|x|{*x += u % 10}).or_insert(u % 10);
                }
            }
        }
    }

    // Then look through all of the keys in values to find the highest one
    let mut max = 0;
    let mut instr = (0, 0, 0, 0);
    for (key, value) in values{
        if value > max {
            instr = key;
            max = value;
        }
    }
    max
}