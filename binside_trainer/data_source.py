import abc
import dataclasses

from binside_trainer.training_data import TrainingData


@dataclasses.dataclass
class DataSourceStatistics:
    pass

class DataSource(abc.ABC):
    @abc.abstractmethod
    def release(self) -> None: ...

    @abc.abstractmethod
    def get_next_data(self) -> TrainingData: ...

    @abc.abstractmethod
    def get_statistics(self) -> DataSourceStatistics: ...
