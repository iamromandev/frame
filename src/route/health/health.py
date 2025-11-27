from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.core.success import Success
from src.data.schema.health import HealthSchema
from src.service.health import HealthService, get_health_service

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    path="/check",
    response_model=Success[HealthSchema],
)
async def check(
    service: Annotated[HealthService, Depends(get_health_service)]
) -> JSONResponse:
    output: HealthSchema = await service.check_health()
    return Success.ok(data=output).to_resp()
