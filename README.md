# IoT Project

This project demonstrates the integration of an MQTT broker with DHT22 sensor and Python Flask Script to show the temperature and humidity changes in real-time
and with the addition of Dataframes using Panda Python Library.

## Prerequisites

- Docker on Linux
- Docker Desktop Application on Windows

## Installation

Follow these steps to install and run the project.

1. Clone the repository.
2. Navigate to the project directory.
3. Make sure docker is running (Docker Desktop on Windows or run systemctl docker on Linux)
4. Open CLI inside the project directory
5. run dht22_sim.py using docker or docker compose
6. Open a new CLI terminal and execute python dhtt22_info_website.py to run the Python flask script
7. open a browser Tab and copy and paste the link where the server is running

### Docker Build

docker build -t [name of image] .

### Docker Run

docker run -it [name of image]

### Docker Compose

docker-compose up -d --scale mqtt_led_controller=[number of images to run simultaneous]




