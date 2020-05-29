from typing import TYPE_CHECKING, Literal

from pydantic import EmailStr as _EmailStr

Ok = Literal["ok"]

if TYPE_CHECKING:
    EmailStr = str
else:
    EmailStr = _EmailStr
