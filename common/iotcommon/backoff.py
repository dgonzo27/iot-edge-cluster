"""wrapper that will back off az service throwing a throttle exception"""

import logging
import random
import time

from dataclasses import dataclass, field
from typing import Callable, List, Optional, TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)


class BackoffError(Exception):
    pass


def is_common_throttle_exception(ex: Exception) -> bool:
    """checks if exception is commonly known az throttle"""
    status_code: Optional[int] = None
    if hasattr(ex, "status_code"):
        # e.g. azure.core.exceptions.HttpResponseError
        status_code = int(getattr(ex, "status_code"))
    elif hasattr(ex, "status"):
        # e.g. aiohttp.client_exceptions.ClientResponseError
        status_code = int(getattr(ex, "status"))
    return status_code is not None and (status_code == 503 or status_code == 429)


@dataclass
class BackoffStrategy:
    waits: List[float] = field(default_factory=lambda: [1.0, 2.0, 4.0, 7.0, 16.0])
    """a list of values in seconds that a backoff should wait, in order"""

    spread_percentage: float = 0.2
    """variance around the wait seconds to actually wait
    - used to introduce some randomness to combat machine synchronization
    """

    def spread(self, seconds: float) -> float:
        """
        takes the given time in seconds and picks a random point
        around it defined by the spread percentage (e.g. 6 seconds 
        with a 0.2 spread percentage will be between 4.8 and 7.2 
        seconds)
        """
        sp = self.spread_percentage
        return seconds * random.uniform(1 - sp, 1 + sp)


def with_backoff(
    fn: Callable[[], T],
    strategy: Optional[BackoffStrategy] = None,
    is_throttle: Optional[Callable[[Exception], bool]] = None,
) -> T:
    """
    executes the given function (fn) - if an exception is raised 
    that returns True from `is_throttle`, wait and retry - or fail 
    after exhausting all backoff strategies
    """
    if strategy is None:
        strategy = BackoffStrategy()
    
    if is_throttle is None:
        is_throttle = is_common_throttle_exception
    
    throttle_exception: Optional[Exception] = None

    for backoff_wait_seconds in strategy.waits:
        try:
            return fn()
        except Exception as ex:
            if is_throttle(ex):
                actual_wait = backoff_wait_seconds * random.uniform(0.8, 1.2)
                logger.warning(
                    f"service responded with throttling message - "
                    f"trying again in {actual_wait:.1f} seconds..."
                )
                time.sleep(actual_wait)
                throttle_exception = ex
            else:
                raise
    
    # try as we might, sometimes we fail
    raise BackoffError(
        f"potential throttling issue - see inner exception\n\n"
        f"tried backoff {len(strategy.waits)} times "
        f"up to {strategy.waits[-1]} seconds"
    ) from throttle_exception
