"""I/O devices for interacting with the shortest path program
"""

from tkinter import Button, Frame, Label, Tk
from typing import Callable

from mediatorbuilder import MenuMediatorBuilder, NullMediatorBuilder, MediatorBuilder


def get_input_handler_frame() -> Tk:
    """Return the Tkinter frame that contains the widgets for inputting information"""

    option_names, options = _get_options()

    mmb = MenuMediatorBuilder(option_names, options)
    for name in option_names:
        mmb.create_option_menu(name, (name,))
    mmb.create_option_menu("random1", ("high",))
    mmb.create_option_list("random2", ("high",))

    ifb = InputFrameBuilder()
    ifb.set_mediator_builder(mmb)
    ifb.set_geometry("300x200")
    return ifb.get_frame()


def run_input_frame() -> None:
    """Run the default the input frame using the default settings from get_input_handler_frame
    """

    get_input_handler_frame().mainloop()


def _get_options() -> tuple[tuple, list[tuple]]:
    option_names = (
        "letter",
        "low",
        "high"
    )
    options = [
        ("a", 2, 1000),
        ("b", 1, 2000),
        ("d", 10, 300)
    ]
    return option_names, options


class InputFrameBuilder:
    """Builder class for inputting the settings for the input frame
    """

    _geometry: str = "300x150"
    _title: str = "Settings Input"

    _mb: MediatorBuilder = NullMediatorBuilder()

    _command = print

    def set_geometry(self, geometry: str):
        """Sets the size of the frame

        Preconditions:
            - geometry must be a valid input for Tk().geometry()
        """
        self._geometry = geometry

    def set_title(self, title: str):
        """Sets the title of the frame"""
        self._title = title

    def set_button_command(self, command: Callable):
        """Sets the command called when clicking the button

        The dict containing the Widget name to its selection is passed into this command
        """
        self._command = command

    def set_mediator_builder(self, mb: MediatorBuilder):
        """Sets the MediatorBuilder to use when creating the input frame"""
        self._mb = mb

    def get_frame(self) -> Tk:
        """Get the frame using the set settings"""

        world = Tk()
        world.title(self._title)
        world.resizable(height=False, width=True)

        f = Frame(world)
        f.pack()

        mediator = self._mb.get_mediator(parent=f)

        named_widgets = mediator.get_components()
        for row, menu_name in enumerate(named_widgets):
            menu = named_widgets[menu_name]

            Label(f, text=menu_name).grid(row=row, column=0, sticky="nsew")
            menu.grid(row=row, column=1, sticky="nsew")

        def _command_wrapper() -> None:
            self._command(mediator.get_selection())

        Button(f, text="Reset Selection", command=mediator.reset_selection). \
            grid(row=len(named_widgets) + 1, column=0, sticky="sew")

        Button(f, text="Export Selection", command=_command_wrapper). \
            grid(row=len(named_widgets) + 1, column=1, sticky="sew")

        return world


def _filter_by_selection(selection: tuple, matrix: list[tuple]) -> list[set]:
    """Return the column sets filtered by the selection tuple"""

    columns = len(selection)
    filtered_options = [row for row in matrix if
                        all(row[i] == selection[i] or selection[i] == ""
                            for i in range(columns))]
    option_sets = _create_column_sets(filtered_options)

    return option_sets


def _create_column_sets(matrix: list[tuple]) -> list[set]:
    """Return a list of sets such that each set is the set of all items in a column of the matrix
    """

    if len(matrix) == 0:
        return []
    else:
        columns = len(matrix[0])
        sets = [set() for _ in range(columns)]
        for row in matrix:
            for col, item in enumerate(row):
                sets[col].add(item)

        return sets
