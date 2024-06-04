from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt

from binside import utils
from binside.processing import ProcessingResult


class ResultPage(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.file_logo: QtWidgets.QLabel
        self.filepath_label: QtWidgets.QLabel
        self.file_size_label: QtWidgets.QLabel
        self.analysis_time_label: QtWidgets.QLabel
        self.file_type_best: QtWidgets.QLabel
        self.file_type_2: QtWidgets.QLabel
        self.file_type_3: QtWidgets.QLabel
        self.file_type_4: QtWidgets.QLabel
        self.memory_map_img: QtWidgets.QLabel
        self.return_button: QtWidgets.QPushButton

        utils.load_ui_from_resource(':/uis/ui/result_page.ui', self)

    def set_result(self, result: ProcessingResult) -> None:
        font_metrics = QtGui.QFontMetrics(self.filepath_label.font())
        filepath_text = font_metrics.elidedText(
            result.filepath,
            Qt.TextElideMode.ElideRight,
            self.file_logo.width())

        self.filepath_label.setText(filepath_text)
        self.filepath_label.setToolTip(result.filepath)
        self.file_size_label.setText(f'{(result.file_size / 1024):.2f}kB')
        self.analysis_time_label.setText(f'{result.analysis_time:.4f}s')

        assert len(result.predictions) >= 4
        predictions_sorted = sorted(result.predictions.items(), key=lambda x: x[1], reverse=True)

        self._set_prediction_text(self.file_type_best, predictions_sorted[0])
        self._set_prediction_text(self.file_type_2, predictions_sorted[1])
        self._set_prediction_text(self.file_type_3, predictions_sorted[2])
        self._set_prediction_text(self.file_type_4, predictions_sorted[3])

        self.memory_map_img.setPixmap(result.generated_image)

    def _set_prediction_text(self, label: QtWidgets.QLabel, prediction: tuple[str, float]) -> None:
        text = f'{prediction[0]} ({(prediction[1] * 100.0):.2f}%)'
        label.setText(text)
