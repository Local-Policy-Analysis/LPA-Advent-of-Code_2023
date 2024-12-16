use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::cmp::Ordering;
use std::collections::BinaryHeap;
use std::collections::HashSet;

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Only the one argument please! Just the filename!");
    } 
    let inputloc = &args[1];

    let input = get_inputs(inputloc).unwrap();
    //print_map(&input.0);
    let graph = make_graph(&input.0);
    let paths = shortest_path(&graph, input.1*4+1, input.2*4).unwrap();
    println!("Part 1: {}", paths.0/10);
    println!("Part 2: {}", paths.1.into_iter().collect::<HashSet<usize>>().len());
    //print_map_with_path(&input.0, &paths.1)
}

fn get_inputs<P>(filename: P) -> io::Result<(Vec<Vec<char>>, usize, usize)>
// return map, instructions, startpos
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut map  = Vec::new();
    let mut startpos = 0;
    let mut endpos = 0;
    for (i, line) in reader.lines().enumerate() {
        let line = line?;
        let curr_line: Vec<char> = line.chars().collect();
        for j in 0..curr_line.len() {
            if curr_line[j] == 'S'{
                startpos = i * line.len() + j;
            } else if curr_line[j] == 'E' {
                endpos = i * line.len() + j;
            }
        }
        map.push(curr_line)
        }
    Ok((map, startpos, endpos))
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

fn shortest_path(adj_list: &Vec<Vec<Edge>>, start: usize, goal: usize) -> Option<(usize, Vec<usize>)> {
    let mut dist: Vec<_> = (0..adj_list.len()).map(|_| usize::MAX).collect();
    let mut predecessor: Vec<Option<Vec<usize>>> = (0..adj_list.len()).map(|_| None).collect();

    let mut heap = BinaryHeap::new();

    dist[start] = 0;
    heap.push(State { cost: 0, position: start});

    while let Some(State { cost, position }) = heap.pop() {
        if position == goal {
            let mut path = Vec::new();
            let mut current = vec![goal];
            while let Some(next_pick) = current.pop() {
                if let Some(predecessors) = &predecessor[next_pick] {
                    current.extend(predecessors.iter().cloned()); //slow?
                }
                path.push(next_pick/4);
            }
            path.reverse();
            return Some((cost, path));}
        if cost > dist[position] { continue; }
        for edge in &adj_list[position] {
            let next = State { cost: cost + edge.cost, position: edge.node};
            if next.cost < dist[next.position] {
                heap.push(next);
                dist[next.position] = next.cost;
                predecessor[next.position] = Some(vec![position]);
            } else if next.cost == dist[next.position] {
                if let Some(predecessors) = &mut predecessor[next.position]{
                    predecessors.push(position);
                }
            }
        }
    }
    None
}

fn print_map(map: &Vec<Vec<char>>) {
    for line in map {
        let p: String = line.into_iter().collect();
        println!("{p}");
    }
 }

 fn print_map_with_path(map: &Vec<Vec<char>>, path: &Vec<usize>) {
    let mut m_clone = map.clone();
    for y in 0..m_clone.len() {
        for x in 0..m_clone[0].len(){
            if path.contains(&(y*(m_clone[0].len()) + x)){
                m_clone[y][x] = '*';
            }
        }
    }
    print_map(&m_clone);
 }

 // Each cell is split into four nodes, one for each direction.
 // It costs 1000 to move between directions
 fn make_graph(map: &Vec<Vec<char>>) -> Vec<Vec<Edge>>{
    let map_width = map[0].len();
    let directions = [(-1,0), (0,1), (1, 0), (0, -1)];
    let mut graph = Vec::new();
    for (y, line) in map.into_iter().enumerate(){
        for (x, cell) in line.into_iter().enumerate(){
            let node_base_num = (map_width * y + x)*4;
            if *cell == '#'{ 
                graph.append( &mut vec![vec![]; 4]);
                continue
            } 
            for (n, d) in directions.iter().enumerate() {
                let mut node = Vec::new();
                if *cell != 'E' {
                    node.push(Edge{node: node_base_num + (n + 1) % 4, cost: 10000});
                    node.push(Edge{node: node_base_num + (n + 3) % 4, cost: 10000});
                } else { // We don't care what direction we enter the exit from
                    node.push(Edge{node: node_base_num + (n + 1) % 4, cost: 1});
                    node.push(Edge{node: node_base_num + (n + 3) % 4, cost: 1});                    
                }
                let poss_link = ((y as i32 + d.0) as usize, (x as i32 + d.1) as usize);
                if map[poss_link.0][poss_link.1] != '#' {
                    node.push(Edge{node: (map_width * poss_link.0 + poss_link.1)*4 + n, cost: 10});
                }
                graph.push(node);

            }
        }
    }
    graph
 }