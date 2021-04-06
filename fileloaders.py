"""Module containing functions that load in files"""

import csv

from graph import Graph


def traffic_heuristic(item1, item2) -> float:
    """
    Returns the weight between two locations using the traffic heuristic.
    To be coded later.
    """


###########################################################################
# Table Column Name Constants for the Chicago Traffic Data from Data World
###########################################################################

C_SPEED = 2
C_START = 5
C_END = 6
C_LENGTH = 7
C_TIME = 12
C_DAY = 13
C_MONTH = 14

PM5 = "17"
THURSDAY = "4"
MARCH = "3"


#########################

def load_graph(chicago_traffic_file: str) -> Graph:
    """Return a graph corresponding to the given chicago dataset from data world.
    We return a graph connecting 'from' and 'to' streets in each row
    For now, I am filtering rows and only reading ones for Thursday 5PM in March.

    We compute the weighted portion of the vertex by calculating length/speed to obtain the
    time taken between the starting and ending points.
    """
    graph = Graph()
    with open(chicago_traffic_file) as csv_file2:

        traffic_data_table = csv.reader(csv_file2)
        next(traffic_data_table)  # to skip the first row

        for row in traffic_data_table:

            is_5pm = row[C_TIME] == PM5
            is_thursday = row[C_DAY] == THURSDAY
            is_march = row[C_MONTH] == MARCH

            if is_5pm and is_thursday and is_march:

                start_point = row[C_START]
                if not graph.check_in(end_point):
                    graph.add_vertex(start_point)

                end_point = row[C_END]
                if not graph.check_in(end_point):
                    graph.add_vertex(end_point)

                speed = float(row[C_SPEED])
                length = float(row[C_LENGTH])
                time = speed / length

                graph.add_edge(start_point, end_point, time)

    return graph
