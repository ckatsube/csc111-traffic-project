"""
CSC111 Project: pathcalculator.py

Module Description
==================

Module which contains the methods and classes related to calculating the shortest path. We use the
heapq module in the implementation of our functions. The main algorithm used for calculating the
shortest path is Dijkstra's Algorithm.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Aryaman Modi, Craig Katsube, Garv Sood, Kaartik Issar

"""

from __future__ import annotations

from abc import ABC
from typing import Any
from collections.abc import Iterable, Iterator

import heapq
from graph import Graph

#############################################################################
# PUBLIC INTERFACE
#############################################################################


def get_shortest_path_map(g: Graph,
                          start: Any, end: Any, points: list) -> dict[Any, dict[Any, Path]]:
    """Return the mapping of relevant shortest paths between points from start to end

    Output format:
        - dict[a][b] == Shortest path from a to b
        - dict[b][a] == Shortest path from b to a

    All internal points are mapped to all other internal points
        - dict[a][b] for any unique pair a and b in points
    The start key is mapped to all internal points (one direction)
        - dict[start][a] for any a in points
    All internal points are mapped to the end point (one direction)
        - dict[a][end] for any a in points
    """

    shortest_map = {start: {},
                    end: {}}
    for point in points:
        shortest_map[point] = {}

    for point in points:
        for other in points:
            if other != point:
                shortest_path = _dijkstra(g, point, other)
                reverse = shortest_path.get_reversed()

                shortest_map[point][other] = shortest_path
                shortest_map[other][point] = reverse

        from_start = _dijkstra(g, start, point)
        shortest_map[start][point] = from_start

        to_end = _dijkstra(g, point, end)
        shortest_map[point][end] = to_end

    return shortest_map


def convert_shortest_map_to_graph(shortest_map: dict[Any, dict[Any, Path]]) -> Graph:
    """Return the graph containing information about the shortest distance between points
    using the edges contained within the shortest_map
    """

    shortest_graph = Graph()

    points = _get_all_points(shortest_map)

    for point in points:
        shortest_graph.add_vertex(point, '0', '0')

    for point, end_points in shortest_map.items():
        for end_point, path in end_points.items():
            shortest_graph.add_edge(point, end_point, 1, path.get_path_weight())

    return shortest_graph


def get_shortest_map_and_graph(g: Graph, start: Any, end: Any, points: list) ->\
        tuple[dict[Any, dict[Any, Path]], Graph]:
    """Return both the shortest map and graph according to get_shortest_map and _graph
    """

    shortest_map = get_shortest_path_map(g, start, end, points)
    shortest_graph = convert_shortest_map_to_graph(shortest_map)

    return shortest_map, shortest_graph


def get_shortest_graph(g: Graph, start: Any, end: Any, points: list) -> Graph:
    """Return a graph containing information about the shortest distance between points

    The subgraph containing the sub-points is a complete graph
    The start and end points are both connected to all internal points, but not to each other
    """

    shortest_map = get_shortest_path_map(g, start, end, points)
    return convert_shortest_map_to_graph(shortest_map)


def dijkstra(g: Graph, start: Any, end: Any) -> Path:
    """Return the Path containing the smallest cumulative weight from point a to b"""
    return _dijkstra(g, start, end)


class Path(Iterable):
    """Interface for getting information about a path"""

    def __len__(self) -> int:
        raise NotImplementedError

    def get_weight(self) -> float:
        """Return the weight of this Path"""
        raise NotImplementedError

    def get_path_weight(self) -> float:
        """Return the cumulative weight along the path this Path is a part of"""
        raise NotImplementedError

    def get_item(self) -> Any:
        """Return the item associated with this Path"""
        raise NotImplementedError

    def get_reversed(self) -> _Node:
        """Return the Path in reverse order from self"""
        raise NotImplementedError

    def __iter__(self) -> _PathIterator[Any]:
        """Return an iterator that can traverse the path"""
        raise NotImplementedError

    def __lt__(self, other: Path) -> bool:
        """Return whether this Path has a smaller weight than the other Path"""
        return self.get_path_weight() < other.get_path_weight()


#############################################################################
# PRIVATE INTERFACE
#############################################################################


