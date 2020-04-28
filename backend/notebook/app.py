"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
from notebook.openapi import API
from notebook.routes import router as api

__all__ = ["app"]

app = API(docs_url=None, redoc_url=None, openapi_url="/api/openapi.json",)

app.add_api_route("/api/", app.redoc_route(), include_in_schema=False)
app.include_router(api, prefix="/api")
