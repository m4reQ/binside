import dataclasses
import enum


class FileType(enum.IntEnum):
    EXE = enum.auto()
    JPG = enum.auto()
    PNG = enum.auto()
    TXT = enum.auto()
    WAV = enum.auto()
    UNKNOWN = enum.auto()

@dataclasses.dataclass
class TrainingData:
    file_type: FileType
    memory: bytes = dataclasses.field(repr=False)

    @property
    def size(self) -> int:
        return len(self.memory)

    def __hash__(self) -> int:
        return hash((self.file_type, self.memory))
