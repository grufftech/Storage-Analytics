FROM python:alpine
MAINTAINER adam.baird@gmail.com
RUN apk --update  add cifs-utils
ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
COPY . /usr/src/app
WORKDIR /usr/src/app
CMD "python /usr/src/app/miner.py ~"
