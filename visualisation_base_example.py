"""
Visualisation part of project. We plot the latitudes and longitudes of the path on the map of Chicago city.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import math

# currently I have defined this list, but this list should be defined using the function call from get
# path functions and our computational function. Someone please can make the function call here correctly
#lst = [(41.75, -87.6), (41.85, -87.65), (41.9, -87.70), (42.00, -87.8)]

def visualise(lst: list):
    """
    Give a visual representation of the path on the map of Chicago City.
    """
    ruh_m = plt.imread('map1.png')
    BBox = (41.65900629, 42.0128288601, -87.535052, -87.8367650119)  # endpoints obtained from
                                                                     # computation in data transformation
    fig, ax = plt.subplots(figsize=(8, 7))

    # use a for loop and plot the longitudes and latitudes of the path.

    for point in lst:
         ax.scatter(float(point[0]), float(point[1]), zorder=10, alpha=0.8, c='black', s=30)

    ax.set_title('Plotting a path on Chicago map')
    ax.set_xlim(41.65900629, 42.0128288601)
    ax.set_ylim(-87.535052, -87.8367650119)
    ax.imshow(ruh_m, zorder=0, extent=BBox, aspect='equal')
