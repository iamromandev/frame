from typing import Any

from loguru import logger
from pydantic import HttpUrl

from src.client.http import HttpClientFactory
from src.core.base import BaseService


class StoryService(BaseService):
    _http_client_factory: HttpClientFactory
    _neuron_run_url: HttpUrl


    def __init__(
        self,
        http_client_factory: HttpClientFactory,
        neuron_base_url: HttpUrl,
        neuron_url_expiration: int
    ) -> None:
        super().__init__()
        self._http_client_factory = http_client_factory
        self._neuron_run_url = HttpUrl(f"{neuron_base_url}agent/run")

    async def generate_story(self) -> dict[str, Any]:
        http_client = self._http_client_factory.get_client(
            url=self._neuron_run_url
        )

        try:
            params = {"prompt": "generate a islamic story"}
            content: dict[str, Any] = await http_client.post(
                url=self._neuron_run_url, data=params
            )
            return content
        except Exception as error:
            logger.error(f"{self._tag}|generate_story(): Connection error: {error}")

        return {}
