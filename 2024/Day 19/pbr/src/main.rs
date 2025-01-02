use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashSet};

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Only the one argument please! Just the filename!");
    } 
    let inputloc = &args[1];
    let (mut towels, patterns) = get_inputs(inputloc).unwrap();
    towels.sort_by(|a, b| {
        match a.len().cmp(&b.len()){
            std::cmp::Ordering::Equal => a.cmp(b),
            ordering => ordering
        }
    });
    let graph = build_graph(&towels);

    let mut npatterns = 0;
    let mut nvalid = 0;
    for pattern in &patterns[..]{
        if let Some(i) = find_string(&graph, &pattern) {
            npatterns += get_num_paths(&i, &towels);
            nvalid += 1;
        }
    }
    println!("Part 1: {}", nvalid);
    println!("Part 2: {}", npatterns);
    
}
 

fn get_inputs<P>(filename: P) -> io::Result<(Vec<String>, Vec<String>)>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut towels = Vec::new();
    let mut patterns = Vec::new();


    for (i, j) in reader.lines().enumerate() {
        let line = j?;
        match i {
            0 => towels = line.split(", ").map(|x| x.to_string()).collect(),
            1 => continue,
            _ => patterns.push(line)
        }
    }

    Ok((towels, patterns))
}

#[derive (Debug, Clone)]
struct Node{
    out_edges: Vec<Edge>,
}

#[derive (Debug, Clone)]
struct Edge{
    target: usize,
    target_colour: char, // Save time looking ahead
    towel_num: Option<usize>,
}

#[derive(Debug, Copy, Clone, Eq, PartialEq)]
struct State {
    string_pos: usize,
    position: usize, //position in the graph
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.string_pos.cmp(&self.string_pos)
            .then_with(|| self.position.cmp(&other.position))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn build_graph(towels: &Vec<String>) -> Vec<Node> {
    let mut graph = Vec::<Node>::new();
    // Make start node
    graph.push(Node{
        out_edges: Vec::<Edge>::new(),
    });
    let mut next_node = 0;
    // Add towels to graph
    for (i, towel) in towels.into_iter().enumerate() {
        let towel_chars: Vec<char> = towel.chars().collect();
        let mut node: Node;
        let mut current_pos = 0;
        'towelchars: for i in 0..towel_chars.len(){
            // step into the graph
            for edge in &graph[current_pos].out_edges{
                if edge.target_colour == towel_chars[i] {
                    current_pos = edge.target;
                    continue 'towelchars;
                }
            } // If the node doesn't already exist
            next_node += 1;
            graph[current_pos].out_edges.push(Edge{target: next_node, target_colour: towel_chars[i], towel_num: None});
            node = Node{
                out_edges: Vec::new()
            };
            graph.push(node);
            current_pos = next_node;
        }
        graph[current_pos].out_edges.push(Edge {
            target: 0,
            target_colour: 'S',
            towel_num: Some(i)
        });
    }
    graph
}

fn find_string(adj_list: &Vec<Node>, target: &str) -> Option<Vec<HashSet<usize>>> {
    //n_valid_paths, for each position in the string, which strings correctly ended on that position
    let mut valid_paths = vec![HashSet::new(); target.len()];
    let mut heap = BinaryHeap::new();
    let mut visited = HashSet::new();
    let target: Vec<char> = target.chars().collect();
    let target_length = target.len();

    heap.push(State {string_pos: 0, position: 0});

    while let Some(State {string_pos, position}) = heap.pop() {
        // If we're back at the start and we've seen all of the string
        if position == 0 && string_pos == target_length {
            return Some(valid_paths)
        }
        if string_pos > target_length || !visited.insert((string_pos, position)) {
            continue;
        }
        for edge in &adj_list[position].out_edges {
            let next_str_pos;
            if edge.target_colour == 'S' {
                next_str_pos = string_pos;
                valid_paths[string_pos - 1].insert(edge.towel_num?);
            } else {
                next_str_pos = string_pos + 1;
            }
            if next_str_pos > target_length {
                continue
            }
            let next = State{string_pos: next_str_pos, position: edge.target};
            if edge.target_colour == target[next_str_pos - 1] || edge.target_colour == 'S' {
                heap.push(next);
            }
            
        }
    }

    None
}

fn get_num_paths(valid_ends: &Vec<HashSet<usize>>, towels: &Vec<String>) -> usize {
    let mut num_routes = vec![0;valid_ends.len()];
    for (i, ends) in valid_ends.into_iter().enumerate(){
        num_routes[i] = match i {
            0 => ends.len(),
            _ => ends.into_iter().fold(0, |acc, x| {
                let y = towels[*x].len() - 1;
                if y > i {
                    panic!("disaster!");
                } else if y == i{
                    acc + 1
                } else {
                    acc + num_routes[i - y - 1]
                }
            })
        };

    }
    num_routes[num_routes.len()-1]
}