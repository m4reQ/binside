from PyQt6 import QtGui, QtWidgets

from binside import utils


class LoadingPage(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.loading_label: QtWidgets.QLabel

        utils.load_ui_from_resource(':/uis/ui/loading_page.ui', self)

        self.animation = QtGui.QMovie(':/icons/images/loading_icon.gif')
        self.loading_label.setMovie(self.animation)
        self.animation.start()
