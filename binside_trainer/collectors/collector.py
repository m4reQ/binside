import abc

from binside_trainer.training_data import FileType, TrainingData


class DataCollector(abc.ABC):
    @abc.abstractmethod
    def retrieve_data(self, file_type: FileType) -> TrainingData: ...
