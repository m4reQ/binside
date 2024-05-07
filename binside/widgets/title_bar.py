import tkinter as tk
import webbrowser
from tkinter import font

from PIL import Image, ImageTk

TITLE_SIZE = 40
GITHUB_LOGO_FILEPATH = './binside/resources/github_logo.png'
GITHUB_HOMEPAGE_LINK = 'https://github.com/m4reQ/binside'

class TitleBar(tk.Frame):
    def __init__(self, master: tk.Misc, font_family: str) -> None:
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._title_font = font.Font(self, family=font_family, size=TITLE_SIZE, weight=font.BOLD)

        github_logo_size = self._title_font.metrics()['linespace']
        self._github_logo = ImageTk.PhotoImage(Image.open(GITHUB_LOGO_FILEPATH).resize((github_logo_size, github_logo_size)))

        self._title_label = tk.Label(self, text='BINSIDE', font=self._title_font)
        self._title_label.grid(row=0, column=0, sticky='new')

        self._homepage_button = tk.Label(self, image=self._github_logo)
        self._homepage_button.bind('<Button-1>', lambda _: webbrowser.open(GITHUB_HOMEPAGE_LINK))
        self._homepage_button.grid(row=0, column=1, sticky='ne')
