<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ activity.subject or "Delivery Report" }} - Mailog</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,300;8..60,400;8..60,600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{{ url_for('static', filename='css/report.css') }}" />
</head>
<body>
    <div class="report">
        <header class="report-header">
            <div class="report-status report-status-{{ activity.status }}">
                {{ activity.status }}
            </div>
            <h1 class="report-subject">{{ activity.subject or "(no subject)" }}</h1>
            <div class="report-timestamp">{{ timestamp_s }}</div>
        </header>

        {% if activity.error %}
            <div class="report-error">
                <div class="report-error-title">Delivery Error</div>
                <div class="report-error-message">{{ activity.error }}</div>
            </div>
        {% endif %}

        <section class="report-section">
            <h2 class="report-section-title">Message</h2>
            <dl class="report-dl">
                <dt class="report-dt">From</dt>
                <dd class="report-dd">{{ activity.sender or "-" }}</dd>
                <dt class="report-dt">Message-ID</dt>
                <dd class="report-dd report-dd-mono">{{ activity.message_id or "-" }}</dd>
                <dt class="report-dt">Relay Server</dt>
                <dd class="report-dd report-dd-mono">{{ activity.server or "-" }}</dd>
                {% if activity.server_agent %}
                    <dt class="report-dt">Server Agent</dt>
                    <dd class="report-dd report-dd-mono">{{ activity.server_agent }}</dd>
                {% endif %}
                {% if activity.username %}
                    <dt class="report-dt">Auth User</dt>
                    <dd class="report-dd report-dd-mono">{{ activity.username }}</dd>
                {% endif %}
                {% if contents_size_s %}
                    <dt class="report-dt">Contents Size</dt>
                    <dd class="report-dd report-dd-mono">{{ contents_size_s }}</dd>
                {% endif %}
            </dl>
        </section>

        <section class="report-section">
            <h2 class="report-section-title">Recipients</h2>
            <ul class="report-recipients">
                {% for recipient in activity.recipients or [] %}
                    <li>{{ recipient }}</li>
                {% endfor %}
            </ul>
        </section>

        {% if sessions %}
            <section class="report-section">
                <h2 class="report-section-title">Delivery Sessions</h2>
                {% for session in sessions %}
                    <div class="report-session">
                        <div class="report-session-header">
                            <span class="report-session-domain">{{ session.domain or "direct" }}</span>
                            {% if session.tls_version %}
                                {% if "1.3" in session.tls_version %}
                                    <span class="report-tls report-tls-13">
                                        <span class="report-tls-lock">&#x1f512;</span> {{ session.tls_version }}
                                    </span>
                                {% elif "1.2" in session.tls_version %}
                                    <span class="report-tls report-tls-12">
                                        <span class="report-tls-lock">&#x1f512;</span> {{ session.tls_version }}
                                    </span>
                                {% else %}
                                    <span class="report-tls report-tls-12">
                                        <span class="report-tls-lock">&#x1f512;</span> {{ session.tls_version }}
                                    </span>
                                {% endif %}
                            {% elif not session.starttls %}
                                <span class="report-tls report-tls-none">
                                    <span class="report-tls-lock">&#x1f513;</span> No TLS
                                </span>
                            {% endif %}
                            {% if session.duration_s %}
                                <span class="report-session-duration">{{ session.duration_s }}</span>
                            {% endif %}
                        </div>

                        <dl class="report-dl">
                            <dt class="report-dt">Host</dt>
                            <dd class="report-dd report-dd-mono">{{ session.host or "-" }}:{{ session.port or "-" }}</dd>
                            {% if session.mx_host %}
                                <dt class="report-dt">MX Record</dt>
                                <dd class="report-dd report-dd-mono">{{ session.mx_host }}</dd>
                            {% endif %}
                            {% if session.tls_cipher %}
                                <dt class="report-dt">Cipher</dt>
                                <dd class="report-dd report-dd-mono">{{ session.tls_cipher }}</dd>
                            {% endif %}
                            <dt class="report-dt">Started</dt>
                            <dd class="report-dd report-dd-mono">{{ session.start_time_s }}</dd>
                            <dt class="report-dt">Finished</dt>
                            <dd class="report-dd report-dd-mono">{{ session.end_time_s }}</dd>
                            <dt class="report-dt">Recipients</dt>
                            <dd class="report-dd">{{ ", ".join(session.recipients or []) }}</dd>
                        </dl>

                        {% if session.capabilities %}
                            <div class="report-capabilities">
                                {% for cap in session.capabilities %}
                                    <span class="report-capability">{{ cap }}</span>
                                {% endfor %}
                            </div>
                        {% endif %}

                        {% if session.greeting %}
                            <div class="report-server-response" title="Server greeting (220 banner)">
                                220 {{ session.greeting }}
                            </div>
                        {% endif %}
                        {% if session.queue_response %}
                            <div class="report-server-response" title="Queue confirmation (250 response)">
                                250 {{ session.queue_response }}
                            </div>
                        {% endif %}
                        {% if session.error %}
                            <div class="report-session-error">{{ session.error }}</div>
                        {% endif %}
                    </div>
                {% endfor %}
            </section>
        {% endif %}

        <footer class="report-footer">
            Mailog Delivery Report
        </footer>
    </div>
</body>
</html>
