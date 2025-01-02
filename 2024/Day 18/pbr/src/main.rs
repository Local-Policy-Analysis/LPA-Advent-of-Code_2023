use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::cmp::Ordering;
use std::collections::BinaryHeap;

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 5 {
        println!("Insufficient arguments. Expected `inputfile` `xmax` `ymax` `p1limit1")
    } else {
    // Too lazy to count the inputs
    // test is 6 x 6
    // input is 70 x 70
    let xmax = &args[2].parse::<usize>().unwrap() + 0;
    let ymax = &args[3].parse::<usize>().unwrap() + 0;
    let p1limit = &args[4].parse::<usize>().unwrap() + 0;
    let inputloc = &args[1];

    let blocks = get_inputs(inputloc).unwrap();
    let p1_graph = make_easy_node_map(&blocks[..p1limit], xmax, ymax);
    let p1_path = shortest_path(&p1_graph, 0, xmax*ymax - 1).unwrap();
    println!("{}", p1_path);
    if let Some(p2_index) = p2(&blocks, xmax, ymax) {
        println!("{:?}", blocks[p2_index]);
    }

    }
}

fn get_inputs<P>(filename: P) -> io::Result<Vec<(usize, usize)>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut out = Vec::new();

    for line in reader.lines() {
        let line = line?;
        let chars = line.split(",").collect::<Vec<&str>>();
        out.push((chars[0].parse::<usize>().unwrap(),chars[1].parse::<usize>().unwrap()));
    }
    return Ok(out)
}

fn make_easy_node_map(blocks: &[(usize, usize)], xmax: usize, ymax: usize) -> Vec<Vec<Edge>> {
    let dirs = vec![(-1,0), (0,1), (1,0), (0,-1)];
    let offset = xmax * ymax;
    // Make a single layers worth of nodes
    let mut layer = vec![Vec::<Edge>::new(); offset];
    for y in 0..ymax {
        for x in 0..xmax {
            let pos = y * ymax + x;
            for dir in &dirs{
                let next_x = x as i32 + dir.1;
                let next_y = y as i32 + dir.0;
                if next_x >=0 && next_x < xmax as i32 && next_y >=0 && next_y < ymax as i32 {
                    layer[pos].push(Edge{node: next_y as usize * ymax + next_x as usize, cost: 1}) //add offset?
                }
            }
        }
    }
    for block in blocks{
        // for each block in the blocks, remove all edges that go to it
        let pos = block.0 + block.1 * ymax;
        for dir in &dirs{
            let next_x = block.0 as i32 + dir.1;
            let next_y = block.1 as i32 + dir.0;
            if next_x >=0 && next_x < xmax as i32 && next_y >=0 && next_y < ymax as i32 {
                let mut edges_temp = Vec::new();
                let newpos = (next_y * ymax as i32 + next_x) as usize;
                for edge in layer[newpos].clone() {
                    if edge.node != pos { // add offset?
                        edges_temp.push(edge.clone());
                    }
                    layer[newpos] = edges_temp.clone();
                }
            }
            layer[pos] = Vec::new();
        }
    }
    layer
}


fn p2(blocks: &[(usize, usize)], xmax: usize, ymax: usize) -> Option<usize> {
    let dirs = vec![(-1,0), (0,1), (1,0), (0,-1)];
    let offset = xmax * ymax;
    // Make a single layers worth of nodes
    let mut layer = vec![Vec::<Edge>::new(); offset];
    for y in 0..ymax {
        for x in 0..xmax {
            let pos = y * ymax + x;
            for dir in &dirs{
                let next_x = x as i32 + dir.1;
                let next_y = y as i32 + dir.0;
                if next_x >=0 && next_x < xmax as i32 && next_y >=0 && next_y < ymax as i32 {
                    layer[pos].push(Edge{node: next_y as usize * ymax + next_x as usize, cost: 1}) //add offset?
                }
            }
        }
    }
    for (i, block) in blocks.into_iter().enumerate(){
        // for each block in the blocks, remove all edges that go to it
        let pos = block.0 + block.1 * ymax;
        for dir in &dirs{
            let next_x = block.0 as i32 + dir.1;
            let next_y = block.1 as i32 + dir.0;
            if next_x >=0 && next_x < xmax as i32 && next_y >=0 && next_y < ymax as i32 {
                let mut edges_temp = Vec::new();
                let newpos = (next_y * ymax as i32 + next_x) as usize;
                for edge in layer[newpos].clone() {
                    if edge.node != pos { // add offset?
                        edges_temp.push(edge.clone());
                    }
                    layer[newpos] = edges_temp.clone();
                }
            }
            layer[pos] = Vec::new();
        }
        if let Some(_l) = shortest_path(&layer, 0, xmax*ymax - 1) {
            continue
        } else {
            return Some(i)
        }
    }
    None
}

fn shortest_path(adj_list: &Vec<Vec<Edge>>, start: usize, goal: usize) -> Option<usize> {
    let mut dist: Vec<_> = (0..adj_list.len()).map(|_| usize::MAX).collect();

    let mut heap = BinaryHeap::new();

    dist[start] = 0;
    heap.push(State { cost: 0, position: start});

    while let Some(State { cost, position }) = heap.pop() {
        if position == goal {
            return Some(cost);}
        if cost > dist[position] { continue; }
        for edge in &adj_list[position] {
            let next = State { cost: cost + edge.cost, position: edge.node};
            if next.cost < dist[next.position] {
                heap.push(next);
                dist[next.position] = next.cost;

            }
        }
    }
    None
}

#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    position: usize,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost)
            .then_with(|| self.position.cmp(&other.position))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

#[derive(Clone, Debug)]
struct Edge {
    node: usize,
    cost: usize,
}