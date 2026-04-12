#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from typing import cast
from email import message_from_string
from email.policy import default

from appier import conf, route, ensure, legacy, NotFoundError

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

        has_contents = (getattr(activity, "contents_size", None) or 0) > 0
        store_contents = conf("MAILOG_STORE_CONTENTS", False, cast=bool)

        return self.template(
            "activity/report.html.tpl",
            activity=activity,
            timestamp_s=timestamp_s,
            sessions=sessions,
            contents_size_s=contents_size_s,
            has_contents=has_contents,
            store_contents=store_contents,
        )

    @route("/activities/<int:activity_id>/contents/raw", "GET")
    @ensure(context="admin")
    def contents_raw(self, activity_id: int) -> bytes:
        activity = cast(
            Activity,
            Activity.get(id=activity_id, fields=("contents",), rules=False),
        )
        if activity == None:
            raise NotFoundError(message=f"Activity {activity_id} not found")
        contents = activity.contents or ""
        self.content_type("text/plain; charset=utf-8")
        return legacy.bytes(contents, encoding="utf-8")

    @route("/activities/<int:activity_id>/contents/html", "GET")
    @ensure(context="admin")
    def contents_html(self, activity_id: int) -> str:
        activity = cast(
            Activity,
            Activity.get(
                id=activity_id, fields=("id", "subject", "contents"), rules=False
            ),
        )
        if activity == None:
            raise NotFoundError(message=f"Activity {activity_id} not found")
        contents = activity.contents or ""
        attachments = self._extract_attachments(contents, activity_id)
        return self.template(
            "activity/contents.html.tpl",
            activity=activity,
            attachments=attachments,
        )

    @route("/activities/<int:activity_id>/contents/body", "GET")
    @ensure(context="admin")
    def contents_body(self, activity_id: int) -> bytes:
        activity = cast(
            Activity,
            Activity.get(id=activity_id, fields=("contents",), rules=False),
        )
        if activity == None:
            raise NotFoundError(message=f"Activity {activity_id} not found")
        contents = activity.contents or ""
        html = self._extract_html(contents)
        self.content_type("text/html; charset=utf-8")
        return legacy.bytes(html, encoding="utf-8")

    @route("/activities/<int:activity_id>/attachments/<int:index>", "GET")
    @ensure(context="admin")
    def attachment(self, activity_id: int, index: int) -> bytes:
        activity = cast(
            Activity,
            Activity.get(id=activity_id, fields=("contents",), rules=False),
        )
        if activity == None:
            raise NotFoundError(message=f"Activity {activity_id} not found")
        contents = activity.contents or ""
        attachments = self._extract_attachments(contents, activity_id)
        if index < 0 or index >= len(attachments):
            raise NotFoundError(message=f"Attachment {index} not found")
        attachment = attachments[index]
        data = attachment["data"]
        self.content_type(attachment["content_type"])
        self.request.set_header(
            "Content-Disposition",
            f"attachment; filename=\"{attachment['filename']}\"",
        )
        return data

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
                    transcript=self._format_transcript(session.get("transcript", [])),
                )
            )
        return formatted

    def _format_transcript(self, transcript: list[dict]) -> list[dict]:
        # groups consecutive entries with the same direction into
        # blocks so that the arrow is only shown once per group
        groups: list[dict] = []
        for entry in transcript:
            direction = entry.get("direction")
            timestamp = entry.get("timestamp")
            timestamp_s = self._format_timestamp_ms(timestamp)
            line = dict(message=entry.get("message"), timestamp_s=timestamp_s)
            if groups and groups[-1]["direction"] == direction:
                groups[-1]["lines"].append(line)
            else:
                groups.append(dict(direction=direction, lines=[line]))
        return groups

    def _format_timestamp_ms(self, timestamp: float | None) -> str:
        if timestamp == None:
            return "-"
        _datetime = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return _datetime.strftime("%H:%M:%S.") + "%03d" % (
            _datetime.microsecond // 1000
        )

    def _extract_html(self, contents: str) -> str:
        # extracts the HTML body from raw email contents by
        # parsing as a MIME message and returning the first
        # text/html part, falls back to the raw body if no
        # HTML part is found
        try:
            message = message_from_string(contents, policy=default)
            if message.is_multipart():
                for part in message.walk():
                    if not part.get_content_type() == "text/html":
                        continue
                    return part.get_content()
            elif message.get_content_type() == "text/html":
                return message.get_content()
            return message.get_content()
        except Exception:
            # falls back to extracting the body after the
            # first blank line (end of headers)
            parts = contents.split("\r\n\r\n", 1)
            if len(parts) > 1:
                return parts[1]
            return contents

    def _extract_attachments(self, contents: str, activity_id: int) -> list[dict]:
        # extracts attachment metadata and data from the raw
        # MIME contents, skipping inline text parts
        attachments: list[dict] = []
        try:
            message = message_from_string(contents, policy=default)
            if not message.is_multipart():
                return attachments
            index = 0
            for part in message.walk():
                disposition = part.get_content_disposition()
                if not disposition == "attachment":
                    continue
                filename = part.get_filename() or f"attachment-{index}"
                content_type = part.get_content_type()
                data = part.get_payload(decode=True) or b""
                attachments.append(
                    dict(
                        index=index,
                        filename=filename,
                        content_type=content_type,
                        size=len(data),
                        size_s=self._format_size(len(data)),
                        data=data,
                        url=self.owner.url_for(
                            "activity.attachment",
                            activity_id=activity_id,
                            index=index,
                        ),
                    )
                )
                index += 1
        except Exception:
            pass
        return attachments
