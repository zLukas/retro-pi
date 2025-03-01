#!/bin/bash

apt update
apt install python3-pip
pip3 install spidev RPi.GPIO pillow --break-system-packages



