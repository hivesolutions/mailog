#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from typing import cast

from appier import route, ensure, NotFoundError

from mailog.models import Activity

from .base import BaseController


class ActivityController(BaseController):
    @route("/activities/<int:activity_id>/report", "GET")
    @ensure(context="admin")
    def report(self, activity_id: int) -> str:
        activity = cast(Activity, Activity.get(id=activity_id, rules=False))
        if activity == None:
            raise NotFoundError(message=f"Activity {activity_id} not found")

        timestamp_s = self._format_timestamp(activity.timestamp)
        sessions = self._format_sessions(activity.sessions or [])
        contents_size_s = self._format_size(getattr(activity, "contents_size", None))

        return self.template(
            "activity/report.html.tpl",
            activity=activity,
            timestamp_s=timestamp_s,
            sessions=sessions,
            contents_size_s=contents_size_s,
        )

    def _format_timestamp(self, timestamp: float | None) -> str:
        if timestamp == None:
            return "-"
        _datetime = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return _datetime.strftime("%B %d, %Y at %H:%M:%S UTC")

    def _format_duration(self, duration: float | None) -> str | None:
        if duration == None:
            return None
        if duration < 1.0:
            return f"{int(duration * 1000)}ms"
        seconds = int(duration)
        millis = int((duration - seconds) * 1000)
        if millis > 0:
            return f"{seconds}s {millis}ms"
        return f"{seconds}s"

    def _format_size(self, size: int | None) -> str | None:
        if size == None or size == 0:
            return None
        if size < 1024:
            return f"{size} B"
        if size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        return f"{size / (1024 * 1024):.1f} MB"

    def _format_cipher(self, cipher: tuple | list | None) -> str | None:
        if cipher == None:
            return None
        if isinstance(cipher, (tuple, list)) and len(cipher) >= 1:
            return str(cipher[0])
        return str(cipher)

    def _format_sessions(self, sessions: list[dict]) -> list[dict]:
        formatted = []
        for session in sessions:
            formatted.append(
                dict(
                    domain=session.get("domain"),
                    host=session.get("host"),
                    port=session.get("port"),
                    mx_host=session.get("mx_host"),
                    greeting=session.get("greeting"),
                    queue_response=session.get("queue_response"),
                    starttls=session.get("starttls", False),
                    tls_version=session.get("tls_version"),
                    tls_cipher=self._format_cipher(session.get("tls_cipher")),
                    start_time_s=self._format_timestamp(session.get("start_time")),
                    end_time_s=self._format_timestamp(session.get("end_time")),
                    duration_s=self._format_duration(session.get("duration")),
                    recipients=session.get("recipients", []),
                    error=session.get("error"),
                )
            )
        return formatted
