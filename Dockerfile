## base image
FROM ubuntu:20.04

## dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends --fix-missing \
    python3-pip \
    firefox \
    wget

RUN pip3 install --upgrade pip

## geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.30.0-linux64.tar.gz && \
    rm geckodriver-v0.30.0-linux64.tar.gz
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin/

## set work dir
WORKDIR /code

## copy script
COPY . /code

## libraires
RUN pip3 install -r requirements.txt

## run app
CMD ["bash", "./start.sh"]