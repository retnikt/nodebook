"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
from databases import Database

from notebook.settings import settings

database = Database(settings.dsn)
