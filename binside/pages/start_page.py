import tkinter as tk

from binside.widgets import AboutArea, SelectFileArea, TitleBar


class StartPage(tk.Frame):
    def __init__(self, master: tk.Misc, font_family: str) -> None:
        super().__init__(master)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._title_bar = TitleBar(self, font_family)
        self._title_bar.grid(row=0, column=0, sticky='new')

        self._select_file_area = SelectFileArea(self, font_family)
        self._select_file_area.grid(row=1, column=0, sticky='nsew')

        self._about_area = AboutArea(self, font_family)
        self._about_area.grid(row=2, column=0, sticky='new', pady=(15, 0))
