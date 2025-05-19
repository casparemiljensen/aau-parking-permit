FROM python:3.11-slim

ENV TZ=Europe/Copenhagen

WORKDIR /app

COPY parking_issuer.py .
COPY scheduler.py .
COPY schedule.txt /app/data/schedule.txt
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "scheduler.py"]