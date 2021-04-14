"""
Program that transfers the original dataset according to our project needs.
    - selects specific columns.
    - creates tidy data by removing undesired and unavailable speed values
    - creates a new csv file with the desired data
"""

import pandas as pd
import csv
import math
df = pd.read_csv('trafficdata.csv')
fd = pd.DataFrame(df, columns=['time', 'segment_id', 'speed', 'street', 'direction',
                               'from_street', 'to_street', 'length', 'bus_count',
                               'hour', 'day_of_week', 'month', 'start_latitude', 'start_longitude',
                               'end_latitude', 'end_longitude'])
fd_one = fd[fd['speed'] != -1]
fd_two = fd_one[fd_one['speed'] != 0]
# saving the dataframe as csv
fd_two.to_csv('transformed_final.csv')

####################################################################################################

#finding out the dimensions of the map of chicago we are going to use.in our visualisation

max_long = -(math.inf)
min_long = math.inf
max_lat = -(math.inf)
min_lat = math.inf
with open('transformed_final.csv') as csv_file2:
    traffic_data = csv.reader(csv_file2)
    next(traffic_data)  # to skip the first row
    for row in traffic_data:
        if float(row[15]) > max_long:
            max_long = float(row[15])
        if float(row[15]) < min_long:
            min_long = float(row[15])
        if float(row[14]) > max_lat:
            max_lat = float(row[14])
        if float(row[14]) < min_lat:
            min_lat = float(row[14])

with open('transformed_final.csv') as csv_file2:
    traffic_data = csv.reader(csv_file2)
    next(traffic_data)  # to skip the first row
    for row in traffic_data:
        if float(row[15]) > max_long:
            max_long = float(row[17])
        if float(row[15]) < min_long:
            min_long = float(row[17])
        if float(row[14]) > max_lat:
            max_lat = float(row[16])
        if float(row[14]) < min_lat:
            min_lat = float(row[16])
end_points = [max_long, min_long, max_lat, min_lat]





