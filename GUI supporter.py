"""
Function(s) that help build the options for the gui interface.
"""
import csv
Graph = __import__("Graph & Node").Graph

# Kaartik's gui supporter
# def gui_supporter1(chicago_traffic_file: str, start, end, day) -> list:
#     """
#     Takes input about the start, end points and the day from user and returns the possible hours to
#     choose from.
#     """
#     possible_hours = []
#     with open(chicago_traffic_file) as csv_file2:
#         traffic_data = csv.reader(csv_file2)
#         next(traffic_data)  # to skip the first row
#         for row in traffic_data:
#             if row[6] == start and row[7] == end and row[11] == day:
#                 if row[10] not in possible_hours:
#                     possible_hours.append(row[10])
#     return possible_hours


def load_graph_from_load_data(info: list[tuple]):
    """
    abcd
    """
    g = Graph()
    for row in info:

        if not g.check_in(row[1]):
            g.add_vertex(row[1], row[7], row[8])
        if not g.check_in(row[2]):
            g.add_vertex(row[2], row[9], row[10])
        g.add_edge(row[1], row[2], row[0], row[3])

    return g
