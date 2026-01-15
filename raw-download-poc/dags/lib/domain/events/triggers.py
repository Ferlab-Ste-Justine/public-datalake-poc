from collections.abc import AsyncIterator
import traceback
from typing import Any, Optional
import asyncio
import logging


from airflow.triggers.base import BaseEventTrigger, TriggerEvent
from lib.domain.events.base import error_event


class HttpEventTrigger(BaseEventTrigger):
    def __init__(self, url: str, poll_interval: float):
        super().__init__()
        self.url = url
        self.poll_interval = poll_interval

    def serialize(self) -> tuple[str, dict[str, Any]]:
        """Serialize HttpTrigger arguments and classpath."""
        return (
            self.__class__.__module__ + "." + self.__class__.__qualname__,
            {
                "url": self.url,
                "poke_interval": self.poll_interval,
            },
        )

    async def check_response(self, text: str) -> Optional[dict]:
        """Override this method to implement custom response checking logic."""
        raise NotImplementedError("Subclasses must implement check_response method.")

    async def run(self) -> AsyncIterator[TriggerEvent]:
        from lib.utils.http import http_get_text_async

        while True:
            try:
                response_text = await http_get_text_async(self.url)
                event_data = await self.check_response(response_text)
                if event_data:
                    yield TriggerEvent(payload=event_data)
            except Exception as e:
                error_details = traceback.format_exc()
                logging.exception('Error in HttpEventTrigger: %s', e)
                yield error_event(error_details)
            finally:
                await asyncio.sleep(self.poll_interval)
