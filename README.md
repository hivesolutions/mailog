# [Mailog](http://mailog.bemisc.com)

SMTP relay activity dashboard powered by [Appier](https://github.com/hivesolutions/appier). Receives delivery status webhooks from [netius](https://github.com/hivesolutions/netius) `ActivityRelaySMTPServer` and provides an admin interface for browsing email activity.

## Features

* Delivery status tracking with per-recipient session details and SMTP transcripts
* TLS negotiation visibility including protocol version and cipher information
* Full email contents storage with raw and HTML viewing modes
* MIME attachment extraction and individual download support
* One-click JSON export of activity data for LLM-assisted analysis
* CSV export for bulk activity reporting
* Webhook authentication via shared secret

## Configuration

| Name                      | Type   | Default     | Description                                                                                     |
| ------------------------- | ------ | ----------- | ----------------------------------------------------------------------------------------------- |
| **MONGOHQ_URL**           | `str`  | `localhost` | MongoDB connection string                                                                       |
| **ACTIVITY_SECRET**       | `str`  | `None`      | Shared secret for webhook authentication (optional)                                             |
| **MAILOG_STORE_CONTENTS** | `bool` | `False`     | If enabled, stores full email contents in MongoDB and exposes raw/HTML view links in the report |
| **SERVER**                | `str`  | `uvicorn`   | ASGI server to use                                                                              |
| **HOST**                  | `str`  | `127.0.0.1` | Bind address                                                                                    |
| **PORT**                  | `int`  | `8080`      | Bind port                                                                                       |

## Netius Integration

Configure the netius `ActivityRelaySMTPServer` to point at this service:

```bash
export SMTP_ACTIVITY_URL=http://localhost:8080/api/activity
export SMTP_ACTIVITY_SECRET=your-shared-secret
```

## Running

```bash
pip install -r requirements.txt
PYTHONPATH=src python -m mailog
```

## License

Mailog is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

