"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
import sqlalchemy
from databases import Database
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from notebook.settings import settings

metadata = sqlalchemy.MetaData()
database = Database(settings.dsn, force_rollback=settings.force_rollback)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id", UUID(False), primary_key=True, server_default=text("uuid_generate_v4()")
    ),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String, nullable=False, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
)

jtis = sqlalchemy.Table(
    "jtis",
    metadata,
    sqlalchemy.Column("jti", sqlalchemy.String, nullable=False, primary_key=True),
    sqlalchemy.Column("expiry", sqlalchemy.DateTime, nullable=False),
)
