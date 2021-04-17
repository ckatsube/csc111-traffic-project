"""CSC111 Project: datatransformation.py
Module Description
==================
Program that transforms the original dataset according to our project needs.
    - selects specific columns.
    - creates tidy data by removing undesired and unavailable speed values
    - creates a new csv file with the desired data
Contains another computation that finds out the minimum and maximum latitude and longitude values.
Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Kaartik Issar, Aryaman Modi,
Craig Katsube and Garv Sood.
"""
import csv
import math
import pandas as pd

DF = pd.read_csv('trafficdata.csv')
FD = pd.DataFrame(DF, columns=['time', 'segment_id', 'speed', 'street', 'direction',
                               'from_street', 'to_street', 'length', 'bus_count',
                               'hour', 'day_of_week', 'month', 'start_latitude', 'start_longitude',
                               'end_latitude', 'end_longitude'])
FD_ONE = FD[FD['speed'] != -1]
FD_TWO = FD_ONE[FD_ONE['speed'] != 0]
# saving the dataframe as csv
FD_TWO.to_csv('transformed_final.csv')

####################################################################################################

# finding out the dimensions of the map of chicago we are going to use.in our visualisation

MAXLONG = -math.inf
MINLONG = math.inf
MAXLAT = -math.inf
MINLAT = math.inf
with open('transformed_final.csv') as CSV_FILE2:
    TRAFFIC_DATA = csv.reader(CSV_FILE2)
    next(TRAFFIC_DATA)  # to skip the first row
    for ROW in TRAFFIC_DATA:
        if float(ROW[15]) > MAXLONG:
            MAXLONG = float(ROW[15])
        if float(ROW[15]) < MINLONG:
            MINLONG = float(ROW[15])
        if float(ROW[14]) > MAXLAT:
            MAXLAT = float(ROW[14])
        if float(ROW[14]) < MINLAT:
            MINLAT = float(ROW[14])

with open('transformed_final.csv') as CSV_FILE2:
    TRAFFIC_DATA = csv.reader(CSV_FILE2)
    next(TRAFFIC_DATA)  # to skip the first row
    for ROW in TRAFFIC_DATA:
        if float(ROW[15]) > MAXLONG:
            MAXLONG = float(ROW[17])
        if float(ROW[15]) < MINLONG:
            MINLONG = float(ROW[17])
        if float(ROW[14]) > MAXLAT:
            MAXLAT = float(ROW[16])
        if float(ROW[14]) < MINLAT:
            MINLAT = float(ROW[16])
END_POINTS = [MAXLONG, MINLONG, MAXLAT, MINLAT]

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9971'],
        'extra-imports': ['heapq', 'graph', 'abc', 'pandas', 'math', 'csv'],
        'allowed-io': [],
        'max-nested-blocks': 5

    })
