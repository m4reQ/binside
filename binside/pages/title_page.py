from PyQt6 import QtWidgets

from binside import utils
from binside.widgets.file_drop_area import FileDropArea


class TitlePage(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.file_drop_area: FileDropArea
        self.add_file_button: QtWidgets.QPushButton

        utils.load_ui_from_resource(':/uis/ui/title_page.ui', self)
