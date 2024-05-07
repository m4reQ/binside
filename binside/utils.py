import tkinter as tk
import typing as t


def bind_with_data(widget: tk.Misc, sequence: str, callback: t.Callable[[tk.Event], None], add: str | None = None) -> None:
    '''
    Bind function `callback` to the virtual event `sequence`.
    This function adds support for the missing `data` member of virtual events,
    which is missing in Tkinter code.
    Note that every event that is intended to be used with this function has to pass its data
    using dictionary.

    :param widget: A parent widget.
    :param sequence: Virtual event name to bind to.
    :param callback: Callback function that will be executed when `sequence` event is fired.
    :param add: Describes how the callback should be registered.
    '''

    def _substitute(*args):
        e = lambda: None
        # NOTE: Dangerous use of eval!
        e.data = eval(args[0])
        e.widget = widget

        return (e, )

    _id = widget._register(callback, _substitute)
    cmd = f'{"+" if add else ""}if {{"[{_id} %d]" == "break"}} break\n'

    widget.tk.call('bind', widget._w, sequence, cmd)
