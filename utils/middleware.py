import time

from starlette.middleware.base import BaseHTTPMiddleware

from utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        logger.info(
            f"Request: {request.method} {request.url.path}"
        )

        response = await call_next(request)

        process_time = round(
            time.time() - start_time,
            3
        )

        logger.info(
            f"Completed {response.status_code} in {process_time}s"
        )

        return response