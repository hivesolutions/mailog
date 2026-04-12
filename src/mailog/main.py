#!/usr/bin/python
# -*- coding: utf-8 -*-

from appier import WebApp
from appier_extras import AdminPart


class MailogApp(WebApp):
    def __init__(self, *args, **kwargs):
        WebApp.__init__(self, name="mailog", parts=(AdminPart,), *args, **kwargs)

    def _version(self) -> str:
        return "0.5.1"

    def _description(self) -> str:
        return "Mailog"

    def _observations(self) -> str:
        return "SMTP relay activity dashboard"


if __name__ == "__main__":
    app = MailogApp()
    app.serve()
else:
    __path__: list[str] = []
