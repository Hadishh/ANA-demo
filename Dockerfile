FROM python:3.10.14

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /ana-demo

COPY ./requirements.txt .
RUN apt-get update -y && \
    apt-get install -y netcat-traditional && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /ana-demo/entrypoint.sh

COPY . .

ENTRYPOINT ["/ana-demo/entrypoint.sh"]
