import dataclasses
import enum

import numpy as np
import numpy.typing as npt


class FileType(enum.IntEnum):
    EXE = 0
    TXT = 1
    JPG = 2
    PNG = 3
    BMP = 4
    # WAV = 5
    # MP3 = 6

@dataclasses.dataclass
class RawData:
    data: bytes = dataclasses.field(repr=False)
    file_type: FileType

    @property
    def size(self) -> int:
        return len(self.data)

@dataclasses.dataclass
class ProcessedData:
    data: npt.NDArray[np.float32]
    file_type: FileType

def process_memory(memory: bytes) -> npt.NDArray[np.float32]:
    frequency = np.zeros((256, 256), dtype=np.uint64)
    np_data = np.frombuffer(memory, dtype=np.uint8)

    pairs = np.lib.stride_tricks.as_strided(np_data, (len(memory) - 1, 2), np_data.strides * 2)
    np.add.at(frequency, (pairs[:, 0], pairs[:, 1]), 1)

    _log = np.log(frequency, out=np.zeros_like(frequency, dtype=np.float32), where=(frequency != 0))
    _max = np.max(_log)

    return _log / _max

def convert_float_array_to_ubyte(arr: npt.NDArray[np.float32]) -> npt.NDArray[np.uint8]:
    return (arr * 255.0).astype(np.uint8)
