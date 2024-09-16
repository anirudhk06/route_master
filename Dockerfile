FROM python:3.11-alpine

ENV PYTHONDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

# upgrate pip version
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./src .
