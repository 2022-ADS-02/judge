# syntax=docker/dockerfile:1

FROM python:3.8
WORKDIR /app

COPY ./ /app/
RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

FROM openjdk:slim
COPY --from=python:3.8 / /

WORKDIR /app


EXPOSE 9000

CMD [ "python3", "app.py"]
