"""Module for containing methods and classes related to calculating the shortest path
"""

from __future__ import annotations

from abc import ABC
from typing import Any, Iterable, Iterator

import heapq

Graph = __import__("Graph & Node").Graph
Vertex = __import__("Graph & Node")._Vertex

#############################################################################
# PUBLIC INTERFACE
#############################################################################


def dijkstra(g: Graph, a: Any, b: Any) -> Path:
    """Return the Path containing the smallest cumulative weight from point a to b"""

    v_i = g._vertices[a]
    p_i = _PathNode(v_i.item, 0)
    visited_vertices = {v_i: p_i}

    heap = [p_i]

    def recursive_dijkstra() -> Path:
        """Recursively calls the dijkstra alg on the globally accessible heap"""

        heap_is_not_empty = (heap != [])
        if heap_is_not_empty:

            p = heapq.heappop(heap)
            v = g._vertices[p.get_item()]
            visited_vertices[v] = p

            end_of_path = v.item == b
            if end_of_path:
                return p

            for neighbour, weight in v.neighbours.items():
                if neighbour not in visited_vertices:
                    next_path = _PathNode(neighbour.item, weight, p)
                    heapq.heappush(heap, next_path)

            return recursive_dijkstra()
        else:
            return _NullPathNode()

    return recursive_dijkstra()


class Path(Iterable):
    """Public interface containing the information for a path"""

    def __len__(self) -> int:
        raise NotImplementedError

    def get_weight(self) -> float:
        """Return the weight of this _Node"""
        raise NotImplementedError

    def get_path_weight(self) -> float:
        """Return the cumulative weight along the path this _Node is a part of"""
        raise NotImplementedError

    def get_item(self) -> Any:
        """Return the item associated with this _Node"""
        raise NotImplementedError

    def __iter__(self) -> Iterator[Any]:
        """Return an iterator that can traverse the path"""
        raise NotImplementedError

    def __lt__(self, other: Path):
        """Return whether this Path has a smaller weight than the other Path"""
        return self.get_path_weight() < other.get_path_weight()


#############################################################################
# PRIVATE INTERFACE
#############################################################################

class _Node(Path, ABC):
    """Abstract Iterable class for hiding the interface for manually iterating through the path"""

    def get_next(self) -> _Node:
        """Return the _Node preceding this _Node in the path"""
        raise NotImplementedError

    def __iter__(self) -> _PathIterator:
        return _PathIterator(self)


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

    def __init__(self, item: Any, weight: float, parent: _PathNode = _NullPathNode()):
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
    """Iterator pattern class for iterating through the path formed by _PathNodes

    Iterates through the _PathNode .next chain in order.
    """

    _current_node: _Node

    def __init__(self, initial_node: _Node):
        self._current_node = initial_node

    def __next__(self) -> Any:
        cur = self._current_node
        self._current_node = self._current_node.get_next()
        return cur.get_item()
