from typing import TYPE_CHECKING, List

from pydantic import AnyHttpUrl, BaseSettings, stricturl

if TYPE_CHECKING:
    _PostgresURL = str
else:
    _PostgresURL = stricturl(
        strip_whitespace=True,
        tld_required=False,
        allowed_schemes={"postgresql", "postgres"},
    )


class _Settings(BaseSettings):
    dsn: _PostgresURL = "postgres://postgresql/notebook"
    cors_origins: List[AnyHttpUrl] = []

    class Config:
        env_prefix: str = "notebook_"


settings = _Settings()
