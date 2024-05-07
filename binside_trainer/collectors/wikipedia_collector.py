import logging
import urllib.parse
from concurrent import futures

import requests
from bs4 import BeautifulSoup

from binside_trainer import utils
from binside_trainer.collectors.collector import DataCollector
from binside_trainer.training_data import FileType, TrainingData

ARTICLES_PER_REQUEST = 5

class WikipediaCollector(DataCollector):
    def __init__(self, concurrent_executor: futures.ThreadPoolExecutor, max_retries_count: int) -> None:
        super().__init__()

        self._concurrent_executor = concurrent_executor
        self._max_retries_count = max_retries_count
        self._available_data: list[TrainingData] = []

    def retrieve_data(self, file_type: FileType) -> TrainingData:
        assert file_type == FileType.TXT

        if len(self._available_data) == 0:
            self._retrieve_new_data(file_type)

        return self._available_data.pop()

    def _retrieve_new_data(self, file_type: FileType) -> None:
        _logger.debug('Getting new list of %d articles from wikipedia.org...', ARTICLES_PER_REQUEST)

        params = {
            'action': 'query',
            'format': 'json',
            'list': 'random',
            'rnlimit': ARTICLES_PER_REQUEST,
            'rnnamespace': 0} # only request articles
        articles_response = utils.run_with_retry_policy(
            self._max_retries_count,
            lambda: requests.get('https://en.wikipedia.org/w/api.php', params=params),
            _response_successful)

        article_titles: list[int] = [x['title'] for x in articles_response.json()['query']['random']]
        download_jobs = self._concurrent_executor.map(
            lambda x: self._download_article_and_extract(x, file_type),
            article_titles)

        for result in download_jobs:
            self._available_data.append(result)

    def _download_article_and_extract(self, title: str, file_type: FileType) -> TrainingData:
        _logger.debug('Getting article data for "%s"...', title)

        params = {
            'action': 'parse',
            'format': 'json',
            'page': title}
        response = utils.run_with_retry_policy(
            self._max_retries_count,
            lambda: requests.get('https://en.wikipedia.org/w/api.php', params=params),
            _response_successful)

        _logger.debug('Extracting plain text from article "%s"...', title)

        html_text = urllib.parse.unquote(response.json()['parse']['text']['*'])
        bs = BeautifulSoup(html_text)

        plain_text = ' '.join(bs.stripped_strings)

        return TrainingData(file_type, plain_text.encode())

def _response_successful(response: requests.Response) -> bool:
    return response.status_code == 200

_logger = logging.getLogger(__name__)
