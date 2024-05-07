import enum
import queue
import random
import threading
import typing as t

from binside_trainer.collectors import PixivDataCollector
from binside_trainer.data_source import DataSource, DataSourceStatistics
from binside_trainer.training_data import FileType, TrainingData

MAX_DATA_QUEUE_SIZE = 10

class OnlineDataSource(DataSource):
    def __init__(self, max_data_queue_size: int = MAX_DATA_QUEUE_SIZE) -> None:
        self._data_queue = queue.Queue[TrainingData](maxsize=max_data_queue_size)

        self._collector_thread_should_run = True
        self._collector_thread = threading.Thread(target=self._collector_thread_main)
        self._collector_thread.start()

        pixiv_data_collector = PixivDataCollector()
        self._collectors = {
            FileType.JPG: (pixiv_data_collector, 0),
            FileType.PNG: (pixiv_data_collector, 0),
        }

    def release(self) -> None:
        self._collector_thread_should_run = False
        self._collector_thread.join()

    def get_next_data(self) -> TrainingData:
        pass

    def get_statistics(self) -> DataSourceStatistics:
        return super().get_statistics()

    def _collector_thread_main(self) -> None:
        while self._collector_thread_should_run:
            file_type = _get_random_enum_value(FileType)
            memory: bytes

            self._collectors[file_type].g
            match file_type:
                case FileType.JPG | FileType.PNG:
                    memory = self._retrieve_random_pixiv_image(file_type)
                case _:
                    raise NotImplementedError('collector for file type not implemented')

            data = TrainingData(file_type, memory)
            self._data_queue.put(data)

    def _retrieve_random_pixiv_image(self, dst_filetype: FileType) -> bytes:
        pass

TEnum = t.TypeVar('TEnum', bound=enum.Enum)
def _get_random_enum_value(_enum: type[TEnum]) -> TEnum:
    return random.choice(_enum._member_map_.values())
