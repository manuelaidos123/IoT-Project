FROM python:3.10-slim

WORKDIR /app

COPY dht22_sim.py .

RUN pip install paho-mqtt

CMD ["python", "dht22_sim.py"]


