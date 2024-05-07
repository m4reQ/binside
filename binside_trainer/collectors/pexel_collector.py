import dataclasses
import io
import logging
from collections import defaultdict
from concurrent import futures

import requests
from PIL import Image

from binside_trainer import utils
from binside_trainer.collectors.collector import DataCollector
from binside_trainer.training_data import FileType, TrainingData

IMAGES_PER_REQUEST = 5

@dataclasses.dataclass
class DownloadJobResult:
    @classmethod
    def failure(cls):
        result = cls(None) # type: ignore
        result._is_successful = False

        return result

    data: TrainingData
    additional_data: TrainingData | None

    _is_successful: bool = dataclasses.field(init=False, repr=False, default=True)

    @property
    def additional_data_type(self) -> FileType:
        assert self.additional_data is not None
        return self.additional_data.file_type

    @property
    def is_successful(self) -> bool:
        return self._is_successful

    @property
    def has_additional_data(self) -> bool:
        return self.additional_data is not None

    def __hash__(self) -> int:
        return hash((self.data, self.additional_data))

class PexelCollector(DataCollector):
    def __init__(self, concurrent_executor: futures.ThreadPoolExecutor, access_token: str, max_retries_count: int) -> None:
        super().__init__()

        self._access_token = access_token
        self._max_retries_count = max_retries_count

        self._available_images = defaultdict[FileType, list[TrainingData]](list)
        self._next_page = 1

        self._concurrent_executor = concurrent_executor

    def retrieve_data(self, file_type: FileType) -> TrainingData:
        assert file_type in (FileType.PNG, FileType.JPG)

        if len(self._available_images[file_type]) == 0:
            self._retrieve_next_images(file_type)

        return self._available_images[file_type].pop()

    def _retrieve_next_images(self, file_type: FileType) -> None:
        _logger.debug('Requesting images batch of size %d from Pexel API...', self._next_page)

        response = utils.run_with_retry_policy(
            self._max_retries_count,
            lambda: requests.get('https://api.pexels.com/v1/curated', params={'per_page': IMAGES_PER_REQUEST, 'next_page': self._next_page}, headers={'Authorization': self._access_token}),
            _response_successful)

        image_urls: list[str] = [x['src']['original'] for x in response.json()['photos']]
        download_jobs = self._concurrent_executor.map(
            lambda x: self._retrieve_image_and_convert(x, file_type),
            image_urls)

        # await all conversion jobs
        for result in download_jobs:
            if not result.is_successful:
                _logger.error('Skipping failed download job.')
                continue

            self._available_images[file_type].append(result.data)

            if result.has_additional_data:
                assert result.additional_data is not None
                assert result.additional_data_type is not None

                self._available_images[result.additional_data_type].append(result.additional_data)

        self._next_page += 1

    def _retrieve_image_and_convert(self, url: str, file_type: FileType) -> DownloadJobResult:
        img_response = utils.run_with_retry_policy(
            self._max_retries_count,
            lambda: requests.get(url, headers={'Authorization': self._access_token}),
            _response_successful)

        source_file_type: FileType
        match img_response.headers['content-type']:
            case 'image/jpeg':
                source_file_type = FileType.JPG
            case 'image/png':
                source_file_type = FileType.PNG
            case inv_media_type:
                _logger.error('Invalid media type of retrieved image data: %s. Skipping...', inv_media_type)
                return DownloadJobResult.failure()

        result: DownloadJobResult

        if source_file_type == file_type:
            result = DownloadJobResult(TrainingData(file_type, img_response.content))
        else:
            _logger.debug('Converting image from type %s to %s...', source_file_type.name, file_type.name)

            # to not waste api requests and internet throughput save already retrieved image to the appropriate storage
            result = DownloadJobResult(
                _convert_image(img_response.content, file_type),
                TrainingData(source_file_type, img_response.content))

        return result

def _convert_image(data: bytes, file_type: FileType) -> TrainingData:
    source_buffer = io.BytesIO(data)
    pil_img = Image.open(source_buffer)

    buffer = io.BytesIO()
    pil_img.save(buffer, format='png' if file_type == FileType.PNG else 'jpg')

    _logger.debug('Successfully converted image to type %s.', file_type.name)
    return TrainingData(file_type, buffer.getvalue())

def _response_successful(response: requests.Response) -> bool:
    return response.status_code == 200

_logger = logging.getLogger(__name__)
