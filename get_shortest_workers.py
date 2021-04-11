"""
Functions which make use of the graphs and maps generated using dijkstra's algorithm to return the
shortest path between two points in the graph , which goes through a certain no. of specified points
.
"""
from __future__ import annotations

from graph import load_graph, Graph
from pathcalculator import get_shortest_map_and_graph
from typing import Any, Optional


def gets_original_gives_full_path(graph: Graph, starting_point: Any, ending_point: Any,
                                  points: list[Any]) -> list[Any]:
    """
    This function returns the shortest path for traversing between 2 street landmarks which takes a
    route which goes through a certain no. of specified points.
    """
    s = get_shortest_map_and_graph(graph, starting_point, ending_point, points)
    shortest_path = connected_with(s[1], starting_point, ending_point, points)
    shortest_map = s[0]
    output = []
    for i in range(len(shortest_path) - 1):
        start = shortest_path[i]
        end = shortest_path[i + 1]
        output.append(shortest_map[start][end])

    full_path = []
    for path in output:
        for _ in range(len(path) - 1):
            full_path.append(path.get_item())
            path = path.get_next()
    full_path.append(ending_point)

    return full_path


def connected_with(graph: Graph, starting_point: Any, ending_point: Any,
                   in_between: list[Any]) -> Optional[list, str]:
    """
    This function returns the shortest path, based on the shortest graph, between two points in our
    graph, which goes through a certain no. of specified points.
    """
    z = graph.get_all_paths(starting_point, ending_point)
    d = []
    for i in z:
        if len(i) == 2 + len(in_between):
            d.append((i, get_path_weight(graph, i)))

    d.sort(key=lambda q: q[1])
    return d[0][0]


def get_path_weight(graph: Graph, path: list) -> float:
    """
    This is a rudimentary function which gets us the path_weight between two points on the shorter
    graph.
    """
    s = 0.0
    for i in range(len(path) - 1):
        s = s + graph.get_weight(path[i], path[i + 1])
    return s

# Sample Call
# g = load_graph('data/chicago_dataset_1.csv')
# end = 'Kinzie'
# visitor = ['26th', '18TH', 'Indianapolis', 'Indiana', 'Michigan', 'Peterson', '75th', '96th']
# start = '1550 West'
# full_path = gets_original_gives_full_path(g, start, end, visitor)
