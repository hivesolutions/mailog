#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import cast

from appier import field, get_app, link, not_null

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
        field(
            type=float,
            index=True,
            safe=True,
            meta="datetime",
            observations="UTC epoch when the relay event occurred",
        ),
    )

    sender: str | None = cast(
        None,
        field(
            type=str,
            index=True,
            safe=True,
            meta="email",
            observations="Envelope sender (MAIL FROM) address",
        ),
    )

    recipients: list[str] = cast(
        list[str],
        field(
            type=list,
            safe=True,
            observations="Envelope recipients (RCPT TO) addresses",
        ),
    )

    subject: str = cast(
        str,
        field(
            type=str,
            safe=True,
            observations="Email subject line from the message header",
        ),
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
            observations="Overall delivery outcome (delivered or failed)",
        ),
    )

    message_id: str = cast(
        str,
        field(
            type=str,
            index=True,
            safe=True,
            description="Message-ID",
            observations="RFC 2822 Message-ID header value",
        ),
    )

    server: str = cast(
        str,
        field(
            type=str,
            index=True,
            safe=True,
            observations="SMTP relay server that processed the message",
        ),
    )

    server_agent: str | None = cast(
        None,
        field(
            type=str,
            safe=True,
            observations="Relay server agent string (eg: netius/1.42.0)",
        ),
    )

    username: str | None = cast(
        None,
        field(
            type=str,
            index=True,
            safe=True,
            observations="SMTP AUTH username used for relay authentication",
        ),
    )

    headers: dict = cast(
        dict,
        field(
            type=dict,
            safe=True,
            observations="Raw email headers as key-value pairs",
        ),
    )

    sessions: list[dict] = cast(
        list[dict],
        field(
            type=list,
            safe=True,
            description="Delivery Sessions",
            observations="Per-domain SMTP session deliverability info",
        ),
    )

    contents_size: int = cast(
        int,
        field(
            type=int,
            safe=True,
            observations="Message contents size in bytes",
        ),
    )

    error: str | None = cast(
        None,
        field(
            type=str,
            safe=True,
            observations="SMTP error or bounce reason when delivery fails",
        ),
    )

    @classmethod
    def _plural(cls) -> str:
        return "Activities"

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

    @link(name="View Report")
    def report_url(self, absolute: bool = False) -> str | None:
        return get_app().url_for(
            "activity.report", activity_id=self.id, absolute=absolute
        )

    @classmethod
    @link(name="Export CSV")
    def export_url(cls, absolute: bool = False) -> str | None:
        return get_app().url_for("activity_api.export_csv", absolute=absolute)
