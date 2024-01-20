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

### Docker Build

docker build -t [name of image] .

### Docker Run

docker run -it [name of image]

### Docker Compose

docker-compose up -d --scale mqtt_led_controller=[number of images to run simultaneous]




