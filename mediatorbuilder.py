"""Module for Builders for WidgetMediators"""

from tkinter import Widget
from typing import Any, Callable

from menumediator import WidgetMediator, NullMediator, MenuMediator, \
    OptionMenuComponent, OptionListComponent


class MediatorBuilder:
    """Interface for building WidgetMediators"""

    def get_mediator(self, parent: Widget) -> WidgetMediator:
        """Return the build Mediator"""
        raise NotImplementedError


def _create_column_lists(matrix: list[tuple]) -> list[list]:
    """Return a list of sets such that each set is the set of all items in a column of the matrix
    """

    if len(matrix) == 0:
        return []
    else:
        columns = len(matrix[0])
        column_lists = [[] for _ in range(columns)]
        for row in matrix:
            for col, item in enumerate(row):
                column_lists[col].append(item)

        return column_lists


class NullMediatorBuilder(MediatorBuilder):
    """Null MediatorBuilder representing behavior when no MediatorBuilder is specified
    """

    def get_mediator(self, parent: Widget) -> WidgetMediator:
        """Return a NullMediator because it has no behavior"""
        return NullMediator()


class MenuMediatorBuilder(MediatorBuilder):
    """Builder class for setting up the MenuMediator and its components

    Primarily used to postpone the creation of the Tkinter Widgets in the Mediator system
    due to the necessity of the parent Widget component when creating the child Widgets.
    """

    _options: dict[Any, list]
    _data: list[tuple]

    _inits: list[Callable[[Widget, MenuMediator], None]] = []

    def __init__(self, column_titles: tuple, data: list[tuple]):
        """
        Preconditions:
            - all(len(option_titles) == len(row) for row in options)
        """
        self._options = _map_title_to_column(column_titles, data)

    def get_mediator(self, parent: Widget) -> MenuMediator:
        """Return a MenuMediator using the settings saved in the builder"""

        mm = MenuMediator()
        for init_and_add in self._inits:
            init_and_add(parent, mm)

        return mm

    def create_option_menu(self, component_name: str, data_titles: tuple) -> None:
        """
        Preconditions:
            - data_title in self._options
        """
        data = [self._options[data_title] for data_title in data_titles]
        self._inits.append(_offset_omc_init(component_name, data))

    def create_option_list(self, component_name: str, data_titles: tuple) -> None:
        """
        Preconditions:
            - data_title in self._options
        """
        data = [self._options[data_title] for data_title in data_titles]
        self._inits.append(_offset_olc_init(component_name, data))


def _map_title_to_column(titles: tuple, matrix: list[tuple]) -> dict[Any, list]:
    """Return a dict mapping title to the respective column in the matrix

    Preconditions:
        - all(len(titles) == len(row) for row in matrix)
    """

    column_data = _create_column_lists(matrix)
    return {title: column
            for title, column in zip(titles, column_data)}


def _offset_omc_init(component_name: str, data: list) -> \
        Callable[[Widget, MenuMediator], None]:
    """Return a function that takes in the parent widget to use to create the OptionMenuComponents

    This method saves some of the settings for creating an OptionMenuComponent to offset the actual
    creating until a parent frame is made
    """

    def create_omc(parent: Widget, mm: MenuMediator) -> None:
        """Creates an OptionMenuComponent using the variables taken from the local context"""
        omc = OptionMenuComponent(parent, mm, component_name, data)
        mm.add_component(component_name, omc)

    return create_omc


def _offset_olc_init(component_name: str, data: list) -> \
        Callable[[Widget, MenuMediator], None]:
    """Return a function that takes in the parent widget to use to create the OptionMenuComponents

    This method saves some of the settings for creating an OptionMenuComponent to offset the actual
    creating until a parent frame is made
    """

    def create_olc(parent: Widget, mm: MenuMediator) -> None:
        """Creates an OptionMenuComponent using the variables taken from the local context"""
        olc = OptionListComponent(parent, mm, component_name, data)
        mm.add_component(component_name, olc)

    return create_olc
