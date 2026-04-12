#!/usr/bin/python
# -*- coding: utf-8 -*-

from mailog import MailogApp, Activity


def test_app_boot() -> None:
    app = MailogApp()
    assert app is not None
    assert app._version() == "0.5.1"


def test_activity_model() -> None:
    assert Activity.list_names() == [
        "timestamp",
        "sender",
        "subject",
        "status",
        "server",
    ]
    assert Activity.order_name() == ("timestamp", -1)
