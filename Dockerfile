FROM python:3.6-alpine3.7
LABEL maintainer="Igor Nehoroshev <harry@hashdivision.com>"
RUN mkdir -p /clothobserve
COPY requirements.txt /requirements.txt
COPY clothobserve /clothobserve/
WORKDIR /clothobserve
RUN pip3 install -r /requirements.txt

EXPOSE 5000

CMD gunicorn -w 2 -b 0.0.0.0:5000 main:server