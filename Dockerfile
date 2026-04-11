FROM python:latest

LABEL version="1.0"
LABEL maintainer="Hive Solutions <development@hive.pt>"

EXPOSE 8080

ENV SERVER uvicorn
ENV HOST 0.0.0.0
ENV PORT 8080
ENV MONGOHQ_URL mongodb://localhost
ENV PYTHONPATH /src

ADD requirements.txt /
ADD extra.txt /
ADD src /src

RUN pip install -r /requirements.txt && pip install -r /extra.txt && pip install --upgrade netius uvicorn

RUN useradd -r -s /bin/false mailog
USER mailog

CMD ["/usr/local/bin/python", "/src/mailog/main.py"]
