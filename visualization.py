"""
CSC111 Project: visualisation.py

Module Description
==================

One half of the visualisation part of project. Plotting the latitudes and longitudes of the path on
the map of Chicago city.
Includes a helper function that converts list[latitudes] and list[longitudes] to a single list.
Copyright and Usage Information

===============================

This file is Copyright (c) 2021 Kaartik Issar, Aryaman Modi, Craig Katsube and Garv Sood.
"""


import matplotlib.pyplot as plt
from graph import Graph

# Graph = __import__("Graph & Node").Graph
# load_graph = __import__("Graph & Node").load_graph


def convert_to_tuple_points(lst1: list, lst2: list) -> list:
    """
    Combines a list of latitudes only and a list of longitudes only into a single list of latitudes
    and longitudes. The returned list should be a list of tuples, where each tuple is latitude and
    longitude of a location.
    >>> convert_to_tuple_points([1,2,3], [4,5,6])
    [(1, 4), (2, 5), (3, 6)]
    """
    new_lst = []
    assert len(lst1) == len(lst2)
    for i in range(0, len(lst1)):
        new_lst.append((lst1[i], lst2[i]))
    return new_lst


def visualise(lst: list, g: Graph) -> None:
    """
    Give a visual representation of the given path on the map of Chicago City.
    """
    map_img = plt.imread('map1.png')

    # endpoints obtained from computation in datatransformation.py
    box = (41.65900629, 42.0128288601, -87.535052, -87.8367650119)
    _, ax = plt.subplots(figsize=(8, 7))

    lst1, lst2 = g.get_all_lat_long(lst)
    lst_lat_long = convert_to_tuple_points(lst1, lst2)

    for point in lst_lat_long:
        ax.scatter(float(point[0]), float(point[1]), zorder=10, alpha=0.8, c='black', s=30)
    ax.set_title('Plotting a path on Chicago map')
    ax.set_xlim(41.65900629, 42.0128288601)
    ax.set_ylim(-87.535052, -87.8367650119)
    for i, txt in enumerate(lst):
        ax.annotate(txt + ' ,' + str(i), (lst_lat_long[i][0], lst_lat_long[i][1]))
    ax.imshow(map_img, zorder=0, extent=box, aspect='equal')


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['matplotlib.pyplot', 'graph'],
        'allowed-io': [],
        'max-nested-blocks': 5

    })
