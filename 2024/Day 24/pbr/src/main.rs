use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::{HashMap, VecDeque};
use regex::Regex;


fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Only the one argument please! Just the filename!");
    } 
    let inputloc = &args[1];
    let (tape, ops, initial) = get_input(inputloc).unwrap();
    println!("Part 1 {}", p1(&tape, &ops, &initial));
    p2(&tape, &ops);
}

#[derive (Debug, Clone)]
struct Operation {
    value: Option<u8>,
    op: String,
    output: String
}

#[derive (Debug, Clone)]
struct Tape_Space {
    value: Option<u8>,
    op_cell: Vec<Option<i32>>
}

fn get_input<P>(filename: P) -> io::Result<(HashMap<String, Tape_Space>, Vec<Operation>, VecDeque<String>)>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut tape: HashMap<String, Tape_Space> = HashMap::new();
    let mut ops = Vec::new();
    let mut initial = VecDeque::new();

    let mut op_mode = false;
    let re = Regex::new(r"(?<node1>[a-z0-9]{3})\s(?<op>[A-Z]{2,3})\s(?<node2>[a-z0-9]{3})\s->\s(?<node3>[a-z0-9]{3})").unwrap();
    let mut op_count = 0;
    for line in reader.lines() {
        let line = line?;
        if line == "" {
            op_mode = true;
            continue
        }
        if op_mode == false{
            let input = line.split(": ").collect::<Vec<&str>>();
            tape.insert(String::from(input[0]), Tape_Space{value: Some(input[1].parse::<u8>().unwrap()), op_cell: Vec::new()});
            initial.push_back(String::from(input[0]));
        } else {
            let nodes = re.captures(&line).unwrap();
            tape.entry(nodes[1].to_string()).and_modify(|x| {x.op_cell.push(Some(op_count))}).or_insert(Tape_Space{value: None, op_cell: vec![Some(op_count)]});
            tape.entry(nodes[3].to_string()).and_modify(|x| {x.op_cell.push(Some(op_count))}).or_insert(Tape_Space{value: None, op_cell: vec![Some(op_count)]});
            ops.push(Operation{
                value: None,
                op: nodes[2].to_string(),
                output: nodes[4].to_string()
            });
            tape.entry(nodes[4].to_string()).or_insert(Tape_Space{value: None, op_cell: Vec::new()});
            op_count += 1;
        };
    }
    Ok((tape, ops, initial))
}

fn p1(tape: &HashMap<String, Tape_Space>, ops: &Vec<Operation>, initial: &VecDeque<String>) -> usize {
    let mut tape = tape.clone();
    let mut ops = ops.clone();
    let mut has_value = initial.clone();
    let mut outs = Vec::new();

    while has_value.len() > 0 {
        // Get next free value
        let consider = has_value.pop_front().unwrap();
        //println!("{consider}");
        // get related operation
        for op in tape[&consider].op_cell.clone(){
            let op = op.unwrap() as usize;
            // Check if there's a number stored there
            if let Some(val) = ops[op].value{
                let out = match &ops[op].op[..] {
                    "AND" => tape[&consider].value.unwrap() & val,
                    "XOR" => tape[&consider].value.unwrap() ^ val,
                    "OR" => tape[&consider].value.unwrap() | val,
                    _ => panic!("Unknown operator!")
                };
                tape.get_mut(&ops[op].output).unwrap().value = Some(out);
                if ops[op].output.chars().nth(0).unwrap() == 'z' {
                    outs.push(ops[op].output.clone());
                } else {
                    has_value.push_back(ops[op].output.clone());
                }
            } else {
                ops[op].value = tape[&consider].value;
            }
        }
    }
    outs.sort();
    let mut answer = 0;
    for (i, out) in outs.into_iter().enumerate(){
        answer += 2_usize.pow(i as u32)*(tape[&out].value.unwrap() as usize);
        //println!("{out} {}", tape[&out].value.unwrap())
    }
    answer
}

