import logging
import tkinter as tk
from tkinter import filedialog, font

import tkinterdnd2
from PIL import Image, ImageTk

DIR_ICON_FILEPATH = './binside/resources/plus_icon.png'

class SelectFileArea(tk.Frame):
    def __init__(self, master: tk.Misc, font_family: str) -> None:
        super().__init__(master)

        self._label_font = font.Font(
            self,
            family=font_family,
            size=26,
            weight=font.BOLD)

        icon_size = self._label_font.metrics()['linespace']
        self._dir_icon = ImageTk.PhotoImage(
            Image.open(DIR_ICON_FILEPATH).resize(
                (icon_size, icon_size),
                Image.Resampling.LANCZOS))

        self.configure(bg='#525252', borderwidth=3)
        # file drop support
        self.drop_target_register(tkinterdnd2.DND_FILES) # type: ignore
        self.dnd_bind(
            '<<Drop>>',
            lambda e: self._request_process_file(e.data)) # type: ignore

        self._fill_frame = tk.Frame(self, bg='#8f8f8f')
        self._fill_frame.pack(expand=True, fill='both')
        self._fill_frame.grid_columnconfigure(0, weight=1)
        self._fill_frame.grid_columnconfigure(3, weight=1)
        self._fill_frame.grid_rowconfigure(0, weight=1)
        self._fill_frame.grid_rowconfigure(2, weight=1)

        self._dir_label = tk.Button(
            self._fill_frame,
            image=self._dir_icon,
            command=self._open_file_dialog)
        self._dir_label.grid(row=1, column=1)

        self._add_file_label = tk.Label(
            self._fill_frame,
            text='Choose file you want to scan or drop a file...',
            bg='#8f8f8f',
            fg='white',
            font=self._label_font,
            justify='center')
        self._add_file_label.grid(row=1, column=2)

    def _open_file_dialog(self) -> None:
        filepath = filedialog.askopenfilename()
        if filepath == '':
            return

        self._request_process_file(filepath)

    def _request_process_file(self, filepath: str) -> None:
        _logger.debug('Requested file open for "%s".', filepath)

        self.event_generate('<<ProcessingRequested>>', data={'filepath': filepath})

_logger = logging.getLogger(__name__)
