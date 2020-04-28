from databases import Database

from notebook.settings import settings

database = Database(settings.dsn)
