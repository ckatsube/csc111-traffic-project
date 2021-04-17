"""I/O devices for interacting with the shortest path program
"""

from tkinter import Button, Frame, Label, Tk
from typing import Callable

from mediatorbuilder import NullMediatorBuilder, MediatorBuilder


class InputFrameBuilder:
    """Builder class for inputting the settings for the input frame
    """
    # Private Attributes:
    #   - _data: the data to display to the user to select from
    #   - _geometry: the geometry of the built frame
    #   - _title: the title of the built frame
    #   - _mb: the MediatorBuilder to use to let input fields interact with each other
    #   - _command: the output function to be called when hitting Export Selection

    _data: list[tuple]

    _geometry: str = "300x150"
    _title: str = "Settings Input"

    _mb: MediatorBuilder = NullMediatorBuilder()

    _command = print

    def set_data(self, data: list[tuple]):
        """Sets the data to be used for selecting options"""
        self._data = data

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
