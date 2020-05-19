"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
import asyncio

import argon2  # type: ignore
from fastapi import HTTPException

from notebook import database
from notebook.settings import settings

password_hasher = argon2.PasswordHasher(
    time_cost=settings.argon2_time_cost,
    memory_cost=settings.argon2_memory_cost,
    parallelism=settings.argon2_parallelism,
)


async def check_password(user, password):
    try:
        password_hasher.verify(user["password"], password)
    except argon2.exceptions.VerifyMismatchError:
        return False
    asyncio.create_task(rehash_password(user, password))
    return True


async def rehash_password(user, password):
    if password_hasher.check_needs_rehash(user["password"]):
        new_hash = password_hasher.hash(password)
        query = (
            database.users.update()
            .where(database.users.c.id == user["id"])
            .values(password=new_hash)
        )
        await database.database.execute(query)


def check_password_strength(password):
    # TODO better password strength requirements
    return len(password) >= 10


def change_password(password, user_id):
    assert len(password) <= 80
    hashed = password_hasher.hash(password)
    await database.database.execute(
        database.users.update()
        .where(database.users.c.id == user_id)
        .values(password=hashed)
    )
