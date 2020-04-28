"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
from functools import cached_property
from typing import Callable, Coroutine, Dict

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from notebook.constants import LICENCE, NAME, URL, VERSION

__all__ = ["API"]

HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>API Documentation - Notebook</title>
  <script src="https://cdn.jsdelivr.net/npm/redoc@2.0.0-rc.28/bundles/redoc.standalone\
.js" async defer crossorigin="anonymous" integrity="sha384-LhHSAPejpYDxPlv2AvXUAB8wYS\
+GbKLTCZNIp+a+f3NA7FATjmJJSv5QIpudxKax"></script>
  <style>
    body { margin: 0; padding: 0; }
  </style>
</head>
<body>
  <noscript>
    Sorry, the API Documentation doesn't work without JavaScript. Please enable it, or
    use the <a href="openapi.json">OpenAPI</a> description directly.
  </noscript>
  <redoc spec-url="openapi.json"></redoc>
</body>
</html>
"""
LOGO_URL: str = "https://raw.githubusercontent.com/retnikt/notebook/master/logo.svg"
DESCRIPTION: str = """\
Notebook API
"""


class API(FastAPI):
    @cached_property
    def _openapi(self) -> Dict:
        openapi = super(API, self).openapi()
        openapi["info"].update(
            {
                "title": NAME,
                "description": DESCRIPTION,
                "version": VERSION,
                "x-logo": {"url": LOGO_URL, "altText": NAME, "href": URL},
                "license": LICENCE,
            }
        )
        return openapi

    def openapi(self) -> Dict:
        return self._openapi

    def redoc_route(self) -> Callable[[], Coroutine[None, None, HTMLResponse]]:
        response = HTMLResponse(HTML)

        async def redoc() -> HTMLResponse:
            return response

        return redoc
