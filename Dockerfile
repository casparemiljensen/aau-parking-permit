FROM python:3.11-slim

ENV TZ=Europe/Copenhagen

WORKDIR /app

COPY parking_issuer.py .
COPY scheduler.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create data folder and a template schedule
RUN mkdir -p /app/data \
    && echo "days: monday, tuesday, wednesday, thursday, friday\ntimes: 08:45\nphone_no:\nlicense_plate:" > /app/data/schedule.txt

CMD ["python", "-u", "scheduler.py"]