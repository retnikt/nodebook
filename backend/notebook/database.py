"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
import sqlalchemy
from databases import Database

from notebook.settings import settings

metadata = sqlalchemy.MetaData()
database = Database(settings.dsn)
