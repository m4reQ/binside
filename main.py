import logging
import pathlib
import time
from concurrent import futures

from binside import app
from binside_trainer.collectors import (FilesystemCollector, PexelCollector,
                                        WikipediaCollector)
from binside_trainer.training_data import FileType

logging.basicConfig(level=logging.DEBUG)

# if __name__ == '__main__':
#     concurrent_executor = futures.ThreadPoolExecutor()
#     max_retries_count = 5

#     pexel_collector = PexelCollector(concurrent_executor, 'Fgh0OoeDEavtXiDWlJn9ONKatG31E6crKCyTZDvOlMxK7GdKpIGdgUpN', max_retries_count) # jpg, png
#     filesystem_collector = FilesystemCollector(pathlib.Path('C:/')) # exe
#     wikipedia_collector = WikipediaCollector(concurrent_executor, max_retries_count) # txt
#     # TODO: mp3 collector (with freesound api)

#     wikipedia_collector.retrieve_data(FileType.TXT)

#     pass


if __name__ == '__main__':
    app = app.create_app()
    app.mainloop()
