"""Промежуточное ПО для логирования."""

import logging
import random
import string
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования HTTP запросов и ответов."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Обработка HTTP запроса и логирование.

        Args:
            request: Входящий HTTP запрос.
            call_next: Следующий обработчик запроса.

        Returns:
            Ответ на HTTP запрос.
        """
        request_uuid = self._get_request_id()

        # Записываем информацию о запросе
        logging.info(f"Request [{request_uuid}]: {request.method} {request.url}")

        start_time = time.time()

        # Делаем запрос
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = f"{process_time:.2f}"

        # Записываем информацию об ответе
        logging.info(
            f"Response [{request_uuid}]: completed_in={formatted_process_time}ms "
            f"staus_code={response.status_code}"
        )

        return response

    @staticmethod
    def _get_request_id() -> str:
        """Возвращает уникальный ID запроса."""
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
