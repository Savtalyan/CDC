FROM ubuntu:22.04

WORKDIR /app
COPY ./src /app

RUN apt-get update && \
    apt-get install -y  python3 python3-pip

CMD ["python3", "main.py"]