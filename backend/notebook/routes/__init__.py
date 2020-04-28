from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", response_model=str)
async def ping() -> str:
    return "pong!"
