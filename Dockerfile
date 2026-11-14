FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update -y && \
    apt-get install -y awscli

RUN python -m pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt

CMD ["python", "application.py"]
