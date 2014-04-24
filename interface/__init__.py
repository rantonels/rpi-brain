# Questo modulo e' un mockup di quello che effettivamente svolgera' la funzione di interfacciarsi con le periferiche.

# numerazione per le devices
# 0 VID1    webcam
# 1 TMP     sensore temperatura
# 2 BAR     sensore pressione barometrica
# 3 GEI     contatore Geiger

# Classi di errore

class DeviceError(Exception):
    pass


import logging
import os

device_names = ["VID1","TMP","BAR","GEI"]

logger = logging.getLogger("root.int")

active_devices = []

def startup_device(deviceID):
    if (deviceID<2):
        logger.info(device_names[deviceID] + " is on")
    else:
        logger.error("ERROR: "+device_names[deviceID] + " is OFF!")
        raise DeviceError
        
def startup_LEDS():
    pass

def startup(device_list):
    logger.info("starting LEDs...")
    startup_LEDS()

    logger.info("running startup check on devices...")
    for i in device_list:
        try:
            startup_device(i)
            active_devices.append(i)

        except DeviceError:
            logger.warn(device_names[i] + " is not active and will not be monitored. :(")

    return active_devices


def get_reading(deviceID):

    if not (deviceID in active_devices):
       return "N/A"

    if deviceID == 0:
       return "DO NOT READ HERE"
    elif deviceID == 1:
       return "21.2"
    elif deviceID == 2:
       return "0.4"
    elif deviceID == 3:
       return "0.0612"


def take_still(name):
    if 0 in active_devices:
        os.system("streamer -o pics/"+name+".jpeg -q")

    else:
       logger.warn("Taking still with VID1 failed. VID1 is not responding.")
