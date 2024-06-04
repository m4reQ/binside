from PyQt6 import QtWidgets

from binside import utils


class ErrorPage(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.error_message: QtWidgets.QLabel
        self.return_button: QtWidgets.QPushButton

        utils.load_ui_from_resource(':/uis/ui/error_page.ui', self)

    def set_error_message(self, message: str) -> None:
        self.error_message.setText(message)
