from __future__ import annotations
from typing import Any, Union
import csv
import networkx as nx

# The following code initialises the Vertex and Graph class, and also defines basic functions
# that we would use throughout our project. In addition to this it also has the function that
# constructs a graph with given dataset


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

    def print_all_connected(self, visited: set[_Vertex]) -> None:
        """Print all streets that this vertex is connected to.

        Example - To check the possible routes from Madison
        graph._vertices['Madison'].print_all_connected(set())
        """
        visited.add(self)
        print(self.item)

        for u in self.neighbours:
            if u not in visited:
                u.print_all_connected(visited)


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

    def add_edge(self, item1: Any, item2: Any, speed: str, length: str) -> None:
        """Add a weighted edge between the two vertices with the given items in this graph.
        The weight of each edge is the amount of time it takes to travel along the given edge(route)
        """
        weight = float(speed) / float(length)
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

    def check_in(self, user: str) -> bool:
        """
        Helper for load review graph. Checks if vertex does not already exist
        """
        if user in self._vertices:
            return True
        else:
            return False

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


def traffic_heuristic(item1, item2) -> float:
    """
    Returns the weight between two locations using the traffic heuristic.
    To be coded later.
    """


def load_graph(chicago_traffic_file: str) -> Graph:
    """Return a graph corresponding to the given dataset.
    We return a graph connecting 'from' and 'to' streets in each row
    row[5] refers to the starting point (street) and row[6] refers to the ending point (street).
    row[13] refers to the day of the week and row[14] refers to the month.
    For now, I am filtering rows and only reading ones for Thursday 5PM in March.

    row[2] refers to the speed and row [7] refers to the length of the route. We compute the
    weighted portion of the vertex by calculating length/speed to obtain the time taken between the
    starting and ending points.
    """
    graph = Graph()
    with open(chicago_traffic_file) as csv_file2:
        traffic_data = csv.reader(csv_file2)
        next(traffic_data)  # to skip the first row
        for row in traffic_data:
            if row[12] == '17' and row[13] == '4' and row[14] == '3':  # Only reads data for 5PM
                # Thursdays in March
                if not graph.check_in(row[5]):
                    graph.add_vertex(row[5])  # adding starting vertex if it's not
                    # in the graph already
                if not graph.check_in(row[6]):
                    graph.add_vertex(row[6])  # adding ending vertex if it's not
                    # in the graph already
                graph.add_edge(row[5], row[6], row[2], row[7])  # represents a route from starting to
                # ending point

    return graph


from plotly.graph_objs import Scatter, Figure

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'


def visualize_graph(graph: Graph,
                    layout: str = 'spring_layout',
                    max_vertices: int = 5000,
                    output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """
    graph_nx = graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)
    kinds = [graph_nx.nodes[k] for k in graph_nx.nodes]

    # colours = [BOOK_COLOUR if kind == 'book' else USER_COLOUR for kind in kinds]

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(color=LINE_COLOUR, width=1),
                     hoverinfo='none',
                     )
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=5,
                                 line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data1 = [trace3, trace4]
    fig = Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)
