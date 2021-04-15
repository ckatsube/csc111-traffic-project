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
        - lat_and_long: The latitude and longitude of the location.
    """
    item: Any
    neighbours: dict[_Vertex, Union[int, float]]  # vertex and weight
    lat_and_long: tuple[float, float]

    def __init__(self, item: Any, latitude: str, longitude: str) -> None:
        """Initializing a new vertex.
        """
        self.item = item
        self.neighbours = {}
        self.lat_and_long = (float(latitude), float(longitude))

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

    def paths(self, item: Any, visited: set, curr_path: list, paths: list) -> None:
        """Returns a list of all the paths between self and item. This function works recursively,
        it works to find a path which ends on the target item and when it find that path it adds it
        to the list of returned paths."""

        visited.add(self.item)
        curr_path.append(self.item)

        if self.item == item:
            paths.append(list(curr_path))

        else:
            for neighbour in self.neighbours:
                if neighbour.item not in visited:
                    neighbour.paths(item, visited, curr_path, paths)

        curr_path.pop()
        visited.remove(self.item)


class Graph:
    """
    A Graph used to represent the network of checkpoint locations in Chicago City.
    """
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialising empty graph"""
        self._vertices = {}

    def add_vertex(self, item: Any, latitude: str, longitude: str) -> None:
        """Add a vertex with the given Street location.
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, latitude, longitude)

    def add_edge(self, item1: Any, item2: Any, speed: str, length: str) -> None:
        """Add a weighted edge between the two vertices with the given items in this graph.
        The weight of each edge is the amount of time it takes to travel along the given edge(route)
        """
        weight = float(length) / float(speed)
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

    def get_all_paths(self, item1: Any, item2: Any) -> list:
        """Returns a list of all the paths from item1 to item2 and uses the paths vertex helper.
        """
        all_paths = []
        v1 = self._vertices[item1]
        v1.paths(item2, set(), [], all_paths)
        return all_paths

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

    def get_weight(self, item1: Any, item2: Any) -> Union[int, float]:
        """Return the weight of the edge between the given items.
        Precondition:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def get_all_vertices(self) -> set:
        """Return a set of all vertex items in this graph.
        """
        return set(self._vertices.keys())

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.
        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_lat_long(self, list: Any) -> tuple:
        """Return te latitude and longitude of the vertices.
        """
        list_of_latitudes = []
        list_of_longitudes = []

        for location in list:
            list_of_latitudes.append(self._vertices[location].lat_and_long[0])
            list_of_longitudes.append(self._vertices[location].lat_and_long[1])

        return (list_of_latitudes, list_of_longitudes)


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
            if row[10] == '17' and row[11] == '4' and row[12] == '3':  # Only reads data for 5PM
                # Thursdays in March
                if not graph.check_in(row[6]):
                    graph.add_vertex(row[6], row[13], row[14])  # adding starting vertex if it's not
                    # in the graph already
                if not graph.check_in(row[7]):
                    graph.add_vertex(row[7], row[15], row[16])  # adding ending vertex if it's not
                    # in the graph already
                graph.add_edge(row[6], row[7], row[3],
                               row[8])  # represents a route from starting to
                # ending point

    return graph
