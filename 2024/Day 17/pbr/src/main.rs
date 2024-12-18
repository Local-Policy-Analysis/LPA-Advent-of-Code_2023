use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashSet;
use itertools::Itertools;

#[derive (Debug, Clone, Copy)]
struct Register {
    a: usize,
    b: usize,
    c: usize
}

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Only the one argument please! Just the filename!");
    } 
    let inputloc = &args[1];

    let (mut register, inst) = get_inputs(inputloc).unwrap();
    println!("Part 1: {}", p1(&register, &inst));
    println!("Part 2: {}", p2(&inst));
}


fn get_inputs<P>(filename: P) -> io::Result<(Register, Vec<usize>)>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut a = 0;
    let mut b = 0;
    let mut c = 0;
    let mut inst_str: String= String::from("");


    for (i, j) in reader.lines().enumerate() {
        let line = j?;
        match i {
            0 => a = line.split(": ").nth(1).unwrap().parse::<usize>().unwrap(),
            1 => b = line.split(": ").nth(1).unwrap().parse::<usize>().unwrap(),
            2 => c = line.split(": ").nth(1).unwrap().parse::<usize>().unwrap(),
            3 => continue,
            4 => inst_str = line.split(": ").nth(1).unwrap().to_string(),
            _ => continue,
        }
    }

    let inst: Vec<usize> = inst_str.split(',').map(|x| x.parse::<usize>().unwrap()).collect();
    // Probably don't need this, but don't trust the compiler
    let register = Register {a, b, c};
    Ok((register, inst))
}

fn p1(r: &Register, inst: &Vec<usize>) -> String {
    let mut reg = r.clone();
    let mut p = 0;
    let mut outvec = Vec::new();
    // There is some way to do this by passing functions...
    while p < inst.len() - 1{
        let r = match inst[p] {
            0 => adv(&mut reg, inst[p+1], &mut p),
            1 => bxl(&mut reg, inst[p+1], &mut p),
            2 => bst(&mut reg, inst[p+1], &mut p),
            3 => jnz(&mut reg, inst[p+1], &mut p),
            4 => bxc(&mut reg, inst[p+1], &mut p),
            5 => out(&mut reg, inst[p+1], &mut p),
            6 => bdv(&mut reg, inst[p+1], &mut p),
            7 => cdv(&mut reg, inst[p+1], &mut p),
            _ => panic!("disaster!")
        };
        if let Some(t) = r{
            outvec.push(t);
        }
    }
    outvec.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",")
}

fn p2(inst: &Vec<usize>) -> usize {
    /*
    By checking through the function definition, actually the progam is a small
    loop. It does:
    10 SET B to A % 8
    20 SET B to B XOR 6
    30 SET C to A // 2**B
    40 SET B TO B XOR C
    50 SET B TO B XOR 4
    60 OUTPUT B % 8
    70 SET A TO A // 8
    80 IF A > 0 GOTO 10

    This very inefficiently runs the loop in reverse to try and find 3-bit numbers
    that make up a vaid input for A
     */
    let mut out = Vec::new();
    for i in 0..inst.len(){
        let j = inst.len() - i - 1;
        if j == inst.len() - 1 {
            let mut curr = HashSet::new();
            curr.insert(inst[j] ^ 2);
            out.push(curr);
        } else if j == inst.len() - 2 {
            let l = out.len();
            let mut curr = HashSet::new();
            // Binary maths is hard. Just try them all
            for y in &out[l-1] { 
                for b in 0..9 {
                    let b1 = b ^ 6;
                    let b2 = b1 ^ (y*8 + b as usize)/2_usize.pow(b1 as u32);
                    let b3 = b2 ^ 4;
                    let b4 = b3 % 8;
                    if b4 == inst[j] {
                        curr.insert(b);
                    }
                }
            }
            out.push(curr)
        } else { //This is just terrible and I'm very sorry
            let l = out.len();
            let mut curr = HashSet::new();
            // Binary maths is hard. Just try them all
            for y in &out[l-1] { 
                for z in &out[l-2] {
                    for b in 0..9 {
                        let b1 = b ^ 6;
                        let b2 = b1 ^ (z*64 + y*8 + b as usize)/2_usize.pow(b1 as u32);
                        let b3 = b2 ^ 4;
                        let b4 = b3 % 8;
                        if b4 == inst[j] {
                            curr.insert(b);
                        }
                    }
                }
            }  
            out.push(curr);     
        }
    }
    // That's still a lot of options, but we can still iterate through them all,
    // It's only very slow
    out.reverse();
    let combinations = out.into_iter().map(|x| x.into_iter().collect::<Vec<usize>>()).multi_cartesian_product();
    let i_str = inst.clone().iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",");
    let mut outs = Vec::new();
    for combination in combinations {
        let mut n = 0;
        for (i, j) in combination.into_iter().enumerate(){
            n += 8_usize.pow(i as u32)*j;
        }
        let reg = Register{a:n,b:0,c:0};
        let figs = p1(&reg, &inst);
        if figs == i_str{
            outs.push(n)
        }
    }
    
    let m = outs.iter().min().unwrap();
    *m
}

