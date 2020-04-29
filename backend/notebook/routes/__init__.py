"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
from fastapi import APIRouter

from .oauth2 import router as auth

router = APIRouter()
router.include_router(auth, prefix="/oauth2")


@router.get("/ping", response_model=str)
async def ping() -> str:
    return "pong!"
