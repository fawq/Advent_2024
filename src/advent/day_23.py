from copy import deepcopy
from itertools import combinations
from pathlib import Path

from advent.utils.graph import Edge, Graph
from advent.utils.load_file import File


def part1_solution(file_path: Path) -> int:
    graph: Graph[str] = Graph()

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        nodes = line.split("-")
        graph.add_edge_bidirectional(Edge(nodes[0],nodes[1]))

    count_lan_parties: int = 0
    for node in deepcopy(graph.get_nodes()):
        neighbors_nodes = graph.get_bidirectional_neighbors(node)
        for node_1, node_2 in combinations(neighbors_nodes, 2):
            if ((node[0] == "t" or 
                 node_1[0] == "t" or 
                 node_2[0] == "t") and
                Edge(node_1, node_2) in graph.get_bidirectional_edges_for_node(node_1)):
                count_lan_parties += 1
        graph.remove_node(node)

    return count_lan_parties

def part2_solution(file_path: Path) -> int:
    graph: Graph[str] = Graph()

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        nodes = line.split("-")
        graph.add_edge_bidirectional(Edge(nodes[0], nodes[1]))
    
    biggest_clique: set[str] = set()
    biggest_size: int = 1
    for node in graph.get_nodes():
        neighbors_nodes = graph.get_bidirectional_neighbors(node)
        for searched_size in range(len(neighbors_nodes), biggest_size, -1):
            for searched_neighbors_nodes in combinations(neighbors_nodes, searched_size):
                for pair in combinations(searched_neighbors_nodes, 2):
                    if not graph.check_if_edge_exists(Edge(pair[0], pair[1])):
                        break
                else:
                    biggest_clique = set(searched_neighbors_nodes) | {node}
                    biggest_size = searched_size

    return ",".join(sorted(biggest_clique))

def main() -> None:
    assert part1_solution("src/advent/day_23/data_test.txt") == 7
    print(f"Part 1: {part1_solution("src/advent/day_23/data.txt")}")
    assert part2_solution("src/advent/day_23/data_test.txt") == "co,de,ka,ta"
    print(f"Part 2: {part2_solution("src/advent/day_23/data.txt")}")