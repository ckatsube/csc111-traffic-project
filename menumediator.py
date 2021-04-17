"""Module containing the classes for utilizing the WidgetMediator

"""

from __future__ import annotations

from tkinter import Button, Frame, Menu, Variable, OptionMenu, Widget
from typing import Any, Callable
from collections import Iterable

from guisupporter import filter_data_from_selection


####################################################################
# Mediator Components
####################################################################


class MediatorComponent:
    """Interface for WidgetMediator components"""

    def get_selected(self) -> Any:
        """Return the current selection(s) of this component"""
        raise NotImplementedError

    def set_selection(self, data: list) -> None:
        """Sets the selection of this component to the specified data"""
        raise NotImplementedError

    def reset_selection(self) -> None:
        """Resets the selection of this components to its default state"""
        raise NotImplementedError

    def get_widget(self) -> Widget:
        """Return the Menu widget composed in this Component"""
        raise NotImplementedError

    def configure_menu(self, config: str, value: str) -> None:
        """Configure the settings of all composed widgets"""
        raise NotImplementedError


class OptionMenuComponent(MediatorComponent):
    """WidgetMediator component that contains an OptionMenu
    """
    # Private Attributes:
    #   - _var: the external mutatable variable for the menu widget
    #   - _om: the OptionMenu shown to the user that displays the selection
    #   - _mediator: the mediator to notify a selection has been made to update other colleages

    _var: Variable
    _om: OptionMenu

    _mediator: MenuMediator

    def __init__(self, parent: Widget, mediator: MenuMediator) -> None:
        self._var = Variable()
        self._mediator = mediator
        self._om = OptionMenu(parent, self._var, "")

    def reset_selection(self) -> None:
        """Sets the option menu variable to an empty string"""
        self._var.set("")

    def set_selection(self, data: list) -> None:
        """Sets the OptionMenu options to data"""
        menu = self._om["menu"]

        _delete_menu_options(menu)

        def click_command(variable: Variable, opt: Any) -> Callable:
            """Return the command to be called when clicking an option item"""

            def wrapper() -> None:
                """Function called when clicking an option item"""
                variable.set(opt)
                self._mediator.update_selection(())

            return wrapper

        data = sorted(set(data))

        menu.add_command(label="", command=click_command(self._var, ""))
        for option in data:
            menu.add_command(label=option, command=click_command(self._var, option))

    def get_widget(self) -> Widget:
        """Return a list containing this OptionMenu"""
        return self._om

    def configure_menu(self, config: str, value: str) -> None:
        """Configures the setting of the composed dOptionMenu"""
        self._om[config] = value

    def get_selected(self) -> Any:
        """Return the current variable's value"""
        return self._var.get()


def _delete_menu_options(menu: Menu) -> None:
    """Deletes all items/commands from the Menu"""
    start, end = 0, "end"
    menu.delete(start, end)


class OptionListComponent(MediatorComponent, Frame):
    """WidgetMediator component allowing for adding and deleting an arbitrary number of
    OptionMenus that rely on the same dataset
    """
    # Private Attributes:
    #   _menu_components: stack of OptionMenuComponents to add and remove using buttons
    #   _menu_frame: the frame to add/remove widgets to/from
    #   - _mediator: the mediator to notify a selection has been made to update other colleages

    _menu_components: list[OptionMenuComponent] = []
    _menu_frame: Frame

    _mediator: MenuMediator

    def __init__(self, parent: Widget, mediator: MenuMediator):
        super().__init__(parent)
        self._parent = parent
        self._mediator = mediator

        self._menu_frame = Frame(self)
        self._setup_frame()

    def _setup_frame(self) -> None:
        menu_frame = self._menu_frame
        menu_frame.grid(row=0, column=0, sticky="nsew")
        button_frame = Frame(self)
        button_frame.grid(row=0, column=1, sticky="nsew")

        self.add_option_menu()

        Button(button_frame, text="Add", command=self.add_option_menu).\
            pack(fill="x", anchor="n")
        Button(button_frame, text="Remove", command=self.remove_option_menu).\
            pack(fill="x", anchor="n")

    def add_option_menu(self) -> None:
        """Adds an OptionMenu to this component"""

        omc = OptionMenuComponent(self._menu_frame, self._mediator)
        self._menu_components.append(omc)

        om = omc.get_widget()
        om.pack(anchor="n")

        self._mediator.update_selection(())

    def remove_option_menu(self) -> None:
        """Removes an OptionMenu from this component"""
        if self._menu_components:
            omc = self._menu_components.pop()

            om = omc.get_widget()
            om.pack_forget()

    def reset_selection(self) -> None:
        """Sets the all option menu variables to an empty string and removes additional OptionMenus
        """
        for om in self._menu_components:
            om.reset_selection()
        while len(self._menu_components) > 1:
            self.remove_option_menu()

    def set_selection(self, data: list) -> None:
        """Restricts the selection of all children OptionMenus to the same data"""
        for om in self._menu_components:
            om.set_selection(data)

    def get_widget(self) -> Widget:
        """Return self which is the Frame composed of all the internal input menus"""
        return self

    def configure_menu(self, config: str, value: str) -> None:
        """Configures the setting of all the composed OptionMenus"""
        for om in self._menu_components:
            om.configure_menu(config, value)

    def get_selected(self) -> Any:
        """Return a tuple of all children OptionMenu values"""
        return tuple(om.get_selected() for om in self._menu_components)


