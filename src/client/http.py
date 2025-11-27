from typing import Any

import aiohttp
from loguru import logger
from pydantic import HttpUrl

from src.core import common
from src.core.factory import SingletonMeta


class HttpClient:
    _client: aiohttp.ClientSession
    _base_url: str

    def __init__(
        self,
        base_url: HttpUrl | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> None:
        self._base_url = str(base_url).rstrip("/") if base_url else ""
        timeout = aiohttp.ClientTimeout(
            total=timeout,
        ) if timeout else None
        self._client = aiohttp.ClientSession(
            base_url=self._base_url,
            headers=headers,
            timeout=timeout,
            raise_for_status=True
        )

    @property
    def _tag(self) -> str:
        return self.__class__.__name__

    async def close(self) -> None:
        logger.debug(f"{self._tag}|close(): Closing HTTP client")
        await self._client.close()

    async def get(
        self,
        url: HttpUrl,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        as_text: bool = False,
    ) -> str | dict[str, Any]:
        path = common.get_path(url)
        logger.debug(
            f"{self._tag}|get(): base_url[{self._base_url}] "
            f"path[{path}] full_url[{url}] params[{params}] headers[{headers}]"
        )

        async with self._client.get(url=path, params=params, headers=headers) as response:
            if as_text:
                content = await response.text()
                logger.debug(
                    f"{self._tag}|get(): status_code[{response.status}] "
                    f"response_text_length[{len(content)}]"
                )
            else:
                content = await response.json()
                logger.debug(
                    f"{self._tag}|get(): status_code[{response.status}] "
                    f"response_json[{content}]"
                )
        return content

    async def post(
        self,
        url: HttpUrl,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
        as_text: bool = False,
    ) -> str | dict[str, Any]:
        path = common.get_path(url)
        logger.debug(
            f"{self._tag}|post(): base_url[{self._base_url}] "
            f"path[{path}] data[{data}] headers[{headers}]"
        )

        async with self._client.post(url=path, json=data, headers=headers) as response:

            if as_text:
                content = await response.text()
                logger.debug(
                    f"{self._tag}|post(): status_code[{response.status}] "
                    f"response_text_length[{len(content)}]"
                )
            else:
                content = await response.json()
                logger.debug(
                    f"{self._tag}|post(): status_code[{response.status}] "
                    f"response_json[{content}]"
                )

        return content


class HttpClientFactory(metaclass=SingletonMeta):
    _initialized: bool = False
    _clients: dict[HttpUrl, HttpClient]

    def __init__(self) -> None:
        if self._initialized:
            return
        self._clients: dict[HttpUrl, HttpClient] = {}
        self._initialized = True

    @property
    def _tag(self) -> str:
        return self.__class__.__name__

    def get_client(
        self,
        url: HttpUrl,
        headers: dict[str, str] | None = None,
    ) -> HttpClient:
        base_url: HttpUrl = common.get_base_url(url)
        logger.debug(f"{self._tag}|get_client(): base_url[{base_url}]")
        if base_url not in self._clients:
            logger.debug(
                f"{self._tag}|get_client(): Creating new HttpClient for base_url[{base_url}]"
            )
            client = HttpClient(base_url=base_url, headers=headers)
            self._clients[base_url] = client

        return self._clients[base_url]

    async def close_all(self):
        logger.debug(f"{self._tag}|close_all(): Closing all HttpClient instances")
        for client in self._clients.values():
            await client.close()
        self._clients.clear()
