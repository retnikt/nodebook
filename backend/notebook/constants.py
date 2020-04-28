"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
from typing import TypedDict, cast

__all__ = ["NAME", "VERSION", "URL", "LICENCE", "LICENSE"]


class _Licence(TypedDict):
    name: str
    url: str


class _Author(TypedDict):
    name: str
    url: str
    email: str


NAME: str = "Notebook"
VERSION: str = "0.1.0"
URL: str = "https://github.com/retnikt/notebook#readme"
LICENCE: _Licence = {
    "name": "MIT",
    "url": "https://opensource.org/licenses/mit-license.html",
}


class _MisspeltLicence:
    """descriptor to teach 330 million people how to spell licence."""

    def __get__(self, instance, owner) -> str:
        raise SyntaxError("learn to spell!")


LICENSE: str = cast(str, _MisspeltLicence())
