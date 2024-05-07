import logging
import typing as t


def run_with_retry_policy[T](max_retries: int, func: t.Callable[[], T], is_successful: t.Callable[[T], bool]) -> T:
    retries_count = 0
    while retries_count < max_retries:
        result = func()
        if is_successful(result):
            return result

        _logger.debug('Retry function call to %s, current retry count: %d.', func.__name__, retries_count)
        retries_count += 1

    raise RuntimeError('Exceeded max retries count for function call to %s.', func.__name__)

_logger = logging.getLogger(__name__)
