from typing import Optional

from fastapi import APIRouter

import pydantic
from notebook import database
from notebook.controllers.oauth2 import requires
from notebook.utils import Ok
from pydantic import EmailStr

router = APIRouter()


class Profile(pydantic.BaseModel):
    email: str
    name: str


@router.get("/", response_model=Profile)
async def get_profile(user: requires("user/read")):
    """gets the user's profile"""
    return {
        "email": user["email"],
        "name": user["name"],
    }


@router.put("/", response_model=Ok)
async def update_profile(
    user: requires("user/read", "user/write"),
    email: Optional[EmailStr] = None,
    name: Optional[str] = None,
):
    """updates the user's profile"""
    data = {}
    if email is not None:
        data["email"] = email
    if name is not None:
        data["name"] = name
    # if there is nothing to update, don't bother
    if data:
        await database.database.execute(
            (
                database.users.update()
                .where(database.users.c.id == user["id"])
                .values(data)
            )
        )
    return "ok"


@router.delete("/", response_model=Ok)
async def delete_profile(user: requires("user/read", "user/write", "user/delete")):
    """deletes a user account"""
    await database.database.execute(
        database.users.delete().where(database.users.c.id == user["id"])
    )
    return "ok"
