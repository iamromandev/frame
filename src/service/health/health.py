
from src.client import CacheClient
from src.core.base import BaseService
from src.core.common import get_app_version
from src.core.type import Status
from src.data import get_db_health, get_db_version
from src.data.schema.health import CacheSchema, DatabaseSchema, HealthSchema


class HealthService(BaseService):
    _cache_client: CacheClient

    def __init__(self, cache_client: CacheClient) -> None:
        super().__init__()
        self._cache_client = cache_client



    async def check_health(self) -> HealthSchema:
        app_version = get_app_version()
        db_status = Status.SUCCESS if await get_db_health() else Status.ERROR
        db_version = await get_db_version()
        db_schema = DatabaseSchema(
            status=db_status,
            version=db_version
        )

        cache_status = Status.SUCCESS if await self._cache_client.health() else Status.ERROR
        cache_version = await self._cache_client.get_version()
        cache_schema = CacheSchema(
            status=cache_status,
            version=cache_version
        )
        health: HealthSchema = HealthSchema(
            version=app_version, db=db_schema, cache=cache_schema
        )
        health.log()
        return health
