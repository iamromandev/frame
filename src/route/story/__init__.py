from fastapi import APIRouter

from .story import router as _story_router

_subrouters = [
    _story_router,
]

router = APIRouter()

for subrouter in _subrouters:
    router.include_router(subrouter)
