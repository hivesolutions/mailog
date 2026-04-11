#!/usr/bin/python
# -*- coding: utf-8 -*-

from appier import Controller, route


class BaseController(Controller):
    @route("/", "GET")
    def index(self):
        return self.redirect(self.url_for("admin.index"))
