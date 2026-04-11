#!/usr/bin/python
# -*- coding: utf-8 -*-

from appier import conf, route, OperationalError

from mailog.models import Activity

from .root import RootAPIController


class ActivityAPIController(RootAPIController):
    @route("/api/activity", "POST", json=True)
    def create(self) -> dict:
        # validates the shared secret if one is configured,
        # requests without the correct header are rejected
        secret = conf("ACTIVITY_SECRET", None)
        if secret:
            header_secret = self.request.get_header("X-Activity-Secret")
            if header_secret != secret:
                raise OperationalError(message="Invalid secret", code=401)

        activity = Activity.new(safe=True)
        activity.save()
        return activity.map()

    @route("/api/activity/export.csv", "GET")
    def export_csv(self) -> bytes:
        from appier import get_object, legacy

        payload = get_object(alias=True, find=True, limit=0)
        activities: list[Activity] = Activity.find(**payload)
        lines: list[str] = ["timestamp,sender,recipients,subject,status,server,username,message_id,error"]
        for a in activities:
            recipients = ";".join(a.recipients) if a.recipients else ""
            lines.append(
                ",".join(
                    [
                        str(a.timestamp),
                        a.sender or "",
                        recipients,
                        a.subject or "",
                        a.status or "",
                        a.server or "",
                        a.username or "",
                        a.message_id or "",
                        a.error or "",
                    ]
                )
            )
        data = "\n".join(lines)
        self.content_type("text/csv")
        return legacy.bytes(data)
