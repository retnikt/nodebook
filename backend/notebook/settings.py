"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
import secrets
from typing import TYPE_CHECKING, List, Union

from pydantic import AnyHttpUrl, BaseSettings, Field, stricturl
from argon2 import (
    DEFAULT_TIME_COST,
    DEFAULT_MEMORY_COST,
    DEFAULT_PARALLELISM,
)

if TYPE_CHECKING:
    _PostgresURL = str
else:
    _PostgresURL = stricturl(
        strip_whitespace=True, tld_required=False, allowed_schemes={"postgresql"},
    )


class _UniversalSet:
    """(psuedo)-universal set - contains everything"""

    def __contains__(self, item):
        return True


UNIVERSAL_SET = _UniversalSet()


class _Settings(BaseSettings):
    dsn: _PostgresURL = "postgresql://db/notebook"
    cors_origins: List[AnyHttpUrl] = []
    rocpf_origins: Union[_UniversalSet, List[str]] = Field(UNIVERSAL_SET)
    secret_key: str = secrets.token_urlsafe(40)
    argon2_time_cost: int = DEFAULT_TIME_COST
    argon2_memory_cost: int = DEFAULT_MEMORY_COST
    argon2_parallelism: int = DEFAULT_PARALLELISM
    force_rollback: bool = False

    class Config:
        env_prefix: str = "notebook_"


settings = _Settings()
