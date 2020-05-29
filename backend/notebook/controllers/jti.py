from http.client import HTTPException

from notebook import database


async def check_jti(data: dict):
    # check token is not being replayed
    if await database.database.execute(
        database.jtis.select().where(database.jtis.c.nonce == data["jti"])
    ):
        raise HTTPException(403, "forbidden")
    # save token so it can't be replayed
    await database.database.execute(
        database.jtis.insert().values(nonce=data["jti"], expiry=data["exp"])
    )
