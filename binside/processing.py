import dataclasses
import os
import time

from PyQt6 import QtCore, QtGui

from binside_common import ai, processing


@dataclasses.dataclass
class ProcessingResult:
    filepath: str
    file_size: int
    generated_image: QtGui.QPixmap
    predictions: dict[str, float]
    analysis_time: float

class ProcessingJob(QtCore.QRunnable):
    class Signals(QtCore.QObject):
        progress = QtCore.pyqtSignal(str)
        finished = QtCore.pyqtSignal(ProcessingResult)
        failed = QtCore.pyqtSignal(str)

    def __init__(self, filepath: str, model: ai.Model) -> None:
        super().__init__()

        self.filepath = os.path.abspath(filepath)
        self.model = model
        self.signals = ProcessingJob.Signals()

    def run(self) -> None:
        start = time.perf_counter()
        self.progress.emit(f'Reading file "{self.filepath}"...')

        if not os.path.exists(self.filepath):
            self.failed.emit(f'Couldn\'t open file "{self.filepath}": file does not exist.')
            return

        with open(self.filepath, 'rb') as f:
            file_data = f.read()

        file_size = len(file_data)

        self.progress.emit('Generating memory map...')

        memory_map = processing.process_memory(file_data)
        memory_map_ubyte = processing.convert_float_array_to_ubyte(memory_map)
        memory_map_img = QtGui.QImage(
            memory_map_ubyte,
            memory_map_ubyte.shape[1],
            memory_map_ubyte.shape[1],
            memory_map_ubyte.shape[1],
            QtGui.QImage.Format.Format_Grayscale8)

        self.progress.emit('Classifying generated memory map...')

        predictions = ai.classify_memory_map(self.model, memory_map)

        result = ProcessingResult(
            self.filepath,
            file_size,
            QtGui.QPixmap(memory_map_img),
            predictions,
            time.perf_counter() - start)
        self.signals.finished.emit(result)

    @property
    def progress(self) -> QtCore.pyqtBoundSignal:
        return self.signals.progress

    @property
    def finished(self) -> QtCore.pyqtBoundSignal:
        return self.signals.finished

    @property
    def failed(self) -> QtCore.pyqtBoundSignal:
        return self.signals.failed
