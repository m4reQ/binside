import webbrowser

from PyQt6 import QtCore, QtWidgets

from binside import resources, utils
from binside.pages.error_page import ErrorPage
from binside.pages.loading_page import LoadingPage
from binside.pages.processing_page import ProcessingPage
from binside.pages.result_page import ResultPage
from binside.pages.title_page import TitlePage
from binside.processing import ProcessingJob, ProcessingResult
from binside_common import ai

DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 720
MODEL_FILEPATH = './tests/modelv2_epoch3_9728.pt'
GITHUB_URL = 'https://github.com/m4reQ/binside'

class LoadingJob(QtCore.QRunnable):
    class Signals(QtCore.QObject):
        finished = QtCore.pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.model: ai.Model | None = None
        self.signals = LoadingJob.Signals()

    def run(self) -> None:
        self.model = ai.load_model(MODEL_FILEPATH)
        self.finished.emit()

    @property
    def finished(self) -> QtCore.pyqtBoundSignal:
        return self.signals.finished

class BinsideApp(QtWidgets.QMainWindow):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()

        self._loading_page = LoadingPage()
        self._title_page = TitlePage()
        self._processing_page = ProcessingPage()
        self._error_page = ErrorPage()
        self._result_page = ResultPage()

        self._model: ai.Model | None = None

        self._thread_pool = QtCore.QThreadPool.globalInstance()
        assert self._thread_pool is not None

        self.page_stack: QtWidgets.QStackedWidget
        self.github_logo_button: QtWidgets.QPushButton

        utils.load_ui_from_resource(':/uis/ui/main_window.ui', self)

        self.setWindowTitle('BINSIDE')
        self.resize(width, height)

        self._loading_job = LoadingJob()
        self._loading_job.finished.connect(self._handle_loading_finished)
        self._thread_pool.start(self._loading_job)

        self._title_page.file_drop_area.files_dropped.connect(self._handle_file_drop)
        self._title_page.add_file_button.clicked.connect(self._handle_add_files_request)
        self._error_page.return_button.clicked.connect(self._handle_return_clicked)
        self._result_page.return_button.clicked.connect(self._handle_return_clicked)
        self.github_logo_button.clicked.connect(self._handle_github_logo_clicked)

        self.page_stack.addWidget(self._loading_page)
        self.page_stack.addWidget(self._title_page)
        self.page_stack.addWidget(self._processing_page)
        self.page_stack.addWidget(self._error_page)
        self.page_stack.addWidget(self._result_page)

    @QtCore.pyqtSlot()
    def _handle_loading_finished(self) -> None:
        self._model = self._loading_job.model

        self._change_page(self._title_page)

    @QtCore.pyqtSlot()
    def _handle_return_clicked(self) -> None:
        self._change_page(self._title_page)

    @QtCore.pyqtSlot()
    def _handle_github_logo_clicked(self) -> None:
        webbrowser.open(GITHUB_URL)

    @QtCore.pyqtSlot()
    def _handle_add_files_request(self) -> None:
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.', 'All Files (*)')
        if len(filepath) == 0:
            return

        self._process_file(filepath)

    @QtCore.pyqtSlot(str)
    def _handle_file_drop(self, filepath: str) -> None:
        self._process_file(filepath)

    @QtCore.pyqtSlot(ProcessingResult)
    def _handle_processing_successful(self, result: ProcessingResult) -> None:
        self._result_page.set_result(result)
        self._change_page(self._result_page)

    @QtCore.pyqtSlot(str)
    def _handle_processing_failed(self, error_message: str) -> None:
        self._error_page.set_error_message(error_message)
        self._change_page(self._error_page)

    @QtCore.pyqtSlot(str)
    def _handle_processing_progress(self, progress_msg: str) -> None:
        self._processing_page.set_progress_message(progress_msg)

    def _process_file(self, filepath: str) -> None:
        self._change_page(self._processing_page)

        job = ProcessingJob(filepath, self._model)
        job.progress.connect(self._handle_processing_progress)
        job.finished.connect(self._handle_processing_successful)
        job.failed.connect(self._handle_processing_failed)

        self._thread_pool.start(job)

    def _change_page(self, page: QtWidgets.QWidget) -> None:
        self.page_stack.setCurrentWidget(page)

def run(argv: list[str]) -> None:
    resources.qInitResources()

    app = QtWidgets.QApplication(argv)
    window = BinsideApp(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    window.show()
    app.exec()

    resources.qCleanupResources()
