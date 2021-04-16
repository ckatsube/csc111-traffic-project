"""CSC111 Project: Graph & Node.py
Module Description
==================
The following code initialises the Vertex and Graph class, and also defines basic functions that we
would use throughout our project. In addition to this it also has the function that constructs a
graph from a given dataset

Some functions present in the Vertex and Graph classes have been provided to us by Professor David
Liu during our CSC111 lectures and the Amazon Book Recommendations assignment (Assignment 3)
All other functions have been made by Kaartik Isaar, Aryaman Modi, Craig Katsube and Garv Sood

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Kaartik Isaar, Aryaman Modi, Craig Katsube and Garv Sood
"""

from __future__ import annotations
from typing import Any, Union
import csv


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
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12", "14")  # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11", "13")
        >>> g.add_vertex("Chicago Square", "10", "14")
        >>> g.add_vertex("23rd", "1", "14")
        >>> g.add_vertex("Avenue", "2", "14")
        >>> g.add_edge("Bay Road", "22nd", "34", "23")
        >>> g.add_edge("Chicago Square", "22nd", "33", "22")
        >>> g.add_edge("Chicago Square", "Avenue", "31", "2")
        >>> v1 = g.get_vertex("Bay Road")
        >>> v1.check_connected("Avenue", set())
        True
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
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12", "14")  # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11", "13")
        >>> g.add_vertex("Chicago Square", "10", "14")
        >>> g.add_vertex("23rd", "1", "14")
        >>> g.add_vertex("Avenue", "2", "14")
        >>> g.add_edge("Bay Road", "22nd", "34", "23")
        >>> g.add_edge("Chicago Square", "22nd", "33", "22")
        >>> g.add_edge("Chicago Square", "Avenue", "31", "2")
        >>> v1 = g.get_vertex("Bay Road")
        >>> v1.print_all_connected(set())
        Bay Road
        22nd
        Chicago Square
        Avenue
        """
        visited.add(self)
        print(self.item)

        for u in self.neighbours:
            if u not in visited:
                u.print_all_connected(visited)

    def paths(self, item: Any, visited: set, curr_path: list, paths: list) -> None:
        """Returns a list of all the paths between self and item. This function works recursively,
        it works to find a path which ends on the target item and when it find that path it adds it
        to the list of returned paths.
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12", "14")  # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11", "13")
        >>> g.add_vertex("Chicago Square", "10", "14")
        >>> g.add_vertex("23rd", "1", "14")
        >>> g.add_vertex("Avenue", "2", "14")
        >>> g.add_edge("Bay Road", "22nd", "34", "23")
        >>> g.add_edge("Chicago Square", "22nd", "33", "22")
        >>> g.add_edge("Chicago Square", "Avenue", "31", "2")
        >>> v1 = g.get_vertex("Bay Road")
        >>> path = []
        >>> v1.paths("Avenue",set(), [], path)
        >>> path
        [['Bay Road', '22nd', 'Chicago Square', 'Avenue']]
        """

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
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12", "14")  # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11", "13")
        >>> g.add_vertex("Chicago Square", "10", "14")
        >>> g.add_vertex("23rd", "1", "14")
        >>> g.add_vertex("Avenue", "2", "14")
        >>> g.add_edge("Bay Road", "22nd", "34", "23")  # 2 items that need to be connected along with speed and length values
        >>> g.add_edge("Chicago Square", "22nd", "33", "22")
        >>> g.adjacent("Bay Road", "22nd")
        True
        >>> g.adjacent("Bay Road", "Chicago Square")
        False
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
        >>> g = Graph()
        >>> g.add_vertex("Madison", "12.55", "14") # name of street with its coordinates
        >>> g.add_vertex("21st", "2", "4.65")
        >>> g.add_vertex("501st", "12", "14.78")
        >>> g.add_vertex("Avenue", "12.3", "14.06")
        >>> g.check_in("21st")
        True
        >>> g.check_in("City Center")
        False
        """
        if user in self._vertices:
            return True
        else:
            return False

    def get_all_paths(self, item1: Any, item2: Any) -> list:
        """Returns a list of all the paths from item1 to item2 and uses the paths vertex helper.
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12", "14")  # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11", "13")
        >>> g.add_vertex("Chicago Square", "10", "14")
        >>> g.add_vertex("23rd", "1", "14")
        >>> g.add_vertex("Avenue", "2", "14")
        >>> g.add_edge("Bay Road", "22nd", "34", "23")  # 2 items that need to be connected along with speed and length values
        >>> g.add_edge("Chicago Square", "22nd", "33", "22")
        >>> g.add_edge("Chicago Square", "Avenue", "31", "2")
        >>> g.add_edge("Bay Road", "Avenue", "39", "29")
        >>> g.add_edge("Avenue", "22nd", "3", "2")
        >>> g.get_all_paths("Bay Road", "Avenue")
        [['Bay Road', '22nd', 'Chicago Square', 'Avenue'], ['Bay Road', '22nd', 'Avenue'], ['Bay Road', 'Avenue']]
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
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12", "14")  # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11", "13")
        >>> g.add_vertex("Chicago Square", "10", "14")
        >>> g.add_vertex("23rd", "1", "14")
        >>> g.add_vertex("Avenue", "2", "14")
        >>> g.add_edge("Bay Road", "22nd", "34", "23")
        >>> g.add_edge("Chicago Square", "22nd", "33", "22")
        >>> g.add_edge("Chicago Square", "Avenue", "31", "2")
        >>> g.connected("Chicago Square", "Bay Road")
        True
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]

            return v1.check_connected(item2, set())
        else:
            return False

    def in_cycle(self, item: Any) -> bool:
        """Return whether the given item is in a cycle in this graph.
        Return False if item does not appears as a vertex in this graph.
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12", "14")  # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11", "13")
        >>> g.add_vertex("Chicago Square", "10", "14")
        >>> g.add_vertex("23rd", "1", "14")
        >>> g.add_vertex("Avenue", "2", "14")
        >>> g.add_edge("Bay Road", "22nd", "34", "23")
        >>> g.add_edge("Chicago Square", "22nd", "33", "22")
        >>> g.add_edge("Bay Road", "Avenue", "39", "29")
        >>> g.add_edge("Avenue", "22nd", "3", "2")
        >>> g.in_cycle("Bay Road")
        True
        >>> g.in_cycle("Chicago Square")
        False
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
        """Return the weight (time taken) of the edge between the given items (streets).
        Precondition:
            - item1 and item2 are vertices in this graph
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12", "14")  # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11", "13")
        >>> g.add_vertex("Chicago Square", "10", "14")
        >>> g.add_vertex("23rd", "1", "14")
        >>> g.add_vertex("Avenue", "2", "14")
        >>> g.add_edge("Bay Road", "22nd", "34", "23")
        >>> g.add_edge("Chicago Square", "22nd", "33", "22")
        >>> g.add_edge("Chicago Square", "Avenue", "31", "2")
        >>> g.add_edge("Bay Road", "Avenue", "39", "29")
        >>> g.add_edge("Avenue", "22nd", "3", "2")
        >>> g.get_weight("Bay Road", "Avenue")  # weight (time taken) between these 2 points
        0.7435897435897436
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def get_all_vertices(self) -> set:
        """Return a set of all vertex items in this graph.
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12", "14")  # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11", "13")
        >>> g.add_vertex("Chicago Square", "10", "14")
        >>> g.add_vertex("23rd", "1", "14")
        >>> g.add_vertex("Avenue", "2", "14")
        >>> g.get_all_vertices() == {'Avenue', 'Chicago Square', 'Bay Road', '22nd', '23rd'}
        True
        """
        return set(self._vertices.keys())

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.
        Raise a ValueError if item does not appear as a vertex in this graph.
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12", "14")  # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11", "13")
        >>> g.add_vertex("Chicago Square", "10", "14")
        >>> g.add_vertex("23rd", "1", "14")
        >>> g.add_vertex("Avenue", "2", "14")
        >>> g.add_edge("Bay Road", "22nd", "34", "23")
        >>> g.add_edge("Chicago Square", "22nd", "33", "22")
        >>> g.add_edge("Chicago Square", "Avenue", "31", "2")
        >>> g.add_edge("Bay Road", "Avenue", "39", "29")
        >>> vertices = g.get_neighbours("Bay Road")
        >>> {v.item for v in vertices} == {"22nd", "Avenue"}
        True
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_lat_long(self, lst: Any) -> tuple:
        """Return the latitude and longitude of the vertices.
        >>> g = Graph()
        >>> g.add_vertex("Bay Road", "12.02", "14.24") # street name with the latitude and longitude
        >>> g.add_vertex("22nd", "11.43", "13.75")
        >>> g.add_vertex("Chicago Square", "10.0", "14.56")
        >>> g.add_vertex("23rd", "1.55", "14.65")
        >>> g.add_vertex("Avenue", "2.66", "14.23")
        >>> g.get_all_lat_long(["Chicago Square", "Avenue", "23rd"])
        ([10.0, 2.66, 1.55], [14.56, 14.23, 14.65])
        """
        list_of_latitudes = []
        list_of_longitudes = []

        for location in lst:
            list_of_latitudes.append(self._vertices[location].lat_and_long[0])
            list_of_longitudes.append(self._vertices[location].lat_and_long[1])

        return (list_of_latitudes, list_of_longitudes)

    def get_vertex(self, item: Any) -> _Vertex:
        """
        Returns the vertex corresponding to the given item
        """
        if item in self._vertices:
            v1 = self._vertices[item]
            return v1

        else:
            raise ValueError


def load_graph(chicago_traffic_file: str) -> Graph:
    """Return a graph corresponding to the given dataset.
    We return a graph connecting 'from' and 'to' streets in each row
    row[6] refers to the starting point (street) and row[7] refers to the ending point (street).
    row[11] refers to the day of the week and row[12] refers to the month and
    row[10] refers to the time.
    row[13] and row[14] refer to the starting latitude and longitude coordinates respectively.
    row[15] and row[16] refer to the latitude and longitude coordinates of the end point.
    For now, we are filtering rows and only reading ones for Thursday 5PM in March.
    row[3] refers to the speed and row [8] refers to the length of the route. We compute the
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
                               row[8])  # represents a route from starting to the ending point

    return graph


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'disable': ['E1136'],
    #     'extra-imports': ['csv', 'networkx'],
    #     'allowed-io': ['load_graph', 'print_all_connected'],
    #     'max-nested-blocks': 4
    # })
