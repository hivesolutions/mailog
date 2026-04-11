#!/usr/bin/python
# -*- coding: utf-8 -*-

from .main import MailogApp

if __name__ == "__main__":
    app = MailogApp()
    app.serve()
else:
    __path__: list[str] = []
