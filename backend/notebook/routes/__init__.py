"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", response_model=str)
async def ping() -> str:
    return "pong!"
