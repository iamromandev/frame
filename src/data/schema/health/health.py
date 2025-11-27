from typing import Annotated

from pydantic import Field

from src.core.base import BaseSchema
from src.core.type import Status


class DatabaseSchema(BaseSchema):
    status: Annotated[Status, Field(default=Status.ERROR)]
    version: Annotated[str | None, Field(default=None)]


class CacheSchema(BaseSchema):
    status: Annotated[Status, Field(default=Status.ERROR)]
    version: Annotated[str | None, Field(default=None)]


class HealthSchema(BaseSchema):
    version: Annotated[str, Field(default="0.0.1", description="Application version")]
    db: Annotated[DatabaseSchema, Field(default=None)]
    cache: Annotated[CacheSchema, Field(default=None)]
