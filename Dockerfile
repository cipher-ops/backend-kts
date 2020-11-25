#use:docker build -t backend-kts .
FROM python:3.6.6-alpine

WORKDIR /opt/backend-kts

ADD . /opt/backend-kts

RUN pip -i https://mirrors.aliyun.com/pypi/simple install -r /opt/backend-kts/requirements.txt \
    && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*

ENTRYPOINT [ "/opt/backend-kts/start.sh" ]
