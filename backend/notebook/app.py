"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
from fastapi import HTTPException
from fastapi.responses import ORJSONResponse

from notebook.openapi import API
from notebook.routes import router as api

__all__ = ["app"]

app = API(docs_url=None, redoc_url=None, openapi_url="/api/openapi.json",)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request, exception: HTTPException):
    """custom handler for HTTPExceptions allowing more flexibility:
    instead of returning { "detail": detail } we just return the detail as JSON
    """
    return ORJSONResponse(
        exception.detail, status_code=exception.status_code, headers=exception.headers
    )


app.add_api_route("/api/", app.redoc_route(), include_in_schema=False)
app.include_router(api, prefix="/api")
