<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ activity.subject or "Email Contents" }} - Mailog</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,300;8..60,400;8..60,600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{{ url_for('static', filename='css/contents.css') }}" />
</head>
<body>
    <div class="contents-page">
        <iframe class="contents-frame" src="{{ url_for('activity.contents_html', activity_id=activity.id) }}"></iframe>

        {% if attachments %}
            <div class="contents-attachments">
                <h2 class="contents-attachments-title">Attachments</h2>
                {% for attachment in attachments %}
                    <a class="contents-attachment" href="{{ attachment.url }}">
                        <span class="contents-attachment-icon">&#x1f4ce;</span>
                        <span class="contents-attachment-name">{{ attachment.filename }}</span>
                        <span class="contents-attachment-size">{{ attachment.size_s or "-" }}</span>
                    </a>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
