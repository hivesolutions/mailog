#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import cast

from appier import field, link, not_null

from .base import MailogBase

STATUS_S: dict[str, str] = dict(
    delivered="delivered",
    failed="failed",
)

STATUS_C: dict[str, str] = dict(
    delivered="green",
    failed="red",
)


class Activity(MailogBase):
    timestamp: float = cast(
        float,
        field(type=float, index=True, safe=True),
    )

    sender: str | None = cast(
        None,
        field(type=str, index=True, safe=True, meta="email"),
    )

    recipients: list[str] = cast(
        list[str],
        field(type=list, safe=True),
    )

    subject: str = cast(
        str,
        field(type=str, safe=True),
    )

    status: str = cast(
        str,
        field(
            type=str,
            index=True,
            safe=True,
            meta="enum",
            enum=STATUS_S,
            colors=STATUS_C,
        ),
    )

    message_id: str = cast(
        str,
        field(type=str, index=True, safe=True, description="Message-ID"),
    )

    server: str = cast(
        str,
        field(type=str, index=True, safe=True),
    )

    username: str | None = cast(
        None,
        field(type=str, index=True, safe=True),
    )

    headers: dict = cast(
        dict,
        field(type=dict, safe=True),
    )

    error: str | None = cast(
        None,
        field(type=str, safe=True),
    )

    @classmethod
    def list_names(cls) -> list[str]:
        return ["timestamp", "sender", "subject", "status", "server"]

    @classmethod
    def order_name(cls) -> tuple[str, int]:
        return ("timestamp", -1)

    @classmethod
    def validate(cls) -> list:
        return super(Activity, cls).validate() + [
            not_null("timestamp"),
            not_null("status"),
        ]

    @classmethod
    @link(name="Export CSV")
    def export_url(cls, absolute: bool = False) -> str | None:
        from appier import get_app

        return get_app().url_for(
            "activity_api.export_csv", absolute=absolute
        )
