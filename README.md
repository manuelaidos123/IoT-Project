To Use the files use the following commands:

docker build -t myimage .     Creats a single docker Image

docker run -it myimage        Runs the image created above

docker-compose up -d --scale mqtt_led_controller=3    Creates three docker images and automatic runs thems syncronously

Note: Some of the python files have some imports do not forget to install them
