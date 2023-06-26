from time import time
from typing import Callable, Any
from typing import Coroutine

from prometheus_client import Gauge
from prometheus_fastapi_instrumentator.metrics import Info

start_app_time = time()


def http_requested_app_work_time() -> Callable[[Info], Coroutine[Any, Any, None]]:
    METRIC = Gauge(
        "http_requested_test",
        "Number of times a certain language has been requested.",
        labelnames=("timestamp",)
    )

    async def instrumentation(info: Info) -> None:
        request_time = time()
        result = request_time - start_app_time
        METRIC.labels(timestamp=1).set(value=result)

    return instrumentation
