import tkinter as tk

from binside import utils

LOADING_ICON_FILEPATH = './binside/resources/loading_icon.gif'
FRAMES_COUNT = 12
TIMEOUT = 350

class ProcessingPage(tk.Frame):
    def __init__(self, master: tk.Misc, font_family: str) -> None:
        super().__init__(master)

        self._loading_icon_frames = [tk.PhotoImage(file=LOADING_ICON_FILEPATH, format=f'gif -index {x}') for x in range(FRAMES_COUNT)]
        self._current_icon_frame = 0

        self._loading_icon = tk.Label(self, image=self._loading_icon_frames[0])
        self._loading_icon.pack(side='top')

        self._message_label = tk.Label(self, text='')
        self._message_label.pack(side='top')

        utils.bind_with_data(
            self,
            '<<ProcessingMessageChanged>>',
            self._handle_set_message)

        self._after_func_id = self.after(TIMEOUT, self._get_next_icon_frame)

    def _handle_set_message(self, e: tk.Event) -> None:
        self._message_label.configure(text=e.data['message'])

    def _get_next_icon_frame(self) -> None:
        current_icon = self._loading_icon_frames[self._current_icon_frame % FRAMES_COUNT]
        self._current_icon_frame += 1

        self._loading_icon.configure(image=current_icon)

        self._after_func_id = self.after(TIMEOUT, self._get_next_icon_frame)

    def __del__(self) -> None:
        self.after_cancel(self._after_func_id)

