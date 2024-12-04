use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use regex::Regex;

fn main() {
    let args: Vec<String> = env::args().collect();
    let inputloc = &args[1];

    let input = get_input_str(inputloc).unwrap();
    let transforms = grid_transform(&input);
    let mut count = 0;
    let re = Regex::new("XMAS").unwrap();
    for grid in &transforms {
        for line in grid{
            count = count + re.find_iter(&line).count();
        }
    }
    println!("Part 1: {}", count);
    let mut count = 0;
    for i in 0..input.len()-2 {
        for j in 0..input[0].len()-2{
            if is_xmas(&get_xbox(&input, i, j)) {
                count = count + 1
            }
        }
    }
    println!("Part 2: {}", count)
}

fn get_input_str<P>(filename: P) -> io::Result<Vec<String>>
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

// The file is quite small, so get transformations of the grid in every
// direction the word could be in. This is very inefficient
fn grid_transform(grid: &Vec<String>) -> Vec<Vec<String>> {

    let mut out = Vec::new();

    out.push(grid.clone());

    // Right to left
    let r_grid = grid.into_iter()
                  .map(|line| line.chars().rev().collect::<String>())
                  .collect();
    out.push(r_grid);
    // Down
    let mut d_grid = Vec::new();
    for letter in grid[0].chars() {
        d_grid.push(letter.to_string());
    }
    let mut j = 0;
    for line in &grid[1..grid.len()] {
        for letter in line.chars(){
            d_grid[j].push_str(&letter.to_string());
            j = j + 1;
        }
        j = 0

    }
    // Up
    let u_grid = d_grid.clone().into_iter()
                      .map(|line| line.chars().rev().collect::<String>())
                      .collect();
    out.push(d_grid);
    out.push(u_grid);
    // diag L->R
    let mut diag_lr = Vec::new();
    for i in (0..2*grid.len()).rev() {
        let mut s = Vec::new();
        let mut j = 0 ;
        while i + j < 2*grid.len() {
            if ((i + j) >= grid.len()) & (j < grid[0].len())  {
                s.push(grid[(i + j) - grid.len()].chars().nth(j).unwrap());
            }
            j = j + 1;
        }
        diag_lr.push(s.into_iter().collect::<String>());
    }
    let diag_lr_r = diag_lr.clone().into_iter()
                      .map(|line| line.chars().rev().collect::<String>())
                      .collect();
    out.push(diag_lr);
    out.push(diag_lr_r);
    // diag R->L
    let mut diag_rl = Vec::new();
    for i in (0..2*grid.len()).rev() {
        let mut s = Vec::new();
        let l = grid[0].len() - 1;
        let mut j = 0;
        while j <= l {
            if ((i + j) >= grid.len()) & ((i + j) < 2*grid.len()){
                s.push(grid[(i + j) - grid.len()].chars().nth(l-j).unwrap())
            }
            j = j + 1;
        }
        diag_rl.push(s.into_iter().collect::<String>());
    }
    let diag_rl_r = diag_rl.clone().into_iter()
                      .map(|line| line.chars().rev().collect::<String>())
                      .collect();
    out.push(diag_rl);
    out.push(diag_rl_r);
    out
}

fn get_xbox(grid: &Vec<String>, x: usize, y: usize) -> Vec<String> {
    // Returns a 3x3 grid with top left corner at x, y
    if (x + 3 > grid.len()) | (y + 3 > grid[0].len()) {
        panic!("xbox does not fit in box");
    }
    let mut out = vec![String::new(); 3];
    for i in 0..3 {
        out[i] = grid[x + i][y..y+3].to_string();
    }

    out
}

fn is_xmas(xbox: &Vec<String>) -> bool {
    let word1: String = vec![xbox[0].chars().nth(0).unwrap(), xbox[1].chars().nth(1).unwrap(), xbox[2].chars().nth(2).unwrap()].into_iter().collect();
    let word2: String = vec![xbox[0].chars().nth(2).unwrap(), xbox[1].chars().nth(1).unwrap(), xbox[2].chars().nth(0).unwrap()].into_iter().collect();
    if !(word1.eq("MAS") || word1.eq("SAM")) || !(word2.eq("MAS") || word2.eq("SAM")) {
        return false
    }
    return true
}