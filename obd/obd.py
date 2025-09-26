import obd
from time import sleep

connection = obd.OBD()


while not connection.is_connected():
    if connection.status() == obd.OBDStatus.ELM327_CONNECTED:
        print("OBD-II connection established.")
        if connection.status() != obd.OBDStatus.CAR_CONNECTED:
            print("Waiting for engine to start...")
        else:
            break
    else:
        print("Connecting to OBD-II adapter...")

    sleep(3)

print("OBD-II connection established.")

cmd = obd.commands.SPEED # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

print(response.value) # returns unit-bearing values thanks to Pint
print(response.value.to("mph")) # user-friendly unit conversions

conn = obd.OBD()  # auto-connects to USB or RF port
