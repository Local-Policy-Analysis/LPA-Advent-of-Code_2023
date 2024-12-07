use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashMap;
use std::cmp::Ordering;

fn main() {
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let input = get_input_rows(inputloc).unwrap();
    println!("{}", part_1(&input));
    println!("{}", part_2(&input));

}

fn get_input_rows<P>(filename: P) -> io::Result<(Vec<Vec<i32>>, Vec<Vec<i32>>)>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut pairs = Vec::new();
    let mut pages = Vec::new();
    let mut mode = true;

    for line in reader.lines() {
        let line = line?;

        if line == "" {
            mode = false;
            continue
        }

        if mode {
            let nums: Vec<i32> = line
                .split('|')
                .map(|s| s.parse().unwrap_or(0))
                .collect();

                pairs.push(nums.clone())
        } else {
            let nums: Vec<i32> = line
                .split(',')
                .map(|s| s.parse().unwrap_or(0))
                .collect();

                pages.push(nums.clone());
        }

    }  

    Ok((pairs, pages))
}

fn get_successors(pairs: &Vec<Vec<i32>>) -> HashMap<i32, Vec<i32>>{
    let mut successors = HashMap::new();

    for pair in pairs{
        successors.entry(pair[0])
            .and_modify(|followers: &mut Vec<i32>| followers.push(pair[1]))
            .or_insert(vec![pair[1]]);
    }

    successors   
}
// Sorry
fn get_predecessors(pairs: &Vec<Vec<i32>>) -> HashMap<i32, Vec<i32>>{
    let mut predecessors = HashMap::new();

    for pair in pairs{
        predecessors.entry(pair[1])
            .and_modify(|followers: &mut Vec<i32>| followers.push(pair[0]))
            .or_insert(vec![pair[0]]);
    }

    predecessors
}


// Assume that the set doesn't give a complete ordering, and so it would
// be to much of a pain to make one
fn part_1(input: &(Vec<Vec<i32>>, Vec<Vec<i32>>)) -> i32{
    let successors = get_successors(&input.0);
    let mut answer = 0;
    for manual in &input.1 {
        let mut success = true;
        for i in 1..manual.len(){
            for j in i..manual.len(){
                if successors.contains_key(&manual[j]) {
                    if successors[&manual[j]].contains(&manual[i-1]) {
                        success = false;
                    } 
                }
            }
        }
        if success {
            let middle = (manual.len())/2;
            answer = answer + manual[middle]
        }
    }
    answer
}

fn comparenums(a: &i32, b: &i32, predecessors: &HashMap<i32, Vec<i32>>, successors: &HashMap<i32, Vec<i32>>) -> std::cmp::Ordering{
    // If b is a successor of a
    let in_succ = successors.contains_key(a);
    let in_pred = predecessors.contains_key(b);
    if in_succ && successors[a].contains(b){
        return Ordering::Greater
    } else if in_pred && predecessors[b].contains(a){
    // if a is a predecessor of b
        return Ordering::Greater
    } else {
        return Ordering::Less
    }
}

fn part_2(input: &(Vec<Vec<i32>>, Vec<Vec<i32>>)) -> i32{
    // There is a faster way to do this but it's taken ages and I'm tired!
    let successors = get_successors(&input.0);
    let predecessors = get_predecessors(&input.0);
    let mut answer = 0;
        for manual in &input.1 {
            let mut success = true;
            for i in 1..manual.len(){
                for j in i..manual.len(){
                    if successors.contains_key(&manual[j]) {
                        if successors[&manual[j]].contains(&manual[i-1]) {
                            success = false;
                        } 
                    }
                }
            }
            if !success {
                let mut m: Vec<i32> = manual.iter().copied().collect();
                m.sort_by(|a, b| comparenums(&a, &b, &successors, &predecessors));
                let middle = (m.len())/2;
                answer = answer + m[middle];
            }
        }
    answer
}