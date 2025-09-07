FROM python:3.11-slim

ENV TZ=Europe/Copenhagen

WORKDIR /app

RUN mkdir -p ./data

COPY parking_issuer.py .
COPY scheduler.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY data ./data

CMD ["python", "-u", "scheduler.py"]
