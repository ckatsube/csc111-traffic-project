"""Module for Builders for WidgetMediators"""

from tkinter import Widget
from typing import Callable

from menumediator import WidgetMediator, NullMediator, MenuMediator, \
    OptionMenuComponent, OptionListComponent


class MediatorBuilder:
    """Interface for building WidgetMediators"""

    def get_mediator(self, parent: Widget) -> WidgetMediator:
        """Return the built Mediator"""
        raise NotImplementedError


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
    # Private Attributes:
    #   - _titles: the titles of the columns of data
    #   - _data: data used to mediate between colleagues
    #   - _inits: promises to create the Widgets when a parent frame is given

    _titles: tuple
    _data: list[tuple]

    _inits: list[Callable[[Widget, MenuMediator], None]] = []

    def __init__(self, titles: tuple, data: list[tuple]) -> None:
        """
        Preconditions:
            - all(len(titles) == len(row) for row in data)
        """
        self._titles = titles
        self._data = data

    def get_mediator(self, parent: Widget) -> MenuMediator:
        """Return a MenuMediator using the settings saved in the builder"""

        mm = MenuMediator(self._titles, self._data)
        for init_and_add in self._inits:
            init_and_add(parent, mm)

        return mm

    def create_option_menu(self, component_name: str, data_titles: tuple) -> None:
        """
        Preconditions:
            - data_title in self._options
        """

        def create_omc(parent: Widget, mm: MenuMediator) -> None:
            """Creates an OptionMenuComponent using the variables taken from the local context"""
            omc = OptionMenuComponent(parent, mm)
            mm.add_component(omc, component_name, data_titles)

        self._inits.append(create_omc)

    def create_option_list(self, component_name: str, data_titles: tuple) -> None:
        """
        Preconditions:
            - data_title in self._options
        """

        def create_olc(parent: Widget, mm: MenuMediator) -> None:
            """Creates an OptionMenuComponent using the variables taken from the local context"""
            olc = OptionListComponent(parent, mm)
            mm.add_component(olc, component_name, data_titles)

        self._inits.append(create_olc)
