"""Module containing the classes for utilizing the WidgetMediator

"""

from __future__ import annotations

from tkinter import Button, Frame, Variable, OptionMenu, Widget
from typing import Any, Callable


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

    def get_selected_rows(self) -> set[int]:
        """Return the row # of the current selection using the innate data vector"""
        raise NotImplementedError

    def restrict_selection(self, filtered_option_rows: set[int]) -> None:
        """Restrict the selection of this component to the data in the selected row"""
        raise NotImplementedError


class OptionMenuComponent(MediatorComponent):
    """WidgetMediator component that contains an OptionMenu

    Representation Invariants:
        - self._var.get() == "" or self._var_get() in self._data
            equivalent to (if self._var.get() != "" then self.var.get() in self._data)
    """

    _name: str

    _var: Variable
    _om: OptionMenu
    _data: list[list]

    _parent: Widget
    _mediator: MenuMediator

    def __init__(self, parent: Widget, mediator: MenuMediator, name: str, data: list[list]):
        self._name = name
        self._var = Variable()
        self._parent = parent
        self._mediator = mediator
        self._om = OptionMenu(parent, self._var, "", *sorted({obj for inner in data for obj in inner}),
                              command=lambda _: mediator.update_selection(()))
        self._data = data

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

        menu.add_command(label="", command=click_command(self._var, ""))
        for option in data:
            menu.add_command(label=option, command=click_command(self._var, option))

    def get_widget(self) -> Widget:
        """Return a list containing this OptionMenu"""
        return self._om

    def configure_menu(self, config: str, value: str) -> None:
        """Configures the setting of the composed dOptionMenu"""
        self._om[config] = value

    def get_selected_rows(self) -> set[int]:
        """Return a set containing the index of the current variable value in the OptionMenu's
        source data

        Return a set of all indices if the value is an empty string"""

        value = self._var.get()
        if value == "":
            return {i for i in range(0, len(self._data[0]))}
        else:
            for row in range(0, len(self._data[0])):
                if any(self._data[col][row] == value for col in range(len(self._data))):
                    return {row}

    def get_selected(self) -> Any:
        """Return the current variable's value"""
        return self._var.get()

    def restrict_selection(self, filtered_option_rows: set[int]) -> None:
        """Overwrites the OptionMenu's options to only display the values corresponding to the rows
        in filtered_option_rows

        Precondition:
            - all(0 <= row < len(self._data) for all row in filtered_option_rows)
        """
        return


def _delete_menu_options(om: OptionMenu) -> None:
    """Deletes all items/commands from the OptionMenu"""
    menu = om["menu"]

    start, end = 0, "end"
    menu.delete(start, end)


class OptionListComponent(MediatorComponent, Frame):
    """WidgetMediator component allowing for adding and deleting an arbitrary number of
    OptionMenus that rely on the same dataset
    """

    _menu_components: list[OptionMenuComponent] = []
    _menu_frame: Frame

    _name: str
    _data: list[list]

    _parent: Widget
    _mediator: MenuMediator

    def __init__(self, parent: Widget, mediator: MenuMediator, name: str, data: list[list]):
        super().__init__(parent)
        self._name = name
        self._parent = parent
        self._mediator = mediator
        self._data = data

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
        """Adds an OptionMenu to the OptionListComponent"""

        omc = OptionMenuComponent(self._menu_frame, self._mediator, self._name, self._data)
        self._menu_components.append(omc)

        om = omc.get_widget()
        om.pack(anchor="n")

        self._mediator.update_selection(())

    def remove_option_menu(self) -> None:
        """Removes an OptionMenu from the OptionListComponent"""
        if self._menu_components:
            omc = self._menu_components.pop()

            om = omc.get_widget()
            om.pack_forget()

    def reset_selection(self) -> None:
        """Sets the all option menu variables to an empty string"""
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

    def get_selected_rows(self) -> set[int]:
        """Return a set containing the index of the current variable value in the OptionMenu's
        source data

        Return a set of all indices if the value is an empty string"""

        if all(value == "" for value in self.get_selected()):
            return {i for i in range(0, len(self._data[0]))}
        else:
            selected_rows = (om.get_selected_rows() for om in self._menu_components)
            return set.union(*selected_rows)

    def get_selected(self) -> Any:
        """Return the current variable's value"""
        return tuple(om.get_selected() for om in self._menu_components)

    def restrict_selection(self, filtered_option_rows: set[int]) -> None:
        """Overwrites the OptionMenu's options to only display the values corresponding to the rows
        in filtered_option_rows

        Precondition:
            - all(0 <= row < len(self._data) for all row in filtered_option_rows)
        """
        return  # deprecated


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

    _components: dict[str, MediatorComponent] = {}

    def add_component(self, name: str, mc: MediatorComponent):
        """Adds a component"""
        self._components[name] = mc

    def get_selection(self) -> dict[str, Any]:
        """Return the selected options"""
        return {name: mc.get_selected() for name, mc in self._components.items()}

    def reset_selection(self) -> None:
        """Removes all currently selected options"""
        for mc in self._components.values():
            mc.reset_selection()
        self.update_selection(())

    def get_components(self) -> dict[str, Widget]:
        """Return all menus handled by this mediator mapped from its arbitrarily given name"""
        return {title: c.get_widget() for title, c in self._components.items()}

    def configure_menu(self, config: str, value: str):
        """Sets the configuration of the specific config to value for all menus
        """
        for mc in self._components.values():
            mc.configure_menu(config, value)

    def update_selection(self, data: tuple) -> None:
        """Updates all the options of the menus to display only valid selections"""
        self.configure_menu("state", "disabled")
        self._reset_all_menus()
        self.configure_menu("state", "normal")

    def _reset_all_menus(self) -> None:
        """Resets all OptionMenus to only display items that produce a valid selection"""

        filtered_option_rows = self._get_filtered_options()
        for mc in self._components.values():
            mc.restrict_selection(filtered_option_rows)

    def _get_filtered_options(self) -> set[int]:
        """Return the set of row numbers such that every selected value is in that row of the data
        """

        row_selections_per_menu = [mc.get_selected_rows() for mc in self._components.values()]
        candidate_rows = set.union(*row_selections_per_menu)

        selected_rows = {row for row in candidate_rows if
                         all({row in selection for selection in row_selections_per_menu})}

        return selected_rows
