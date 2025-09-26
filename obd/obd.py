import obd
import os

from time import sleep

connection = obd.OBD()


# execute shell cmd
# TODO: replace with python display code
def print_on_display(text: str) -> None:
    os.system(f"display-str {text}")

while not connection.is_connected():
    if connection.status() == obd.OBDStatus.ELM327_CONNECTED:
        print_on_display("OBD-II connection established.")
        if connection.status() != obd.OBDStatus.CAR_CONNECTED:
            print_on_display("Waiting for engine to start...")
        else:
            break
    else:
        print_on_dprint_on_displayisplay("Connecting to OBD-II adapter...")

    sleep(3)

print_on_display("OBD-II connection established.")

cmd = obd.commands.SPEED # select an OBD command (sensor)
