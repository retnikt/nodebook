import os

import pytest
import starlette.testclient

os.environ["NOTEBOOK_FORCE_ROLLBACK"] = "true"


@pytest.fixture()
def client():
    from notebook import app

    with starlette.testclient.TestClient(app) as client:
        yield client
