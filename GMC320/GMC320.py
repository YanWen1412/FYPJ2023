from Thingspeak import *
from IFTTT import *
from MQTT import *
from utils.utils import *

from functions.getCPM import *

import time
import serial
import sys

try:
    gmc = serial.Serial(gmc320Port, speed, timeout=3)
except serial.SerialException:
    gmc = None

peak = 0

'''
Main function
'''
if __name__ == "__main__":
    currentDatetime = getCurrentDatetime()
    ift = IFTTT(iftttAPIKey)
    mqtt = MQTT("2194131", mqttUsername, mqttPassword)
    thingspeakAPI = Thingspeak(readAPIKey, writeAPIKey)

    if len(sys.argv) > 1:
        print("Interval: {0} sec".format(sys.argv[1]))

        try:
            slp = float(sys.argv[1])
        except:
            print("Usage: python gmc-320.py 10 (For 10 second interval)\nTimer argument [1] must be an integer.")
            sys.exit(1)

    try:
        while True:
            currentDatetime = getCurrentDatetime()

            currentCPM = -1

            if gmc is None:
                try:
                    gmc = serial.Serial(gmc320Port, speed, timeout=3)
                except serial.SerialException:
                    gmc = None

            if gmc is not None:
                try:
                    currentCPM = getCPM(gmc)
                except serial.SerialException:
                    currentCPM = -1

            if currentCPM >= 0:
                cpm = "{0}, {1}\n".format(currentDatetime, currentCPM)

                safetyLvlInt = safetyLevelInt(currentCPM)
                safetyLvl = safetyLevelString(safetyLvlInt)
                safetyLvlStr = " | ".join(safetyLvl)

                if currentCPM > peak:
                    peak = currentCPM

                print("{0} | {1} (Peak: {2}) [{3}]".format(currentDatetime, currentCPM, peak, safetyLvlStr))

                if safetyLvlInt != 1 and sendIFTTTNotification:
                    print("Sending IFTTT Notification...")
                    
                    ift.sendNotification(safetyLvl[0], currentCPM, safetyLvl[1])
                    print("IFTTT Notification sent")

                if gmc is not None:
                    try:
                        thingspeakAPI.writeField(currentCPM)
                        print("Sent to Thingspeak...")
                    except InvalidAPIKeyError:
                        print("Invalid API Key provided for Thingspeak.\nSending through MQTT...")

                        mqtt.sendToThingspeak(currentCPM)
                else:
                    print("There is an issue with radiation detector...")
            else:
                print("An error occured while trying to communicate with GMC-320!")

                if isinstance(gmc, serial.Serial):
                    gmc.close()

                gmc = None

            time.sleep(sleep)
    except KeyboardInterrupt:
        if isinstance(gmc, serial.Serial):
            gmc.close()
        
        pass