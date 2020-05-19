from email.mime.multipart import MIMEMultipart
from unittest.mock import MagicMock

import notebook.email
import pytest


def async_(f):
    async def inner(*args, **kwargs):
        return f(*args, **kwargs)

    return inner


@pytest.mark.asyncio
async def test(monkeypatch):
    mime_multipart = MagicMock(spec=MIMEMultipart)
    mime_multipart.return_value = mime_multipart
    send_message = MagicMock()
    monkeypatch.setattr(notebook.email.smtp, "send_message", async_(send_message))
    monkeypatch.setattr(notebook.email, "MIMEMultipart", mime_multipart)

    await notebook.email.send_message("example@example.invald", "test", "test")
    send_message.assert_called_with(mime_multipart)
