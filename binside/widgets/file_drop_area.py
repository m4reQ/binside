import os

from PyQt6 import QtCore, QtGui, QtWidgets


class FileDropArea(QtWidgets.QFrame):
    files_dropped = QtCore.pyqtSignal(str)

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent | None) -> None:
        if event is None:
            return super().dragEnterEvent(event)

        # allow only drop for single elements that have urls associated with them and are not a directory
        # effectively allowing to only drop singular files

        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            dirs_present = any(os.path.isdir(_sanitize_qt_path(x.path())) for x in urls)
            if len(urls) != 1 or dirs_present:
                event.ignore()
                return

            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent | None) -> None:
        urls = event.mimeData().urls()
        assert len(urls) == 1

        self.files_dropped.emit(_sanitize_qt_path(urls[0].path()))

def _sanitize_qt_path(path: str) -> str:
    return path.lstrip('/')
