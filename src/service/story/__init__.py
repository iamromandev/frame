from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from pydantic import Field

from src.client import HttpClientFactory, get_http_client_factory
from src.core.config import settings

from .story import StoryService


async def get_story_service(
    http_client_factory: Annotated[HttpClientFactory, Field(...)] = Depends(get_http_client_factory),
) -> AsyncGenerator[StoryService]:
    yield StoryService(
        http_client_factory=http_client_factory,
        neuron_base_url=settings.neuron_base_url,
        neuron_url_expiration=settings.neuron_url_expiration
    )
