import secrets
import time

from fastapi import APIRouter, HTTPException

import jwt
from notebook import database
from notebook.controllers.oauth2 import AUDIENCE, ISSUER, requires
from notebook.controllers.passwords import change_password, check_password_strength
from notebook.email import send_message
from notebook.settings import settings
from notebook.utils import Ok
from starlette.requests import Request

EXPIRY = 86400  # 24 hours
router = APIRouter()


@router.put("/", response_model=Ok)
async def change(
    password: str, user=requires("user/read", "user/write", "user/password")
):
    """changes the user's password"""

    if not check_password_strength(password):
        raise HTTPException(422, "password not long enough (min=10)")
    if len(password) > 80:
        raise HTTPException(422, "password too long (max=60)")

    await change_password(password, user["id"])
    return "ok"


@router.post("/forgot", response_model=Ok)
async def forgot(email: str, request: Request):
    """sends an email to reset a forgotten password"""
    if user := await database.database.execute(
        database.users.select().where(database.users.c.email == email)
    ):
        token = jwt.encode(
            {
                "sub": user["id"],
                "iss": ISSUER,
                "aud": AUDIENCE,
                "iat": (now := time.time()),
                "nbf": now,
                "exp": now + EXPIRY,
                "jti": secrets.token_bytes(32),
                "scope": "user/password_reset",
            },
            algorithm="HS256",
            key=settings.secret_key,
        ).decode()
        url = (
            f"{request.url.scheme}://{request.url.netloc}/password/reset?token={token}"
        )
        await send_message(
            email, "Rest your Password", "reset_forgotten", email=email, url=url
        )
    return "ok"


@router.post("/reset", response_model=Ok)
async def reset(token: str, password: str):
    try:
        data = jwt.decode(token, algorithms=[], key=settings.secret_key)
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(403, "expired token") from e
    except jwt.DecodeError as e:
        raise HTTPException(422, "invalid token") from e

    if data["scope"] != ["user/password_reset"]:
        raise HTTPException(403, "forbidden")

    if not check_password_strength(password):
        raise HTTPException(422, "password not long enough (min=10)")
    if len(password) > 80:
        raise HTTPException(422, "password too long (max=60)")

    return await change_password(password=password, user_id=data["sub"])
