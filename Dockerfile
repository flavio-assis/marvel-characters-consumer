FROM python:3.9-slim

ENV LOG_LEVEL=INFO
ENV VERSION='0.0.1'
ENV MARVEL_PUBLIC_API_KEY=""
ENV MARVEL_PRIVATE_API_KEY=""
ENV APP_HOME="/home/consumer/marvel-characters-consumer"

COPY . /home/consumer/marvel-characters-consumer

WORKDIR /home/consumer/marvel-characters-consumer

RUN apt-get update && \
 apt-get upgrade -y && \
 apt-get clean

RUN python setup.py sdist
RUN python -m pip install --upgrade pip setuptools dist/marvel-characters-consumer-${VERSION}.tar.gz && \
 python -m pip install -r requirements.txt --no-cache-dir

RUN mkdir -p results/raw
RUN mkdir -p results/cleaned

ENTRYPOINT ["load-characters-df"]
