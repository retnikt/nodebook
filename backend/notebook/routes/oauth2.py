"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
import time
from typing import Literal

import argon2  # type: ignore
import jwt.exceptions  # type: ignore
import pydantic
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.openapi.models import OAuthFlowPassword, OAuthFlows
from fastapi.responses import ORJSONResponse
from fastapi.security.oauth2 import OAuth2

from notebook.settings import settings

ALGORITHM = "HS256"

ISSUER = "notebook"
AUDIENCE = "notebook"

WWW_AUTHENTICATE_HEADERS = {"www-authenticate": "bearer"}

router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer("/api/oauth2/ropcf")


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
                403, "not authenticated", headers=WWW_AUTHENTICATE_HEADERS
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
            raise HTTPException(
                403, "token expired", headers=WWW_AUTHENTICATE_HEADERS
            ) from e
        except jwt.exceptions.PyJWTError as e:
            raise HTTPException(400, str(e), headers=WWW_AUTHENTICATE_HEADERS) from e


oauth2_scheme = JWTScheme()


password_hasher = argon2.PasswordHasher()

EMAIL = "admin@example.com"
PASSWORD = password_hasher.hash("hunter2")
EXPIRY = 86400

EXAMPLE_JWT = jwt.encode(
    {
        "sub": "user@example.com",
        "iat": (now := time.time()),
        "nbf": now,
        "exp": now + EXPIRY,
        "aud": "example_audience",
        "iss": "example_issuer",
        "scope": ["user/read", "user/write"],
    },
    "example_key",
).decode()
del now


class OAuth2ROPCFSuccessResponse(pydantic.BaseModel):
    """models a successful response to an OAuth2 Resource Owner Password Credentials Flow request"""

    access_token: str = pydantic.Field(
        example=EXAMPLE_JWT,
        description="JWT-encoded access token (see [RFC 7519](https://tools.ietf.org/html/rfc7519))",
    )
    expires_in: int = pydantic.Field(
        example=86400,
        description="seconds until the token expires (note, however, that the JWT's `exp` field is the canonical source of truth)",
    )
    token_type: Literal["bearer"] = pydantic.Field(
        example="bearer",
        description="the type of the token as described in [RFC 6749.7.1](https://tools.ietf.org/html/rfc6749#section-7.1) (always Bearer)",
    )
    scope: str = pydantic.Field(
        example="user/read user/write",
        description="space-separated list of OAuth2 scopes granted for this token",
    )


class OAuth2ROPCFInvalidResponse(pydantic.BaseModel):
    """models an unsuccessful response to an OAuth2 Resource Owner Password Credentials Flow request due to a malformed request"""

    error: str = pydantic.Field(
        description="indicates the type of error as described in [RFC 6749.5.2](https://tools.ietf.org/html/rfc6749#section-5.2)",
        example="invalid_request",
    )
    error_description: str = pydantic.Field(
        description="provides a short human-readable explanation of the error",
        example="only grant_type of 'password' is supported",
    )


class OAuth2ROPCFIncorrectResponse(pydantic.BaseModel):
    """models an unsuccessful response to an OAuth2 Resource Owner Password Credentials Flow request due to incorrect or invalid credentials"""

    error: str = pydantic.Field(
        description="indicates the type of error as described in [RFC 6749.5.2](https://tools.ietf.org/html/rfc6749#section-5.2)",
        example="invalid_grant",
    )
    error_description: str = pydantic.Field(
        description="provides a short human-readable explanation of the error",
        example="incorrect email address or password",
    )


class OAuth2ROPCFForm(pydantic.BaseModel):
    # form.username has to be called "username" (per RFC 6749.4.3.2) but it actually
    # contains an email address in this case. don't bother validating it as an EmailStr
    # though because it just needs to be looked up in the database
    email: str = pydantic.Field(
        alias="username",
        description="the email address to of the account (called username per [RFC 6749.4.3.2](https://tools.ietf.org/html/rfc6749#section-4.3.2))",
        example="user@example.com",
    )
    password: str = pydantic.Field(
        description="the password to log in to the account", example="hunter2"
    )
    grant_type: str = pydantic.Field(
        description="the OAuth2 grant type. Currently only 'password' is supported",
        example="password",
    )


@Depends
async def oauth_2_ropcf_form(request: Request) -> OAuth2ROPCFForm:
    try:
        form = OAuth2ROPCFForm.parse_obj(await request.form())
    except pydantic.ValidationError as e:
        raise HTTPException(
            400,
            {  # RFC 6749.5.2
                "error": "invalid_request",
                "error_description": "request must include username, password",
            },
        ) from e
    if form.grant_type != "password":
        raise HTTPException(
            400,
            {
                "error": "unsupported_grant",
                "error_description": "only grant_type of 'password' is supported",
            },
        )
    return form


@router.post(
    "/ropcf",
    summary="OAuth2 Resource Owner Password Credentials Flow",
    responses={
        400: {
            "description": "Unsuccessful response per [RFC 6749.5.2](https://tools.ietf.org/html/rfc6749#section-5.2) (invalid request, scope, or grant type)",
            "model": OAuth2ROPCFInvalidResponse,
        },
        401: {
            "description": "Unsuccessful response per [RFC 6749.5.2](https://tools.ietf.org/html/rfc6749#section-5.2) (incorrect email/password or unauthorized client)",
            "model": OAuth2ROPCFIncorrectResponse,
        },
    },
    response_model=OAuth2ROPCFSuccessResponse,
    response_description="Successful response per [RFC 6749.5.1](https://tools.ietf.org/html/rfc6749#section-5.1)",
    tags=["OAuth2"],
)
async def ropcf(request: Request, form: OAuth2ROPCFForm = oauth_2_ropcf_form):
    """Implements OAuth 2 Resource Owner Password Credentials Flow, per RFC 6749.4.3"""

    # limit access to only specifically allowed origins
    # note that this security feature only works on websites - outside a browser, this
    # can be easily bypassed
    origin = request.headers.get("Origin")
    if not origin or origin not in settings.rocpf_origins:
        raise HTTPException(
            401,
            {
                "error": "invalid_client",
                "error_description": "this origin is not allowed to perform the ROPCF authentication flow",
            },
        )

    if form.email != EMAIL:
        raise HTTPException(
            401,
            {
                "error": "invalid_grant",
                "error_description": "incorrect email address or password",
            },
        )

    try:
        password_hasher.verify(hash=PASSWORD, password=form.password)
    except argon2.exceptions.VerifyMismatchError as e:
        raise HTTPException(
            401,
            {
                "error": "invalid_grant",
                "error_description": "incorrect email address or password",
            },
        ) from e

    scope = ["user/read", "user/write"]
    return ORJSONResponse(
        {  # RFC 6749.5.1
            "access_token": jwt.encode(  # RFC 7519
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
            ).decode(),
            "token_type": "bearer",
            "scope": " ".join(scope),  # RFC 6749.3.3
            "expires_in": EXPIRY,
        },
        headers={"cache-control": "no-store", "pragma": "no-cache"},
    )


@router.post("/refresh", response_model=OAuth2ROPCFSuccessResponse, tags=["OAuth2"])
async def refresh_token(token=Depends(oauth2_scheme)):
    token.update({"iat": (now := time.time()), "nbf": now, "exp": now + EXPIRY})
    return {
        "access_token": jwt.encode(
            token, key=settings.secret_key, algorithm=ALGORITHM
        ).decode(),
        "token_type": "bearer",
        "scope": " ".join(token["scope"]),
        "expires_in": EXPIRY,
    }
