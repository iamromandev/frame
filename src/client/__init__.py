from collections.abc import AsyncGenerator

from src.core.config import settings

from .cache import CacheClient
from .http import HttpClientFactory


async def get_cache_client(
) -> AsyncGenerator[CacheClient]:
    yield CacheClient(
        cache_url=settings.cache_url
    )


async def get_http_client_factory(
) -> AsyncGenerator[HttpClientFactory]:
    yield HttpClientFactory(
    )
