FROM python:alpine
MAINTAINER adam.baird@gmail.com
RUN apk --update add cifs-utils curl
ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN pip3 install pipreqs
COPY . /usr/src/app
WORKDIR /usr/src/app
CMD "python /usr/src/app/miner.py ~"
