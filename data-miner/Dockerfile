FROM alpine:3.3
MAINTAINER adam.baird@gmail.com
RUN apk update && \
    apk upgrade && \
    apk add curl python ca-certificates supervisor && \
    rm -rf /var/cache/apk/* && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python
RUN pip install gunicorn json-logging-py supervisor-stdout
COPY ./supervisord.conf /etc/supervisord.conf
WORKDIR /usr/src/app
CMD supervisord -c /etc/supervisord.conf -n
