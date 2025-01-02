use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Only the one argument please! Just the filename!");
    } 
    let inputloc = &args[1];
    let (locks, keys) = get_input(inputloc).unwrap();
    println!("Part 1: {}", p1(&locks, &keys))
}

fn get_input<P>(filename: P) -> io::Result<(Vec<Vec<i32>>, Vec<Vec<i32>>)>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut keys = Vec::new();
    let mut locks = Vec::new();

    let mut mode = "none";

    let mut curr = vec![0;5];
    let mut count = 0;

    for (i,line) in reader.lines().enumerate() {
        let line = line?;
        if line == "" {
            if mode == "key"{
                keys.push(curr.clone());
            } else {
                locks.push(curr.clone());
            }
            mode = "none";
            curr = vec![0;5];
            continue
        }
        if mode == "none" {
            if line == "#####" { // it's a lock
            count = 0;
            mode = "lock"
            } else {
                mode = "key";
                count = 0;
            }
            continue
        } else if mode == "key" {
            count += 1;
            for (i, c) in line.chars().into_iter().enumerate() {
                if c == '.' {
                    curr[i] = count;
                }
            }
        } else if mode == "lock" {
            count += 1;
            for (i, c) in line.chars().into_iter().enumerate() {
                if c == '#' {
                    curr[i] = count;
                }
            }
        }

    }
    if mode == "key"{
        keys.push(curr.clone());
    } else {
        locks.push(curr.clone());
    }
    Ok((locks, keys))
}

fn p1(locks: &Vec<Vec<i32>>, keys: &Vec<Vec<i32>>) -> i32 {
    // Could use a tree for speed, but it's small enough for 
    // brute force
    //println!("{locks:?}, {keys:?}");
    let mut fits = 0;
    for lock in locks {
        'keys: for key in keys{
            for i in 0..5 {
                if key[i] < lock[i]{
                    //println!("{lock:?} {key:?} {i}");
                    continue 'keys
                }
            }
            fits += 1;
        }
    }
    fits
}