#!/bin/bash

apt update
apt install python3-pip
pip3 install spidev RPi.GPIO pillow --break-system-packages

CONFIG_FILE=/boot/firmware/config.txt

# enable SPI in boot config
sed -i  s'/#dtparam=spi=on/dtparam=spi=on/' ${CONFIG_FILE}

# Load SPI kernel module
if ! lsmod | grep -q spi_bcm2835; then
    echo "Loading SPI kernel module..."
    sudo modprobe spi_bcm2835
else
    echo "SPI kernel module is already loaded."
fi

reboot