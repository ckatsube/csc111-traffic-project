"""Module for the graph and its related content"""

from __future__ import annotations

from typing import Any, Union
import networkx as nx


class _Vertex:
    """A vertex in the Graph that represents a checkpoint location in Chicago city.

        Instance Attributes:
        - item: The name of street location.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.
    """
    item: Any
    neighbours: dict[_Vertex, Union[int, float]]  # vertex and weight

    def __init__(self, item: Any) -> None:
        """Initializing a new vertex.
        """
        self.item = item
        self.neighbours = {}

    def check_connected(self, target_item: Any, visited: set[_Vertex]) -> bool:
        """Return whether this vertex is connected to a vertex corresponding to target_item,
        by a path that DOES NOT use any vertex in visited.
        """
        if self.item == target_item:
            return True
        else:
            visited.add(self)

            for u in self.neighbours:
                if u not in visited:
                    if u.check_connected(target_item, visited):
                        return True

            return False

    def print_all_connected(self) -> None:
        """Print all streets that this vertex is connected to.

        Example - To check the possible routes from Madison
        graph._vertices['Madison'].print_all_connected(set())
        """

        self._print_all_connected(set())

    def _print_all_connected(self, visited: set[_Vertex]) -> None:
        visited.add(self)
        print(self.item)

        for u in self.neighbours:
            if u not in visited:
                u._print_all_connected(visited)


class Graph:
    """
    A Graph used to represent the network of checkpoint locations in Chicago City.
    """
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialising empty graph"""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given Street location.
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item)

    def add_edge(self, item1: Any, item2: Any, weight: float) -> None:
        """Add a weighted edge between the two vertices with the given items in this graph.
        The weight of each edge is the amount of time it takes to travel along the given edge(route)
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            v1.neighbours[v2], v2.neighbours[v1] = weight, weight
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """
        Return if the following two locations are adjacent.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            for v2 in v1.neighbours:
                if v2.item == item2:
                    return True
            return False
        else:
            return False

    def get_neighbours(self, item1: Any) -> set[Any]:
        """Return an unordered collection of all items that are adjacent to item1"""
        if item1 in self._vertices:
            return {v.item for v in self._vertices[item1].neighbours}
        else:
            raise ValueError()

    def check_in(self, item: str) -> bool:
        """
        Helper for load review graph. Checks if vertex does not already exist
        """
        return item in self._vertices

    # temp function for visualization
    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx

    def connected(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are connected vertices
        in this graph.

        Return False if item1 or item2 do not appear as vertices
        in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]

            return v1.check_connected(item2, set())
        else:
            return False

    def in_cycle(self, item: Any) -> bool:
        """Return whether the given item is in a cycle in this graph.

        Return False if item does not appears as a vertex in this graph.
        """
        if item not in self._vertices:
            return False
        else:
            if len(self._vertices[item].neighbours) >= 2:
                for n in self._vertices[item].neighbours:
                    if n.check_connected(item, set()) and len(n.neighbours) >= 2:
                        return True
            return False
