import logging
import threading
import time
import tkinter as tk

import tkinterdnd2

from binside import utils
from binside.pages import ProcessingPage, StartPage

DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 720

FONT_FAMILY = 'Cascadia Mono'

class App(tkinterdnd2.Tk):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()

        self._current_page: tk.Frame | None = None
        self._start_page = StartPage(self, FONT_FAMILY)
        self._processing_page = ProcessingPage(self, FONT_FAMILY)

        self._processing_thread: threading.Thread | None = None

        self.title('BINSIDE')
        self.geometry(f'{width}x{height}')

        self._change_page(self._start_page)

        utils.bind_with_data(self, '<<ProcessingRequested>>', self._handle_processing_requested)

    def _change_page(self, page: tk.Frame) -> None:
        if self._current_page is not None:
            self._current_page.pack_forget()

        self._current_page = page
        self._current_page.pack(fill='both', expand=True, pady=15, padx=15)

    def _handle_processing_requested(self, e: tk.Event) -> None:
        filepath: str = e.data['filepath'] # type: ignore
        assert filepath

        self._change_page(self._processing_page)

        self._processing_thread = threading.Thread(target=self._process_filepath, args=[filepath])
        self._processing_thread.start()

    def _set_processing_message(self, message: str) -> None:
        self.event_generate('<<ProcessingMessageChanged>>', data={'message': message})

    def _process_filepath(self, filepath: str) -> None:
        self._set_processing_message(f'Reading file {filepath}...')
        _logger.debug('Reading file %s...', filepath)

        # FIXME temporary
        time.sleep(3)

        with open(filepath, 'rb') as f:
            data = f.read()

        self._set_processing_message('Generating memory map...')

def create_app() -> tk.Tk:
    return App(DEFAULT_WIDTH, DEFAULT_HEIGHT)

_logger = logging.getLogger(__name__)