##############################################################################
# Mediators
##############################################################################


class WidgetMediator:
    """Mediator for handling interaction between multiple Widgets"""

    def get_selection(self) -> dict[str, Any]:
        """Return the mapping of each Widget name to its selection"""
        raise NotImplementedError

    def get_components(self) -> dict[str, Widget]:
        """Return the mapping of each Widget name to its respective Widget"""
        raise NotImplementedError

    def update_selection(self, data: tuple) -> None:
        """Receives information of an updated selection in a colleague

        Mediator pattern method to be called by colleagues (MediatorComponents)"""
        raise NotImplementedError

    def reset_selection(self) -> None:
        """Resets the values of all Widget components"""
        raise NotImplementedError


class NullMediator(WidgetMediator):
    """Null WidgetMediator for behavior when the Mediator does not exist"""

    def update_selection(self, data: tuple) -> None:
        """Does nothing since there is nothing to update"""
        return

    def get_selection(self) -> dict[str, Any]:
        """Return an empty dict since there are no Widgets"""
        return {}

    def get_components(self) -> dict[str, Widget]:
        """Return an empty dict since there are no Widgets"""
        return {}

    def reset_selection(self) -> None:
        """Do nothing since there are no Widgets to reset"""
        return


class MenuMediator(WidgetMediator):
    """Class for mediating a collection of input devices (Menus) that operate on a related
    set of data
    """
    # Private Attributes:
    #   - _data_titles: the titles each component is associated with
    #   - _components: the name of each component mapped to said component
    #   - _titles: all titles of the self._data
    #   - _data: the data used to mediate between colleagues

    _data_titles: dict[MediatorComponent, tuple]
    _components: dict[str, MediatorComponent]

    _titles: tuple
    _data: list[tuple]

    def __init__(self, titles: tuple, data: list[tuple]):
        self._titles = titles
        self._data = data

        self._data_titles = {}
        self._components = {}

    def add_component(self, mc: MediatorComponent, component_name: str, titles: tuple):
        """Adds a component associating it with its given name and titles"""
        self._data_titles[mc] = titles
        self._components[component_name] = mc

    def get_selection(self) -> dict[str, Any]:
        """Return the mapping of each input menu's given name to its selection
        """
        return {name: mc.get_selected() for name, mc in self._components.items()}

    def _get_title_selection(self) -> dict[str, list]:
        """Return the selected objects in a map from data titles to the selections
        """

        selections = {}
        for mc, titles in self._data_titles.items():
            selected = _flatten(mc.get_selected())
            for title in titles:
                if title in selections:
                    selections[title] = selections[title] + selected
                else:
                    selections[title] = selected

        return selections

    def reset_selection(self) -> None:
        """Removes all currently selected options"""
        for mc in self._data_titles:
            mc.reset_selection()
        self.update_selection(())

    def get_components(self) -> dict[str, Widget]:
        """Return all menus handled by this mediator mapped from its arbitrarily given name"""
        return {name: c.get_widget() for name, c in self._components.items()}

    def configure_menu(self, config: str, value: str):
        """Sets the configuration of the specific config to value for all menus
        """
        for mc in self._data_titles:
            mc.configure_menu(config, value)

    def update_selection(self, data: tuple) -> None:
        """Updates all the options of the menus to display only valid selections"""
        self.configure_menu("state", "disabled")
        self._reset_all_menus()
        self.configure_menu("state", "normal")

    def _reset_all_menus(self) -> None:
        """Resets all OptionMenus to only display items that produce a valid selection"""

        filtered_option_rows = filter_data_from_selection(self._data, self._get_title_selection())
        column_map = _map_title_to_column(self._titles, filtered_option_rows)
        for mc, titles in self._data_titles.items():
            mc.set_selection(_flatten([column_map[title] for title in titles]))


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


def _map_title_to_column(titles: tuple, matrix: list[tuple]) -> dict[Any, list]:
    """Return a dict mapping title to the respective column in the matrix

    Preconditions:
        - all(len(titles) == len(row) for row in matrix)
    """

    column_data = _create_column_lists(matrix)
    return {title: column
            for title, column in zip(titles, column_data)}


def _flatten(obj: Any) -> list:

    if _is_collection(obj):
        flattened = []
        for nested_component in obj:
            for element in _flatten(nested_component):
                flattened.append(element)
        return flattened

    return[obj]


def _is_collection(obj: Any):
    return isinstance(obj, Iterable) and not isinstance(obj, str)
