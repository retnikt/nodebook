import time

from fastapi import Depends, HTTPException
from fastapi.openapi.models import OAuthFlowPassword, OAuthFlows
from fastapi.security import OAuth2

import jwt.exceptions  # type: ignore
from notebook import database
from notebook.settings import settings
from starlette.requests import Request

ALGORITHM = "HS256"
ISSUER = "notebook"
AUDIENCE = "notebook"
EXPIRY = 86400

WWW_AUTHENTICATE_HEADERS = {"www-authenticate": "Bearer"}
NO_CACHE_HEADERS = {"cache-control": "no-store", "pragma": "no-cache"}


class JWTScheme(OAuth2):
    """JSON Web Token Authentication Scheme"""

    description = "JSON Web Token Authentication Scheme"

    def __init__(self):
        super(JWTScheme, self).__init__(
            auto_error=False,
            flows=OAuthFlows(password=OAuthFlowPassword(tokenUrl="/api/oauth2/ropcf")),
        )

    async def __call__(self, request: Request):
        header = await super(JWTScheme, self).__call__(request) or ""
        token_type, _, token = header.partition(" ")
        if token_type.casefold() != "bearer" or not token:
            raise HTTPException(
                401, "not authenticated", headers=WWW_AUTHENTICATE_HEADERS
            )
        try:
            return jwt.decode(
                token,
                algorithms=[ALGORITHM],
                key=settings.secret_key,
                issuer=ISSUER,
                audience=AUDIENCE,
            )
        except jwt.exceptions.ExpiredSignatureError as e:
            raise HTTPException(403, "token expired", headers=NO_CACHE_HEADERS) from e
        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(400, str(e), headers=NO_CACHE_HEADERS) from e


oauth2_scheme = JWTScheme()


def create_jwt(form, scope):
    return jwt.encode(  # RFC 7519
        {
            "sub": form.email,
            "iat": (now := time.time()),
            "nbf": now,
            "exp": now + EXPIRY,
            "aud": AUDIENCE,
            "iss": ISSUER,
            "scope": scope,  # RFC 8693.4.2
        },
        key=settings.secret_key,
        algorithm=ALGORITHM,
    ).decode()


def refresh(token: dict):
    token.update({"iat": (now := time.time()), "nbf": now, "exp": now + EXPIRY})
    return jwt.encode(token, key=settings.secret_key, algorithm=ALGORITHM).decode()


def requires(*scopes):
    scopes_set = set(scopes)

    @Depends
    async def dependency(auth: oauth2_scheme = Depends()):
        if scopes_set <= auth["scopes"]:
            raise HTTPException(403, "forbidden")
        return await database.database.execute(
            database.users.select().where(database.users.c.id == auth["sub"])
        )

    return dependency
