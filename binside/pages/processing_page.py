from PyQt6 import QtGui, QtWidgets

from binside import utils


class ProcessingPage(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.gif_label: QtWidgets.QLabel
        self.message_label: QtWidgets.QLabel
        self.animation = QtGui.QMovie(':/icons/images/loading_icon.gif')

        utils.load_ui_from_resource(':/uis/ui/processing_page.ui', self)

        self.gif_label.setMovie(self.animation)
        self.animation.start()

    def set_progress_message(self, message: str) -> None:
        self.message_label.setText(message)
