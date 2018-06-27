FROM python:3.6-alpine3.7
LABEL maintainer="Igor Nehoroshev <harry@hashdivision.com>"
RUN mkdir -p /clothobserve /tests /docs
COPY requirements.txt /requirements.txt
COPY clothobserve /clothobserve/
COPY tests /tests/
WORKDIR /clothobserve
RUN apk add --update alpine-sdk
RUN pip3 install -r /requirements.txt

EXPOSE 5000

CMD sleep 20 && coverage run --source=/clothobserve --omit=/clothobserve/ui/* -m unittest discover -v -s /tests/ && coverage report -m && sphinx-apidoc -f -o /docs/source/ /clothobserve/ /clothobserve/ui && cd /docs && make html && cd /clothobserve && pylint --generated-members=id,objects,StringField,DateTimeField,BooleanField,ReferenceField,ListField,IntField main.py configs core utils modules