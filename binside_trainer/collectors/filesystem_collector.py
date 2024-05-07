import pathlib

from binside_trainer.collectors.collector import DataCollector
from binside_trainer.training_data import FileType, TrainingData


class FilesystemCollector(DataCollector):
    def __init__(self, directory: pathlib.Path) -> None:
        super().__init__()

        self._directory_iter = (x for x in directory.rglob('*.exe') if x.is_file() and not x.is_symlink())

    def retrieve_data(self, file_type: FileType) -> TrainingData:
        assert file_type == FileType.EXE

        with next(self._directory_iter).open(mode='rb') as f:
            data = f.read()

        return TrainingData(file_type, data)
