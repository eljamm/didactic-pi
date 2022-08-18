# Description

An educational platform for teaching beginners how to work with sensors using a Raspberry Pi. Therefore, it guides them with wiring schematics and pinout tables and allows them to control some sensors directly through the web interface.

The server includes both the django backend and the frontend components and is packaged as a docker container for better deployability and cross-platform compatibility. As such, it can run as a docker-compose service, alongside Postgresql and Redis, on any system capable of running docker.

The client contains a script to control the websocket `ws_control.py` and a package `raspi` that includes all the code for sensors and utilities.

# Table of Contents

- [Description](#description)
- [Table of Contents](#table-of-contents)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
  - [Improving Performance (Recommended)](#improving-performance-recommended)
- [Project Setup](#project-setup)
  - [Installing Dependencies](#installing-dependencies)
    - [Client](#client)
    - [Server](#server)
  - [Configuration](#configuration)
  - [Docker Image](#docker-image)
    - [Building](#building)
    - [Starting](#starting)
    - [Modification](#modification)
    - [Migrating Database](#migrating-database)
  - [Testing Connection](#testing-connection)
- [Client Setup](#client-setup)
- [Useful resources](#useful-resources)
- [Credits](#credits)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->

# Hardware Requirements

- It's recommended to use something like the [DuinoKit Raspberry Pi learning Kit](https://duinokit.com/store/home/10-duinokit-rpi-raspberry-pi-learning-kit.html) which conveniently groups together all the components a beginner might need while protecting some of them with built-in resistors. However, you can also use individual components or even make your own board if you're curious.

- The project was developed on a Raspberry Pi 3, Model B v1.2 with 1GB of RAM, so expect better or worse performance depending on your device.

# Software Requirements

Initially, I've used [RaspiOS](https://www.raspberrypi.com/software/operating-systems/) Bullseye, but I experienced frequent freezes while using it, even after trying to [optimize](#improving-performance-recommended) its performance.
This made me switch to an alternative to RaspiOS named [DietPi](https://dietpi.com/), which i found to be lighter and more performant.

The versions I tested were both AARCH64 and with a command-line interface only. So, I recommend you try them out and see which one works best for you.

## Improving Performance (Recommended)

This enables **zram** and some **kernel parameters** to improve system responsiveness in case you experience frequent freezes and hangups from your SD card. Also, it removes the default swap file since it's no longer needed.

This step is recommended in case you're using a low memory device or a sub-optimal SD card. However, you don't need to do this if you're using DietPi.

```sh
./utils/optimize.sh
```

# Project Setup

First, clone the git project on your local machine with :

```sh
git clone https://www.github.com/eljamm/didactic-card
cd didactic-card
```

## Installing Dependencies

You can install the client and server on the same machine or on different ones. However, the client needs to run on a Raspberry Pi whereas the server can be installed on any computer capable of running docker, including the Raspberry Pi.

For example, the server can be installed on your PC while many Raspberry Pi clients connect to it.

### Client

This upgrades the system packages and installs the required dependencies for the application.

It may take some time depending on your SD card and the number of packages to upgrade, so you may want to grab a cup of coffee in the meantime.

- RaspiOS

```sh
./utils/install-client.sh
```

- DietPi

```sh
sudo ./utils/install-client.sh
```

### Server

Given that the server runs as a docker service, it only depends on docker and docker-compose.

- RaspiOS

```sh
./utils/install-docker.sh
```

- DietPi

```sh
sudo dietpi-software install 162 # Docker
sudo dietpi-software install 134 # Docker-Compose
```

## Configuration

Before building the docker image, you need to create an .env file in the project directory :

```sh
touch .env
```

Then enter the following variables, which you should change according to your needs :

```txt
SECRET_KEY='django-insecure-XXX'
DEBUG=True
PORT=8000
POSTGRES_DB='postgres'
POSTGRES_PASSWORD='postgres'
POSTGRES_USER='postgres'
ALLOWED_HOSTS="localhost"
```

- SECRET_KEY: Should be changed to a unique and unpredictable value.
- DEBUG: A boolean that turns on/off debug mode.
- PORT: Port to run the application.
- POSTGRES_DB: The database name.
- POSTGRES_USER: PostgreSQL user name to connect as.
- POSTGRES_PASSWORD: Password to be used if demanded.
- ALLOWED_HOSTS: A space-separated list of host/domain names that the Django site can serve.

**Note**

To access the server from other devices you need to add your machine's ip address to the ALLOWED_HOSTS variable. For example, if your machine's address is **192.168.1.10** then change the variable to :

```txt
ALLOWED_HOSTS="localhost 192.168.1.10"
```

## Docker Image

### Building

After having all dependencies installed, you should build the services with :

```sh
docker-compose build
```

### Starting

To start the services, you can use :

```sh
docker-compose up -d && docker-compose logs -f -t
```

- -d: Starts the containers in the background.
- -f: Follow log output.
- -t: Show timestamps.

or the wrapper script for convenience :

```sh
./dostart --up --logs
```

**Note**

Running the service in detached mode allows us to exit the container log with `CTRL-C` without stopping the application.

### Modification

Any time you modify docker-compose.yml or the Dockerfile, you should rebuild the service with :

```sh
./dostart --build
```

or directly while starting it:

```sh
./dostart --up --build
```

**Note**

You can find out more about the `dostart` wrapper by executing :

```sh
./dostart --help
```

### Migrating Database

After starting all services, wait until this message appears on the container log :

```sh
didactic-card-db-1     | ... LOG:  database system is ready to accept connections
```

Then, press `CTRL-C` to exit the log and type the following :

```sh
docker-compose exec web python manage.py migrate
```

With this, the database is ready to be used and we can start using the application.

## Testing Connection

You can try connecting to the server by opening **[http://localhost:8000](http://localhost:8000)** in your browser. Don't forget to replace the port `8000` in the URL if you changed it in the configuration.

If you don't see a webpage, try restarting the web service :

```sh
docker-compose restart web
```

If you do, then you can proceed in creating, modifying or removing your Raspberry Pi devices.

# Client Setup

Before connecting to the server, in the `ws_control.py` file you must modify the following lines :

```txt
SERVER = "192.168.1.10"
PORT = "8000"
RASPI = "IOT1"
```

- SERVER: The server address which you added to ALLOWED_HOSTS, 192.168.1.10 for the previous example.
- PORT: The server port.
- RASPI: The name of the Raspberry Pi to connect to. Make sure it's created first from the website.

Then, you can connect with the server :

- RaspiOS

```txt
python ws_control.py
```

- DietPi

```txt
sudo python3 ws_control.py
```

# Useful resources

- [Django](https://docs.djangoproject.com/en/4.0/)
- [Django Channels](https://channels.readthedocs.io/en/stable/)
- [Bootstrap](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
- [GPIO Zero](https://gpiozero.readthedocs.io/en/stable/)
- [Adafruit CircuitPython Library Bundle](https://docs.circuitpython.org/projects/bundle/en/latest/index.html)

# Credits

- Improving Raspberry Pi performance by [Hayden James](https://haydenjames.io/raspberry-pi-performance-add-zram-kernel-parameters/)
- How to use the ADC8032 by [Heinrich Hartmann](https://gist.github.com/HeinrichHartmann/27f33798d12317575c6c).
- Raspberry Pi icon from [Raspberry Pi Ltd](https://www.raspberrypi.org/).
- Website icons from [Feather icons](https://github.com/feathericons/feather).
- Sensor icons from the [Flat Arduino SVG Icons Kit](https://github.com/philanri/arduino-icons)
- Some icons and all wiring schematics were originally created with [Fritzing](https://fritzing.org/) and were modified using [inkscape](https://inkscape.org/). Therefore, they all fall under the (CC BY-SA 3.0) license, as described in the [fritzing-parts license](https://github.com/fritzing/fritzing-parts/blob/develop/LICENSE.txt).
