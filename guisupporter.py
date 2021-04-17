"""
Function(s) that help build the options for the gui interface.
"""
import csv
from graph import Graph


###################################################################
# Supported row format and its constants
###################################################################

DATA_HEADER = (
    "speed",
    "start point", "end point",
    "length",
    "time", "day", "month",
    "start point latitude", "start point longitude",
    "end point latitude", "end point longitude"
)

I_SPEED = 0
I_START = 1
I_END = 2
I_LENGTH = 3
I_TIME = 4
I_DAY = 5
I_MONTH = 6
I_START_LAT = 7
I_START_LON = 8
I_END_LAT = 9
I_END_LON = 10


#############################################


def load_titled_data(traffic_file: str) -> tuple[tuple, list[tuple]]:
    """Return a matrix mirroring data contained in the csv and its corresponding header"""

    data = load_data(traffic_file)
    return DATA_HEADER, data


def load_data(traffic_file: str) -> list[tuple]:
    """Return a matrix mirroring the data contained in the csv with some additional filtering
    """
    data = []
    with open(traffic_file) as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        for row in csv_reader:
            select = (row[3],) + tuple(row[6:9]) + tuple(row[10:17])
            data.append(select)

    return data


def filter_data_from_selection(data: list[tuple], selections: dict[str, list]) -> list[tuple]:
    """Filter data by complete match for month, day, time and by connectedness for the
    start and end streets

    Preconditions:
        - all(title in DATA_HEADER for title in selection)
        - data must be in the same format as the matrices formed in this module
    """

    g = Graph()
    time_headers = {"time", "day", "month"}
    filtered = []
    for row in data:
        if all(header not in selections or _selection_is_empty(selections[header])
               or _get(header, row) in selections[header] for header in time_headers):
            _add_row_to_graph(row, g)
            filtered.append(row)

    if _selections_are_empty(selections, ["start point", "end point"]):
        return filtered
    else:
        place_headers = {"start point", "end point"}
        try:
            connected_vertices = g.get_all_connected_components(
                set.union(*(set(selections[header]) for header in place_headers)).difference({''})
            )
        except ValueError:
            connected_vertices = {}

        return [row for row in filtered if any(place in connected_vertices for place in
                                               [_get(header, row) for header in place_headers])]


def _selections_are_empty(selections: dict[str, list], titles: list[str]) -> bool:
    return all(_selection_is_empty(selections[title]) for title in titles)


def _selection_is_empty(selection: list[str]) -> bool:
    return all(value == "" for value in selection)


def _add_row_to_graph(row: tuple, g: Graph) -> None:
    if not g.check_in(row[I_START]):
        g.add_vertex(row[I_START], row[I_START_LAT], row[I_START_LON])
    if not g.check_in(row[I_END]):
        g.add_vertex(row[I_END], row[I_END_LAT], row[I_END_LON])
    g.add_edge(row[I_START], row[I_END], row[I_SPEED], row[I_LENGTH])


def _get(header: str, row: tuple) -> str:
    """
    Preconditions:
        - header in DATA_HEADERS
        - row in the module supported format
    """
    col = DATA_HEADER.index(header)
    return row[col]


def load_graph_from_load_data(info: list[tuple]) -> Graph:
    """
    Loads a graph from the provided matrix of data

    Preconditions:
        - row is in the supported format for row in info
    """
    g = Graph()
    for row in info:
        _add_row_to_graph(row, g)

    return g