def _dijkstra(g: Graph, start: Any, end: Any) -> _Node:
    """Return the _Node containing the smallest cumulative weight from point a to b"""

    # starts at the end because the path is built in reverse order
    item_end = end
    p_end = _PathNode(item_end, 0)

    visited_vertices = {item_end: p_end}

    heap = [p_end]

    def recursive_dijkstra() -> _Node:
        """Recursively calls the dijkstra alg on the globally accessible heap"""

        heap_is_not_empty = (heap != [])
        if heap_is_not_empty:

            p = heapq.heappop(heap)
            v = p.get_item()
            visited_vertices[v] = p

            end_of_path = (v == start)
            if end_of_path:
                return p

            for neighbour_vertex in g.get_neighbours(v):
                u = neighbour_vertex.item

                if u not in visited_vertices:
                    weight = g.get_weight(u, v)
                    next_path = _PathNode(u, weight, p)
                    heapq.heappush(heap, next_path)

            return recursive_dijkstra()
        else:
            return _NullPathNode()

    return recursive_dijkstra()


def _get_all_points(shortest_map: dict[Any, dict[Any, Path]]) -> set[Any]:
    key_set = set(shortest_map)
    one_value_set = set(list(shortest_map.values())[0])
    # the key_set contains all points except the end point.
    # All value sets contain the end point (so only one is needed to get it)
    return set.union(key_set, one_value_set)


class _Node(Path, ABC):
    """Abstract Iterable class for hiding the interface for manually iterating through the path"""

    def get_next(self) -> _Node:
        """Return the _Node preceding this _Node in the path"""
        raise NotImplementedError

    def __iter__(self) -> _PathIterator:
        return _ItemIterator(self)


class _NullPathNode(_Node):
    """Null object pattern to represent the end of a path"""

    def get_item(self) -> Any:
        """Return None since this _Node has no item"""
        return None

    def get_weight(self) -> float:
        """There is no parent, hence no weight, so return 0"""
        return 0

    def get_path_weight(self) -> float:
        """There is no path, hence no weight, so return 0"""
        return 0

    def get_reversed(self) -> _Node:
        """Return a copy of self since no reverse exists"""
        return _NullPathNode()

    def get_next(self) -> _Node:
        """Raise a stop iteration error because no next exists"""
        raise StopIteration

    def __len__(self) -> int:
        return 0


class _PathNode(_Node):
    """Path node for containing information about a path

    """
    # Private Instance Attributes:
    #   - item: the value of this node
    #   - next: the node in the path prior to this one
    #   - _path_weight: the cumulative weight along the entire path
    #   - _weight: the weight between this node and its self.next
    #   - _size: the size of this path

    _item: Any
    _next: _PathNode
    _path_weight: float
    _weight: float
    _size: int

    def __init__(self, item: Any, weight: float, parent: _PathNode = _NullPathNode()) -> None:
        self._next = parent
        self._item = item

        self._size = len(parent) + 1
        self._weight = weight
        self._path_weight = parent.get_path_weight() + weight

    def __len__(self) -> int:
        return self._size

    def get_item(self) -> Any:
        """Return the item associated with this _PathNode"""
        return self._item

    def get_reversed(self) -> _Node:
        """Return the _PathNode at the end of an entirely reversed chain"""
        parent = _NullPathNode()
        for node in _NodeIterator(self):
            parent = _PathNode(node.get_item(), node.get_weight(), parent)

        return parent

    def get_next(self) -> _Node:
        """Return the _Node preceding this one in the path"""
        return self._next

    def get_path_weight(self) -> float:
        """Return the cumulative weight of this path"""
        return self._path_weight

    def get_weight(self) -> float:
        """Return the weight of this path node to its parent"""
        return self._weight


class _PathIterator(Iterator[Any]):
    """Iterator pattern class for iterating through a Path"""

    def __next__(self) -> Any:
        raise NotImplementedError


class _ItemIterator(_PathIterator[Any]):
    """Iterator pattern class for iterating through the items in a path formed by _PathNodes

    Iterates through the _PathNode .next chain in order and returns the item of each _Node.
    """

    _wrapped_iterator: _NodeIterator

    def __init__(self, initial_node: _Node) -> None:
        self._wrapped_iterator = _NodeIterator(initial_node)

    def __next__(self) -> Any:
        node = self._wrapped_iterator.__next__()
        return node.get_item()


class _NodeIterator(_PathIterator[_Node]):
    """Iterator pattern class for iterating through the _Node chain

    Returns the _Node object at each iteration
    """

    _current_node: _Node

    def __init__(self, initial_node: _Node) -> None:
        self._current_node = initial_node

    def __next__(self) -> _Node:
        cur = self._current_node
        self._current_node = self._current_node.get_next()
        return cur


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9971'],
        'extra-imports': ['heapq', 'graph', 'abc'],
        'allowed-io': [],
        'max-nested-blocks': 5

    })
