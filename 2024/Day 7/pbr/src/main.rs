use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::char;

fn main() {
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let nums = get_input_rows(inputloc).unwrap();
    let mut p1 = 0;
    for num in &nums {
        if find_ops(&num.0, &num.1) {
            p1 += num.0;
        }
    }
    println!("Part 1: {}", p1);
    println!("Part 2: {}", p2(nums));
    
}

fn get_input_rows<P>(filename: P) -> io::Result<Vec<(i64, Vec<i64>)>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut out = Vec::new();

    for line in reader.lines() {
        let line = line?;

        let mut split = line.split(": ");
        // Only works because every line only has two parts
        let res: i64 = split.next().unwrap().parse().unwrap_or(0);
        let vals: Vec<i64> = split.next().unwrap().split_whitespace().map(|s| s.parse().unwrap_or(0)).collect();

        out.push((res, vals))
    }  

    Ok(out)
}

fn find_ops(target: &i64, ops: &Vec<i64>) -> bool {
    let l = ops.len();
    for i in 0..2_i32.pow((l - 1) as u32){
        let mut out = ops[0];
        let bin_str = format!("{:0width$b}", i, width = l-1 as usize);
        for (j, opt) in bin_str.chars().enumerate() {
            if opt == '0'{
                out = out + ops[j+1];
            } else {
                out = out * ops[j+1];
            }

            if out > *target{
                break;
            }
        }
        if out == *target {
            return true
        }
    }

    false
}

// It's as if this is just a trap for usual programming tricks!
// Make all valid trinary strings
fn tri_strings(length: u32) -> Vec<String>{
    let max = 3_u32.pow(length);
    let mut out = Vec::new();
    for i in 0..max {
        let mut j = i;
        let mut my_str = Vec::new();
        for _ in 0..length {
            my_str.push(char::from_digit(j % 3, 10).unwrap());
            j /= 3;
        }
        my_str.reverse();

        while my_str.len() < length as usize {
            my_str.insert(0, '0');
        }

        out.push(my_str.into_iter().collect());
    }
    out
}



fn do_ops(data: (Vec<i64>, String), target: &i64) -> i64 {
    let mut out = data.0[0];
    if data.1.len() == 0{
        return data.0[0]
    }
    for (i, op) in data.1.chars().into_iter().enumerate(){
        if op == '0'{
            out = out + data.0[i+1];
        } else if op == '1'  {
            out = out * data.0[i+1];
        } else {
            out = (out.to_string() + &data.0[i+1].to_string()).parse::<i64>().unwrap();
        }

        if out > *target{
            return 0
        }
    }
    return out
}

fn p2(input: Vec<(i64, Vec<i64>)>) -> i64{
    let mut out = 0;
    for row in input{
        for instr in tri_strings((row.1.len()-1) as u32){
            let res = do_ops((row.1.clone(), instr.clone()), &row.0);
            if res != -1 && res == row.0{
                out += row.0;
                break
            }
        }
    }
    out
}


//             let res = split_vec_on_concats(&row.1, &instr).into_iter().fold(
//    String::new(), |mut acc, x| {
//        acc.push_str(&do_ops(x, &row.0).to_string());
//        acc}

// Some code from when I read the question wrong
//fn split_vec_on_concats(vals: &Vec<i64>, ops: &str) -> Vec<(Vec<i64>, String)>{
//    let mut out = Vec::new();
//    let mut last_concat = 0;
//    for (i, op) in ops.chars().into_iter().enumerate(){
//        if op == '2' {
//            out.push((vals[last_concat..i+1].into_iter().cloned().collect::<Vec<i64>>(), ops[last_concat..i].to_string()));
//            last_concat = i + 1;
//        }
//    }
//    out.push((vals[last_concat..vals.len()].into_iter().cloned().collect::<Vec<i64>>(), ops[last_concat..ops.len()].to_string()));
//    out
//}