// Surely there's some way that doesn't involve doing it by inspection...
fn p2(tape: &HashMap<String, Tape_Space>, ops: &Vec<Operation>){
    let mut x_keys = Vec::new();
    let mut y_keys = Vec::new();
    let mut x = 0;
    let mut y = 0;
    for key in tape.keys(){
        let first_char = key.chars().nth(0).unwrap();
        if first_char == 'x' {
            x_keys.push(key.clone())
        } else if first_char == 'y' {
            y_keys.push(key.clone())
        }
    }
        x_keys.sort();
        y_keys.sort();

        for (i, key) in x_keys.clone().into_iter().enumerate(){
            x += 2_usize.pow(i as u32)*(tape[&key].value.unwrap() as usize);
        }
        for (i, key) in y_keys.clone().into_iter().enumerate(){
            y += 2_usize.pow(i as u32)*(tape[&key].value.unwrap() as usize);
        }
   
    println!("x: {x}, y: {y} sum:{}", x + y);
    println!("Adder errors:");

    // We'll assume it's a normal binary adder
    // So every input should lead to an XOR gate

    let all_initial_keys = [x_keys.as_slice(), y_keys.as_slice()].concat();
    let initial_XORs: Vec<usize> = Vec::new();

    let mut carrier = String::from("");
    for x_key in x_keys {
        let val = &x_key[1..];
        let y_key = format!("y{val}");
        // Check all of the things they connect to. It should be an XOR gate
        // and an AND gate
        let mut xor = 0;
        let mut and = 0;
        let mut xor2 = 0;
        let mut and2 = 0;
        let mut or = 0;
        if tape[&x_key].op_cell.len() > 0 {

            for op in &tape[&x_key].op_cell{
                if let Some(chosen_op) = op {
                    let op_op = ops[*chosen_op as usize].op.clone();
                    match &op_op[..] {
                        "XOR" => xor = *chosen_op,
                        "AND" => and = *chosen_op,
                        _ => {println!("{x_key} connects to {op_op}")}
                    }
                }
            }
        } else {
            println!("initial value has no connections?")
        }
        // this should also be true for the y value, and they should be the
        // same xor and and
        if tape[&y_key].op_cell.len() > 0 {
            for op in &tape[&y_key].op_cell{
                if let Some(chosen_op) = op {
                    let op_op = ops[*chosen_op as usize].op.clone();
                    match &op_op[..]{
                        "XOR" => {if *chosen_op != xor {
                            println!("different XORs for same row {val} x:{xor} {chosen_op}")}},
                        "AND" => {if *chosen_op != and {
                            println!("different ANDs for same row {val} x:{and} {chosen_op}")
                        }},
                        _ => {println!("{y_key} connectes to {op_op}")}
                    }
                }
            }
        } else {
            println!("initial value has no connections?")
        }
        // If this is the first one, that should go to the output
        if val == "00" {
            if ops[xor as usize].output != "z00" {
                println!("Error at initial xor: {xor}");
            }
            // The output of the and is carried
            carrier = ops[and as usize].output.clone();
        } else {
            // For all of the others the XOR should lead to an XOR and an
            // AND
            let xor_out = ops[xor as usize].output.clone();
            for op in &tape[&xor_out].op_cell{
                if let Some(chosen_op) = op {
                    let op_op = ops[*chosen_op as usize].op.clone();
                    match &op_op[..]{
                        "XOR" => xor2 = *chosen_op,
                        "AND" => and2 = *chosen_op,
                        _ => println!{"cable {xor_out} (xor_out) {val} is incorrect {op_op}"}
                    }
                }
            }
            // Which the carrier should also lead to
            for op in &tape[&carrier].op_cell{
                if let Some(chosen_op) = op {
                    let op_op = ops[*chosen_op as usize].op.clone();
                    match &op_op[..]{
                        "XOR" => {if *chosen_op != xor2 {
                            println!("different XOR2s for carrier {val} {carrier} {xor_out} x:{xor} {chosen_op}")}},
                        "AND" => {if *chosen_op != and2 {
                            println!("different AND2s for same carrier {val} {carrier} {xor_out} x:{and} {chosen_op}")
                        }},
                        _ => println!("cable (carrier) {carrier} is incorrect")
                    }
                }
            }
            // Both ANDs should lead to an OR
            let and_out = ops[and as usize].output.clone();
            for op in &tape[&and_out].op_cell{
                if let Some(chosen_op) = op {
                    let op_op = ops[*chosen_op as usize].op.clone();
                    match &op_op[..]{
                        "OR" => or = *chosen_op,
                        _ => println!("cable {and_out} (and_out) {val} is incorrect {op_op}")
                    }
                }
            }
            let and2_out = ops[and2 as usize].output.clone();
            for op in &tape[&and2_out].op_cell{
                if let Some(chosen_op) = op {
                    let op_op = ops[*chosen_op as usize].op.clone();
                    match &op_op[..]{
                        "OR" => {if *chosen_op != or {
                            println!("cable and2_out {and2_out} doesn't match and_out {and_out} {}", *chosen_op)
                        }
                                if or == 0 {
                                    or = *chosen_op;
                                }},
                        _ => println!("cable {and2_out} (and2_out) {val} is incorrect {op_op}")
                    }
                }
            }
            if or != 0 {
                carrier = ops[or as usize].output.clone();
            } else {
                println!("failed to find carry for {val}");
            }
            // xor2 should lead to the correct out
            let xor2_out = ops[xor2 as usize].output.clone();
            if xor2_out != format!("z{val}") {
                println!("{val} -> {xor2_out}");
            }
        } // If not first
    }

}


// Then use logic basically