// Here be many function definitions

fn combo_operand(r: &Register, literal: usize) -> usize {
    match literal {
        0 => 0,
        1 => 1,
        2 => 2,
        3 => 3,
        4 => r.a,
        5 => r.b,
        6 => r.c,
        _ => panic!("Invalid combo"), 
    }
}

// Should use methods 
fn adv(r: &mut Register, l: usize, p: &mut usize) -> Option<usize> {
    let num = r.a;
    let den = 2_usize.pow(combo_operand(&r, l) as u32);
    //println!("{p}: Dividing A {} by {den} -> {}", r.a, num/den);
    r.a = num/den;
    *p += 2;
    None
}

fn bxl(r: &mut Register, l: usize, p: &mut usize) -> Option<usize> {
    //println!("{p}: doing B {} XOR {} -> {}", r.b, l, r.b^l);
    r.b = r.b ^ l;
    *p += 2;
    None
}

fn bst(r: &mut Register, l: usize, p: &mut usize) -> Option<usize> {
    r.b = combo_operand(&r, l) % 8;
    //println!("{p}: Setting B to {}",r.b);
    *p += 2;
    None
}

fn jnz(r: &mut Register, l: usize, p: &mut usize) -> Option<usize> {
    if r.a != 0 {
        //println!("{p}: Jumping to {l}");
        *p = l;
    } else {
        //println!("{p}: Doing nothing");
        *p += 2;
    }
    None
}

fn bxc(r: &mut Register, _l: usize, p: &mut usize) -> Option<usize> {
    //println!("{p}: Setting B to B {} XOR C {} -> {}", r.b, r.c, r.b^r.c);
    r.b = r.b ^ r.c;
    *p += 2;
    None
}

fn out(r: &mut Register, l: usize, p: &mut usize) -> Option<usize> {
   // println!("{p}: Returning {l} -> {} -> {}",combo_operand(&r, l),combo_operand(&r, l) % 8);
    *p += 2;
    Some(combo_operand(&r, l) % 8)
}

fn bdv(r: &mut Register, l: usize, p: &mut usize) -> Option<usize> {
    let num = r.a;
    let den = 2_usize.pow(combo_operand(&r, l) as u32);
    //println!("{p}: Dividing A {} by {den} -> B {}", r.a, num/den);
    r.b = num/den;
    *p += 2;
    None
}

fn cdv(r: &mut Register, l: usize, p: &mut usize) -> Option<usize> {
    let num = r.a;
    let den = 2_usize.pow(combo_operand(&r, l) as u32);
    //println!("{p}: Dividing A {} by {den} -> C {}", r.a, num/den);
    r.c = num/den;
    *p += 2;
    None
}