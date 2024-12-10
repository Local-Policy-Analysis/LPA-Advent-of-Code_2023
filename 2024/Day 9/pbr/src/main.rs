use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashMap;

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let input = get_input_rows(inputloc).unwrap();
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

fn get_input_rows<P>(filename: P) -> io::Result<String>
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

    Ok(line)
}

fn get_mem_length(inst: &String) -> usize {
    inst.chars()
        .enumerate()
        .filter(|(i, _)| i % 2 == 0)
        .filter_map(|(_, x)| x.to_digit(10))
        .sum::<u32>() as usize
}

fn p1(inst: &String) -> i64 {
    let inst_chars: Vec<char> = inst.chars().collect();
    let mut memory: Vec<usize> = vec![0; get_mem_length(&inst)];
    // Instruction pointers
    let mut i: usize = 0;
    let mut i_count: u32 = 0;
    let mut j: usize = inst.len() - 1;
    let mut j_count: u32 = 0;
    // Memory pointer
    let mut m: usize = 0;

    while m < memory.len() {
        if i % 2 == 0 {
            if inst_chars.get(i).unwrap().to_digit(10).unwrap() != 0 {
                memory[m] = i/2;
                i_count += 1;    
            }   
            if i_count == inst_chars.get(i).unwrap().to_digit(10).unwrap(){
                i += 1;
                i_count = 0;
            }
            m += 1;
        } else {
            if inst_chars.get(j).unwrap().to_digit(10).unwrap() != 0 {

                if inst_chars.get(i).unwrap().to_digit(10).unwrap() != 0 {
                    memory[m] = j/2;
                    j_count += 1;
                    m += 1;
                    i_count += 1;
                }
            }
            if j_count == inst_chars.get(j).unwrap().to_digit(10).unwrap(){
                j -= 2;
                j_count = 0;
            }

            if i_count == inst_chars.get(i).unwrap().to_digit(10).unwrap(){
                i += 1;
                i_count = 0;
            }
        }
    }
    let mut out: i64 = 0;
    for (i,j) in memory.into_iter().enumerate() {
        out += (i * j) as i64;
    }

    out
}

fn p2 (inst: &String) -> i64 {
    // Turn memory into doubly linked list (but much slower)
    // Each item in list is [prev, ID number, length, next]
    let inst_chars: Vec<char> = inst.chars().collect();
    let mut memory: HashMap<i32, Vec<i32>> = HashMap::new();
    let mut next_index = inst_chars.len() as i32;

    for (i, j) in inst_chars.clone().into_iter().enumerate() {
        let val: i32 = if i % 2 == 0 {
            (i /2) as i32
        } else {
            -1
        };
        let next_block: i32 = if i as i32 == next_index - 1{
            -1
        } else {
            (i + 1) as i32
        };
        memory.insert(i as i32, vec![((i as i32) - 1), val, j.to_digit(10).unwrap() as i32, next_block]);
    }
    // block to try and move
    let mut try_move = (next_index - 1)/2;
    'outer: while try_move > 0 {
        // Find out how big the block is from the string
        let size = inst_chars[(try_move * 2) as usize].to_digit(10).unwrap();
        // Seek from left to try and find a space of that size
        let mut l = 0;
        while l != -1 {
            // If ther are no spaces before it
            if memory[&l][1] == try_move{
                try_move -= 1;
                continue 'outer;
            }
            if memory[&l][1] != -1 || memory[&l][2] <  (size as i32){
                l = memory[&l][3];
            } else {
                break
            }
        }
        if l == -1 {
            // No spaces
            try_move -= 1;
            continue
        }
        // otherwise move block into space

        next_index = move_into_space(&mut memory, &(try_move * 2), &l, &next_index);
        try_move -= 1;
    }

    // Run through memory and calculate checksum in a very inefficient way
    let mut loc = 0;
    let mut out: i64 = 0;
    let mut hdloc = 0;
    while loc != -1 {
        let s = &memory[&loc][1];
        let c = if *s == -1 {
            0
        } else {
            *s
        };
        for _j in 0..memory[&loc][2] {
            out += (c * hdloc) as i64;
            hdloc += 1;
        }
        loc = memory[&loc][3];
    }


    out
}

fn move_into_space(memory: &mut HashMap<i32, Vec<i32>>, block_id: &i32, space_id: &i32, next_index: &i32) -> i32 {
    let block = memory[&block_id].clone();
    let space = memory[&space_id].clone();
    let mut id = *next_index;
    if block[2] > space[2]{
        panic!("block does not fit in space");
    }
    if space[1] != -1 {
        panic!("attempted to move block into block")
    }
    if block[2] == space[2]{
        // The block takes up all of the space
        memory.insert(*space_id, vec![space[0], block[1], block[2], space[3]]);

    } else {
        memory.insert(*space_id, vec![space[0], block[1], block[2], id]);
        memory.insert(id, vec![*space_id, -1, space[2] - block[2], space[3]]); 
        id += 1;
    }
    memory.insert(*block_id, vec![block[0], -1, block[2], block[3]]); // Could combine spaces but lazy

    id
}

// Memory printing function

fn print_memory_plain(memory: &HashMap<i32, Vec<i32>>) {
    let mut i = 0;
    let mut loc = 0;
    let mut out = String::new();
    while i < memory.keys().len() {
        let s = &memory[&loc][1];
        let c = if *s == -1 {
            "."
        } else {
            &memory[&loc][1].to_string()
        };
        for _j in 0..memory[&loc][2] {
            
            out.push_str(&c)
        }
        loc = memory[&loc][3];
        i += 1;
    }
    println!("{}", out);
}
