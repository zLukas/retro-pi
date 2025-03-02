# Retro Pi Display

This project contains scripts to display text on an LCD connected to a Raspberry Pi.

## Scripts

### `install.sh`

This script installs the necessary files to `/usr/bin` and sets the appropriate permissions.

### `display.py`

This Python script handles the communication with the LCD. It can display text provided as a command-line argument.

### `display-str`

This Bash script is a wrapper for `display.py`. It simplifies the process of displaying text on the LCD.

## Usage

1. **Install the scripts:**
    ```bash
    sudo ./install.sh
    ```

2. **Display text on the LCD:**
    ```bash
    display-str "Your text here"
    ```

3. **Clear the LCD display:**
    ```bash
    display-str --clear
    ```

nokia 5510 display was used so only 6 rows can be displayed at the time. the command append new to the display. when all 6 rows are filled with text, the screen clears itslefl and write a new line.
