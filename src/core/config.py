from typing import Annotated
from urllib.parse import quote_plus

from pydantic import Field, HttpUrl, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .type import Env


class Settings(BaseSettings):
    # core
    env: Annotated[Env, Field(description="Application environment")]
    debug: Annotated[bool, Field(description="Enable debug mode")]
    # db
    db_schema: Annotated[str, Field(description="Database schema")]
    db_host: Annotated[str, Field(description="Database host")]
    db_port: Annotated[int, Field(description="Database port")]
    db_name: Annotated[str, Field(description="Database name")]
    db_user: Annotated[str, Field(description="Database user")]
    db_password: Annotated[str, Field(description="Database password")]
    db_root_password: Annotated[str, Field(description="Root database password")]
    # cache
    cache_schema: Annotated[str, Field(description="Cache schema")]
    cache_host: Annotated[str, Field(description="Cache host")]
    cache_port: Annotated[int, Field(description="Cache port")]
    cache_user: Annotated[str, Field(description="Cache user")]
    cache_password: Annotated[str, Field(description="Cache password")]
    # http
    http_timeout: Annotated[float, Field(description="HTTP timeout")]
    # neuron
    neuron_server_schema: Annotated[str, Field(description="Neuron server schema")]
    neuron_server_host: Annotated[str, Field(description="Neuron server host")]
    neuron_server_port: Annotated[int, Field(description="Neuron server port")]
    neuron_url_expiration: Annotated[int, Field(description="URL expiration time (seconds)")]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )

    @property
    def is_local(self) -> bool:
        return self.env == Env.LOCAL

    @property
    def is_prod(self) -> bool:
        return self.env == Env.PROD

    @property
    def db_url(self) -> str:
        return f"{self.db_schema}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def cache_url(self) -> RedisDsn:
        if self.is_local:
            return RedisDsn.build(
                scheme=self.cache_schema,
                host=self.cache_host,
                port=self.cache_port,
            )
        return RedisDsn.build(
            scheme=self.cache_schema,
            host=self.cache_host,
            port=self.cache_port,
            username=self.cache_user,
            password=quote_plus(self.cache_password),
        )

    @property
    def neuron_base_url(self) -> HttpUrl:
        return HttpUrl.build(
            scheme=self.neuron_server_schema,
            host=self.neuron_server_host,
            port=self.neuron_server_port,
        )


settings = Settings()
