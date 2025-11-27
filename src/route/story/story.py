from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.core.success import Success
from src.data.schema.health import HealthSchema
from src.service.story import StoryService, get_story_service

router = APIRouter(prefix="/story", tags=["Story"])


@router.get(
    path="/generate",
    response_model=Success[HealthSchema],
)
async def generate(
    service: Annotated[StoryService, Depends(get_story_service)]
) -> JSONResponse:
    output = await service.generate_story()
    return Success.ok(data=output).to_resp()
