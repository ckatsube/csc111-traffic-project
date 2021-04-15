"""
Mapping using gmplot, pip install gmplot before doing this.
"""
import gmplot
import webbrowser
Graph = __import__("Graph & Node").Graph


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

    gmap = gmplot.GoogleMapPlotter(41.8781, -87.6298, 13)  # Plots the map frm the center of
    # chicago.
    gmap.marker(r[0], t[0], color='black', title=path[0])  # Adds markers for start and end
    gmap.marker(r[1], t[1], color='black', title=path[-1])  # locations.

    # Scatter the different points in our path on the google map.
    gmap.scatter(x, y, color='blue', size=80, marker=False)

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

    gmap1 = gmplot.GoogleMapPlotter(41.8781, -87.6298, 13)  # Plots the map frm the center of
    # chicago.

    gmap1.marker(r[0], t[0], color='black', title=path[0])  # Adds markers for start and end
    gmap1.marker(r[1], t[1], color='black', title=path[-1])  # locations.

    # Scatter the different points in our path on the google map.
    gmap1.scatter(x, y, color='blue',
                  size=80, marker=False)

    # Draw lines connecting the different co-ordinates or points in our google map.
    gmap1.plot(x, y,
               '#6495ED', edge_width=2.0)

    gmap1.draw('map2.html')
    webbrowser.open('map2.html')
