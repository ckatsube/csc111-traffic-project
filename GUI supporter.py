"""
Function(s) that help build the options for the gui interface.
"""
import csv

def gui_supporter1(chicago_traffic_file: str, start, end, day) -> list:
    """
    Takes input about the start, end points and the day from user and returns the possible hours to choose from.
    """
    possible_hours = []
    with open(chicago_traffic_file) as csv_file2:
        traffic_data = csv.reader(csv_file2)
        next(traffic_data)  # to skip the first row
        for row in traffic_data:
            if row[6] == start and row[7] == end and row[11] == day:
                if row[10] not in possible_hours:
                    possible_hours.append(row[10])
    return possible_hours


