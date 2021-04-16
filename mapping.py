"""
CSC111 Project: mapping.py

Module Description
==================
The following module utilizes the gmplot module to scatter the various points in our shortest paths
and then draw lines showing which point is connected to which point, or how we can travel from one
point to the next.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Aryaman Modi, Craig Katsube, Garv Sood, Kaartik Issar
"""

import webbrowser
import gmplot
from graph import Graph
# Graph = __import__("Graph & Node").Graph


def mapping_on_maps_multiple(graph: Graph, path: list) -> None:
    """
    Mapping function for only start and end points. This is so that we can have two separate
    html files for the two different calculations, calculating the shortest path between 2 points
    and calculating the shortest path between 2 points which goes through multiple other points.
    """
    start = path[0]
    end = path[-1]
    q = [start, end]  # So that we can have markers for the start and end points.
    r, t = graph.get_all_lat_long(q)  # To receive the latitude and longitude for the start and
    # end location .

    x, y = graph.get_all_lat_long(path)  # To receive the latitude and longitude for all the
    # different points in our path.
    z = x[1:-1]
    w = y[1:-1]

    gmap = gmplot.GoogleMapPlotter(41.8781, -87.6298, 13)  # Plots the map frm the center of
    # chicago.
    gmap.marker(r[0], t[0], color='black', title=path[0])  # Adds markers for start and end
    gmap.marker(r[1], t[1], color='black', title=path[-1])  # locations.

    # Scatter the different points in our path on the google map.
    gmap.scatter(z, w, color='blue', size=80, marker=True, title=path[1:-1])

    # Draw lines connecting the different co-ordinates or points in our google map.
    gmap.plot(x, y, '#6495ED', edge_width=2.0)

    gmap.draw('map1.html')
    webbrowser.open('map1.html')


def mapping_on_maps_singular(graph: Graph, path: list) -> None:
    """
    Mapping function for only start and end points. This is so that we can have two separate
    html files for the two different calculations, calculating the shortest path between 2 points
    and calculating the shortest path between 2 points which goes through multiple other points.
    """
    s = path[0]
    h = path[-1]
    q = [s, h]  # So that we can have markers for the start and end points by
    r, t = graph.get_all_lat_long(q)  # receiving the latitude and longitude for the start and
    # end location .

    x, y = graph.get_all_lat_long(path)  # To receive the latitude and longitude for all the
    # different points in our path.
    z = x[1:-1]
    w = y[1:-1]

    gmap1 = gmplot.GoogleMapPlotter(41.8781, -87.6298, 13)  # Plots the map frm the center of
    # chicago.

    gmap1.marker(r[0], t[0], color='black', title=path[0])  # Adds markers for start and end
    gmap1.marker(r[1], t[1], color='black', title=path[-1])  # locations.

    # Scatter the different points in our path on the google map.
    gmap1.scatter(z, w, color='blue',
                  size=80, marker=True, title=path[1:-1])

    # Draw lines connecting the different co-ordinates or points in our google map.
    gmap1.plot(x, y,
               '#6495ED', edge_width=2.0)

    gmap1.draw('map2.html')
    webbrowser.open('map2.html')


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['gmplot', 'webbrowser', 'graph'],
        'allowed-io': [],
        'max-nested-blocks': 5

    })
