use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::{HashMap, HashSet};

#[derive(Debug)]
struct Node {
    edges: Vec<Edge>,
}

#[derive(Debug, PartialEq, Clone)]
struct Edge {
    to: String,
}

fn main() {
    env::set_var("RUST_BACKTRACE", "1");
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Only the one argument please! Just the filename!");
    } 
    let inputloc = &args[1];

    let graph = get_input(inputloc).unwrap();
    println!("Part 1: {}", p1(&graph));
    println!("Part 2: {}", p2(&graph));
}

fn get_input<P>(filename: P) -> io::Result<HashMap<String, Node>>
where P: AsRef<Path> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut out: HashMap<String, Node> = HashMap::new();

    for line in reader.lines() {
        let line = line?;
        let cpu1 = &line[..2];
        let cpu2 = &line[3..];
        out.entry(cpu1.to_string())
            .and_modify(|x| {x.edges.push(Edge{to: cpu2.to_string()})})
            .or_insert(Node{edges: vec![Edge{to: cpu2.to_string()}]});
        out.entry(cpu2.to_string())
            .and_modify(|x| {x.edges.push(Edge{to: cpu1.to_string()})})
            .or_insert(Node{edges: vec![Edge{to: cpu1.to_string()}]});
    }  

    Ok(out)
}

fn p1(input: &HashMap<String, Node>) -> usize {
    // Find 3-cliques where one of the computers starts with t
    let mut cliques = HashSet::new();
    // loop through every computer
    let keys = input.keys();
    
    for key in keys{
        // only care if the first letter is t
        if key.chars().nth(0).unwrap() != 't'{
            continue
        }
        // for each computer those connect to
        for connection in &input[key].edges[..] {
            // if that computer connects to a computer that this one also connects
            // to then this is a 3-clique
            for cpu in &input[&connection.to].edges[..] {
                if input[key].edges.contains(&cpu){
                    let mut clique = vec![&key, &connection.to, &cpu.to];
                    clique.sort();
                    cliques.insert((clique[0].to_string(), clique[1].to_string(), clique[2].to_string()));
                }
            }
        }
    }
    cliques.len()
}

fn p2(input: &HashMap<String, Node>) -> String{
        let potential: HashSet<String> = input.keys().cloned().collect();
        let cliques = bron_kerbosch(HashSet::new(), potential, HashSet::new(), input);
        let mut cliques: Vec<String> = cliques.into_iter().collect();
        cliques.sort_by(|a, b| b.len().cmp(&a.len()));
        cliques[0].clone()
}


/* Sketch of method:
Choose a starting point: 
    for each connected node:
        does it connect to any of the connections of the layer above?
        if yes: 
            run the above logic on the first of those
        if no: 
            not a clique

*/

// I'm very tired, so I'm going to code up someone else's algorithm. It does 
// follow what I've written above, so I was doing the right thing!
//It's not a good implementation though, and has way too many copies!
fn bron_kerbosch(current: HashSet<String>,
                 potential: HashSet<String>,
                 excluded: HashSet<String>,
                 graph: &HashMap<String, Node>) -> HashSet<String> {
    let mut cliques: HashSet<String> = HashSet::new();
    // If we're out of potential and excluded nodes, then the current clique
    // is maximal
    if potential.len() == 0 && excluded.len() == 0 {
        // store cliques in the output format: in alphabetical order separated by commas
        let mut clique: Vec<String> = current.into_iter().collect();
        clique.sort();
        cliques.insert(clique.join(","));
        return cliques
    }
    let mut potential_self = potential.clone();
    let mut excluded_self = excluded.clone();
    // Otherwise
    for vertex in potential.clone().into_iter() {   // For every remaining node
        let mut next_curr = current.clone(); 
        next_curr.insert(vertex.clone());  // Add the node to the clique
        let neighbours = graph[&vertex] // This is very slow and could be avoided by just changing the input struct
                            .edges
                            .clone()
                            .into_iter()
                            .fold(HashSet::new(),
                                    |mut acc, x|
                                    {acc.insert(x.to); acc});
        let next_potential: HashSet<String> = potential_self
                        .intersection(
                            &neighbours).cloned().collect(); // Remove all non-common neigbours
        let next_excluded: HashSet<String> = excluded_self.intersection(&neighbours).cloned().collect();
        cliques = cliques.union(&bron_kerbosch(next_curr, next_potential, next_excluded, graph)).cloned().collect();
        excluded_self.insert(vertex.clone());
        potential_self.remove(&vertex);
    }
    cliques
}