#!/usr/bin/python
# -*- coding: utf-8 -*-

from appier import Controller, route


class RootAPIController(Controller):
    @route("/api/status", "GET", json=True)
    def status(self) -> dict:
        return dict(status="ok")
