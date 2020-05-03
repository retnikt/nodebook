import asyncio
import os

import pytest
import starlette.testclient

os.environ["NOTEBOOK_FORCE_ROLLBACK"] = "true"


@pytest.fixture()
def client():
    from notebook import app

    with starlette.testclient.TestClient(app) as client:
        yield client


@pytest.fixture()
def sql():
    """fixture to execute arbitrary SQL statements"""
    from notebook.database import database

    loop = asyncio.get_event_loop()

    def execute(query, **values):
        return loop.run_until_complete(database.execute(query, values or None))

    return execute
