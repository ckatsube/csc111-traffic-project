"""Entry point for the program"""
from typing import Any, Callable

from usergui import InputFrameBuilder
from mediatorbuilder import MenuMediatorBuilder
from shortest_path_calculator import gets_original_gives_full_path
from pathcalculator import dijkstra
from visualization import visualise
from mapping import mapping_on_maps_multiple, mapping_on_maps_singular

from graph import Graph

from guisupporter import load_graph_from_load_data
from guisupporter import load_titled_data

CHICAGO_TRAFFIC_FILE = "transformed_final.csv"


def create_and_run_input_frame() -> None:
    """Creates an input frame using the InputFrameBuilder and Chicago traffic dataset
    and runs the frame"""

    header, data = load_titled_data(CHICAGO_TRAFFIC_FILE)
    mmb = MenuMediatorBuilder(header, data)
    mmb.create_option_menu("day menu", ("day",))
    mmb.create_option_menu("month menu", ("month",))
    mmb.create_option_menu("time menu", ("time",))
    mmb.create_option_menu("start street*", ("start point", "end point"))
    mmb.create_option_menu("end street*", ("start point", "end point"))
    mmb.create_option_list("intermediate streets", ("start point", "end point"))

    ifb = InputFrameBuilder()
    ifb.set_mediator_builder(mmb)
    ifb.set_button_command(inject_data(data))
    ifb.get_frame().mainloop()


def inject_data(data: list[tuple]) -> Callable[[dict[str, Any]], None]:
    """Wrapper for inserting data into the output function"""

    def process_input(options: dict[str, Any]) -> None:
        """Uses the options to generate the graph and visualize the graph and shortest path"""

        filtered_data = _filter_by(data, options)
        g = load_graph_from_load_data(filtered_data)
        _visualize_graph(g, options)

    return process_input


def _visualize_graph(g: Graph, options: dict[str, Any]) -> None:

    start = options["start street*"]
    end = options["end street*"]

    intermediate_points = filter(lambda x: x != "", options["intermediate streets"])

    if all(intermediate == "" for intermediate in intermediate_points):
        path = list(dijkstra(g, start, end))
        mapping_on_maps_singular(g, path)
    else:
        path = gets_original_gives_full_path(g, start, end, list(intermediate_points))
        mapping_on_maps_multiple(g, path)

    visualise(path, g)


def _filter_by(data: list[tuple], options: dict[str, Any]) -> list[tuple]:
    """Return data filtered using the data provided in options

    Postconditions:
        - every row in the returned list contains every required option
    """

    required = ("time menu", "day menu", "month menu")
    indices = (4, 5, 6)

    filtered_matrix = []
    for row in data:
        if all(options[title] == "" or row[index] == options[title]
               for title, index in zip(required, indices)):

            filtered_matrix.append(row)

    return filtered_matrix


if __name__ == "__main__":
    create_and_run_input_frame()
