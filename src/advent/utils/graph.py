from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class Edge[T]:
    node_from: T
    node_to: T

    def get_opposite_direction(self) -> Self:
        return self.__class__(self.node_to, self.node_from)

@dataclass
class Graph[T]:
    nodes: set[T] = field(default_factory=set)
    edges: set[Edge[T]] = field(default_factory=set)

    def add_node(self, node: T) -> None:
        self.nodes.add(node)

    def _add_missing_nodes_for_edge(self, edge: Edge[T]) -> None:
        node_from = edge.node_from
        node_to = edge.node_to
        if node_from not in self.nodes:
            self.add_node(node_from)
        if node_to not in self.nodes:
            self.add_node(node_to)

    def add_edge(self, edge: Edge[T]) -> None:
        self._add_missing_nodes_for_edge(edge)
        self.edges.add(edge)

    def add_edge_bidirectional(self, edge: Edge[T]) -> None:
        self._add_missing_nodes_for_edge(edge)
        self.add_edge(edge)
        self.add_edge(edge.get_opposite_direction())

    def get_nodes(self) -> set[T]:
        return self.nodes
    
    def get_edges(self) -> set[Edge[T]]:
        return self.edges
    
    def get_edges_for_node(self, node: T) -> set[Edge[T]]:
        return {edge for edge in self.edges if edge.node_from == node}
    
    def get_edges_to_node(self, node: T) -> set[Edge[T]]:
        return {edge for edge in self.edges if edge.node_to == node}
    
    def get_bidirectional_edges_for_node(self, node: T) -> set[Edge[T]]:
        return {edge for edge in self.edges if edge.node_from == node or edge.node_to == node}
    
    def get_neighbors(self, node: T) -> set[T]:
        return {edge.node_to for edge in self.get_edges_for_node(node)}
    
    def get_bidirectional_neighbors(self, node: T) -> set[T]:
        return {edge.node_to if edge.node_from == node else edge.node_from for edge in self.get_bidirectional_edges_for_node(node)}
    
    def check_if_node_exists(self, node: T) -> bool:
        return node in self.nodes
    
    def check_if_edge_exists(self, edge: Edge[T]) -> bool:
        return edge in self.edges
    
    def remove_edge(self, edge: Edge[T]) -> None:
        self.edges.discard(edge)

    def remove_edge_bidirectional(self, edge: Edge[T]) -> None:
        self.remove_edge(edge)
        self.remove_edge(edge.get_opposite_direction())
    
    def remove_node(self, node: T) -> None:
        self.nodes.remove(node)
        for edge in self.get_bidirectional_edges_for_node(node):
            self.remove_edge_bidirectional(edge)