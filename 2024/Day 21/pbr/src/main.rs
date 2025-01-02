use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashMap;



fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Only the one argument please! Just the filename!");
    } 
    let inputloc = &args[1];

    let input = get_inputs(inputloc).unwrap();
    
    println!("Part 1: {}", p1(&input));
    println!("Part 2: {}", enter_codes(&input, 25));
}



fn get_inputs<P>(filename: P) -> io::Result<Vec<String>>
// return map, instructions, startpos
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut out = Vec::new();

    for line in reader.lines() {
        let line = line?;
        out.push(line);
        }
    Ok(out)
}

fn get_between(from: char, to: char) -> String {
    if from == to {
        return String::from("A");
    }
    let mut out = String::new();
    let from_int_try = from.to_digit(10);
    let to_int_try = to.to_digit(10);
    let from_loc = match from_int_try{
        Some(0) => 1,
        Some(a) => a + 2,
        None => 2
    };
    let to_loc = match to_int_try{
        Some(0) => 1,
        Some(a) => a + 2,
        None => 2
    };
    let right = (to_loc % 3) as i32 - (from_loc % 3) as i32;
    let up = (to_loc / 3) as i32 - (from_loc / 3) as i32;
    // if it would go over the corner
    if (from_loc / 3 == 0 || to_loc / 3 == 0) && (from_loc % 3 == 0 || to_loc % 3 == 0) {
        if up > 0 {
            // lazy
            for _ in 0..up {
                out.push('^');
            }
        }
        if right > 0 {
            for _ in 0..right {
                out.push('>');
            }
        } else if right < 0 {
            for _ in right..0 {
                out.push('<');
            }
        }
        if up < 0 {
            for _ in up..0 {
                out.push('v');
            }
        }
    } else {
        if right < 0 {
            for _ in right..0 {
                out.push('<');
            }
        }
        if up > 0 {
            for _ in 0..up {
                out.push('^');
            }
        }
        if up < 0 {
            for _ in up..0 {
                out.push('v');
            }
        }
        if right > 0 {
            for _ in 0..right {
                out.push('>');
            }
        }
    }
    out.push('A');
    out
}

fn get_between_arrows(from: char, to: char) -> String {
    //Just reuse code
    if from == to {
        return String::from("A");
    }
    let mut out = String::new();
    let from_loc = match from {
        '^' => 4,
        'A' => 5,
        '<' => 0,
        'v' => 1,
        '>' => 2,
        _ => -1
    };
    let to_loc = match to {
        '^' => 4,
        'A' => 5,
        '<' => 0,
        'v' => 1,
        '>' => 2,
        _ => -1
    };
    // Logic from https://observablehq.com/@jwolondon/advent-of-code-2024-day-21
    // Because mine was wrong for some reason that I still don't understand!
    let right = (to_loc % 3) as i32 - (from_loc % 3) as i32;
    let up = (to_loc / 3) as i32 - (from_loc / 3) as i32;
    let mut verts = String::new();
    let mut hors = String::new();
    if up > 0 {
        verts = format!("{}", "^".repeat(up as usize));
    } else if up < 0 {
        verts = format!("{}", "v".repeat(up.abs() as usize));
    }
    if right > 0 {
        hors = format!("{}", ">".repeat(right as usize));
    } else if right < 0 {
        hors = format!("{}", "<".repeat(right.abs() as usize));
    }

    if right > 0 && (up < 1 || from_loc != 0) {
        out = verts + &hors;
    } else if up >= 0 || to_loc != 0 {
        out = hors + &verts;
    } else {
        out = verts + &hors;
    }
    out.push('A');
    out
}

fn p1(inputs: &Vec<String>) -> i64 {
    let mut out = 0;
    for input in inputs {
        let input_with_a = String::from("A") + input;
        let mut out1 = String::from("A");
        for i in 0..(input_with_a.len() - 1) {
            out1.push_str(&get_between(input_with_a.chars().nth(i).unwrap(), input_with_a.chars().nth(i+1).unwrap()));
        }
        let mut out2 = String::from("A");
        for i in 0..(out1.len() - 1) {
            out2.push_str(&get_between_arrows(out1.chars().nth(i).unwrap(), out1.chars().nth(i+1).unwrap()));
        }
        let mut out3 = String::from("");
        for i in 0..(out2.len() - 1){
            out3.push_str(&get_between_arrows(out2.chars().nth(i).unwrap(), out2.chars().nth(i+1).unwrap()));
        }
        out += out3.len() as i64 * input[..3].parse::<i64>().unwrap();
    }
    out
}

// method taken from someone on reddit because it was just all going wrong.
// Still took so long to work out as well!
fn enter_codes(input: &Vec<String>, robots: usize) -> i64 {
    let dirkeys = ['^', 'A', '<', 'v', '>'];
    let mut paths = HashMap::new();
    for from in dirkeys{
        for to in dirkeys{
            paths.insert((from, to), get_between_arrows(from, to));
        }
    }
    for (key, value) in paths.clone().into_iter(){
    }
    let mut complexity_sum = 0;
    for code in input{
        let  mut button_presses = HashMap::new();
        // First count button presses on the numeric keypad
        let mut curr_button = 'A';
        for button in code.chars().into_iter() {
            let directions = get_between(curr_button, button);
            curr_button = button;
            //directions += &String::from("A");
            button_presses.entry(directions).and_modify(|x| {*x += 1}).or_insert(1);
        }
        // Count all the button presses on the directional keypads
        for _ in 0..robots {
            // copy the dictionary
            let button_presses_layer = button_presses.clone();
            for (button_press, count) in button_presses_layer.into_iter() {
                curr_button = 'A';
                for button in button_press.chars().into_iter() {
                    let directions = paths.get(&(curr_button, button)).unwrap();
                    curr_button = button;
                    button_presses.entry(directions.to_string()).and_modify(|x| {*x += count}).or_insert(count);
                }
                button_presses.entry(button_press).and_modify(|x| {*x -= count});
            }
        }
        let mut complexity = 0;
        for (button_press, count) in button_presses.into_iter() {
            complexity += button_press.len() as i64 * count;
        }
        complexity_sum += complexity * code[..3].parse::<i64>().unwrap()
    }
    complexity_sum

}
