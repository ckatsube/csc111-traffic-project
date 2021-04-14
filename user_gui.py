"""I/O devices for interacting with the shortest path program
"""

from tkinter import OptionMenu, Frame, Tk, Label, Button, Variable, Menu, Widget
from typing import Any, Callable


def get_input_handler_frame() -> Tk:
    """Return the Tkinter frame that contains the widgets for inputting information"""
    ifb = InputFrameBuilder()
    ifb.set_options(*_get_options())
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

    _option_names: tuple = ("title 1", "title 2")
    _options: list[tuple] = [("option 1", "option a"), ("option 2", "option b")]

    _geometry: str = "300x150"
    _title: str = "Settings Input"

    _command = print

    def set_options(self, option_names: tuple, options: list[tuple]):
        """Sets the options for the frame

        Preconditions:
            - all(len(row) == len(option_names) for row in options)
        """

        self._option_names = option_names
        self._options = options

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

        Preconditions:
            - len(command.__annotations__) == len(self._options) or subsequence parameters are
                the arbitrary * or **
        """
        self._command = command

    def get_frame(self) -> Tk:
        """Get the frame using the set settings"""

        world = Tk()
        world.title(self._title)
        world.geometry(self._geometry)

        f = Frame(world)
        f.pack()

        of = OptionsFacade(f, self._options)
        for row, zipped in enumerate(zip(self._option_names, of.get_menus())):
            name, menu = zipped

            Label(f, text=name).grid(row=row, column=0, sticky="nsew")
            menu.grid(row=row, column=1, sticky="nsew")

        def _command_wrapper() -> None:
            self._command(*of.get_selection())

        Button(f, text="Reset Selection", command=of.reset_selection). \
            grid(row=len(self._options) + 1, column=0, sticky="sew")

        Button(f, text="Export Selection", command=_command_wrapper). \
            grid(row=len(self._options) + 1, column=1, sticky="sew")

        return world


class OptionsFacade:
    """Class that handles higher level interactions with a
    list of OptionMenus and its set of options
    """

    _options: list[tuple]

    _vars: list[Variable]
    _menus: list[OptionMenu]

    def __init__(self, parent: Widget, options: list[tuple]):
        """
        Preconditions:
            - len(options) == 0 or all(len({option) == len(options[0]) for option in options})
        """

        columns = 0 if len(options) == 0 else len(options[0])
        self._options = options
        self._vars = [Variable() for _ in range(columns)]

        option_sets = _create_column_sets(self._options)
        self._menus = [OptionMenu(parent, self._vars[i], "", *option_sets[i],
                                  command=lambda *_: self._update_options())
                       for i in range(columns)]

    def get_selection(self) -> tuple:
        """Return the selected options"""
        return tuple(var.get() for var in self._vars)

    def reset_selection(self) -> None:
        """Removes all currently selected options"""
        for var in self._vars:
            var.set("")
        self._update_options()

    def get_menus(self) -> list[OptionMenu]:
        """Return the option menus being handled by this facade"""
        return self._menus.copy()

    def configure_menu(self, config: str, value: str):
        """Sets the configuration of the specific config to value for all menus
        """
        for menu in self._menus:
            menu[config] = value

    def _update_options(self) -> None:
        """Updates all the options of the menus to display only valid selections"""
        self.configure_menu("state", "disabled")
        self._reset_all_menus()
        self.configure_menu("state", "normal")

    def _reset_all_menus(self) -> None:
        """Resets all OptionMenus to only display items that produce a valid selection"""

        filtered_option_sets = _filter_by_selection(self.get_selection(), self._options)
        for category, option_menu in enumerate(self._menus):
            menu = option_menu["menu"]
            var = self._vars[category]
            options = [] if len(filtered_option_sets) == 0 else filtered_option_sets[category]

            self._reset_option_menu(menu, var, options)

    def _reset_option_menu(self, menu: Menu, var: Variable, options: set):
        """Override the options of the menu with the specified set of options"""
        start, end = 0, "end"
        menu.delete(start, end)

        menu.add_command(label="", command=self._click_command(var, ""))
        for option in options:
            menu.add_command(label=option, command=self._click_command(var, option))

    def _click_command(self, variable: Variable, opt: Any) -> Callable:
        """Return the command to be called when clicking an option item"""
        def wrapper() -> None:
            """Function called when clicking an option item"""
            variable.set(opt)
            self._update_options()

        return wrapper


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
