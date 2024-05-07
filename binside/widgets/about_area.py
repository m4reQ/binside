import tkinter as tk
from tkinter import font

DESCRIPTION_HEADER = 'What is Binside?'
DESCRIPTION_TEXT = 'Binside is a reverse engineering tool that allows you to guess binary format of unknown files based on produced memory pattern. Binside generates images that represent frequency of bytes in a block of memory, which are then classified using AI model to recognize common file types like EXE or JPG. Application can detect the following file types: JPG, PNG, EXE, TXT, MP3.'

class AboutArea(tk.Frame):
    def __init__(self, master: tk.Misc, font_family: str) -> None:
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._header_font = font.Font(
            self,
            family=font_family,
            size=22,
            weight=font.BOLD)
        self._text_font = font.Font(
            self,
            family=font_family,
            size=15)

        self._header_label = tk.Label(self, text=DESCRIPTION_HEADER, font=self._header_font)
        self._header_label.grid(row=0, column=0, sticky='wn')

        self._text_label = tk.Label(self, text=DESCRIPTION_TEXT, font=self._text_font, justify='left')
        self._text_label.grid(row=1, column=0, sticky='wne')
        self._text_label.bind(
            '<Configure>',
            lambda _: self._text_label.config(wraplength=self._text_label.winfo_width()))
