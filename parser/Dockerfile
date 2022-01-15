FROM debian:10

RUN apt-get update && \
    apt-get install -y \
    chromium \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND noninteractive
ENV TZ Europe/Moscow

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD [ "python3", "parser.py"]

