"""Entry point for the program"""
from typing import Any, Callable

from usergui import InputFrameBuilder
from mediatorbuilder import MenuMediatorBuilder
from shortest_path_calculator import gets_original_gives_full_path
from visualization import visualise

create_graph_from_matrix = __import__("GUI supporter").load_graph_from_load_data
loader = __import__("GUI supporter").load_titled_data

CHICAGO_TRAFFIC_FILE = "transformed_final.csv"


def create_and_run_input_frame() -> None:
    """Creates an input frame using the InputFrameBuilder and Chicago traffic dataset
    and runs the frame"""

    header, data = loader(CHICAGO_TRAFFIC_FILE)
    mmb = MenuMediatorBuilder(header, data)
    mmb.create_option_menu("day menu", ("day",))
    mmb.create_option_menu("month menu", ("month",))
    mmb.create_option_menu("time menu", ("time",))
    mmb.create_option_menu("start street", ("start point", "end point"))
    mmb.create_option_menu("end street", ("start point", "end point"))
    mmb.create_option_list("intermediate streets", ("start point", "end point"))

    ifb = InputFrameBuilder()
    ifb.set_mediator_builder(mmb)
    ifb.set_button_command(inject_data(data))
    ifb.get_frame().mainloop()


def inject_data(data: list[tuple]) -> Callable[[dict[str, Any]], None]:
    """Wrapper for inserting data into the output function"""

    def process_input(options: dict[str, Any]) -> None:
        """Visualizes path"""

        filtered_data = _filter_by(data, options)

        g = create_graph_from_matrix(filtered_data)

        start_point = filtered_data[0][7:9]
        end_point = filtered_data[0][9:11]

        path = gets_original_gives_full_path(g, start_point, end_point, [])

        visualise(path, g)

    return process_input


def _filter_by(data: list[tuple], options: dict[str, Any]) -> list[tuple]:
    """Return data filtered using the data provided in options

    Postconditions:
        - every row in the returned list contains every required option
    """

    required = ("day menu", "month menu", "time menu")
    indices = (4, 5, 6)

    filtered_matrix = []
    for row in data:
        if all(row[index] == options[title] for title, index in zip(required, indices)):
            filtered_matrix.append(row)

    return filtered_matrix


if __name__ == "__main__":
    create_and_run_input_frame()
