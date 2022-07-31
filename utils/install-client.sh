#!/bin/bash

# Upgrade system packages
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y apt-utils build-essential git pigpio python3-dev \
python3-gpiozero python3-pip python3-rpi.gpio rsync

# Useful text editors
sudo apt install -y neovim micro

# Install python packages
pip install -r ./utils/raspberry-requirements.txt

# Uninstall make dependencies
#sudo apt uninstall build-essential python3-dev
