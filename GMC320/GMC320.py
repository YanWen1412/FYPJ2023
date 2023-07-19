from utils import *
from Thingspeak import *
from IFTTT import *
from MQTT import *
from utils.utils import *
from utils.safetyLevel import *
from utils.getCurrentDatetime import *

from functions.getCPM import *

import time
import serial
import sys

try:
    gmc = serial.Serial(gmc320Port, speed, timeout=3)
except serial.SerialException:
    gmc = None

peakCPM = 0
prevCPM = 0

# Fill in the list with data of numbers to bypass sensor requirement for testing
testCPMData = [40, 52, 500, 500, 1500, 9000, 2]

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

            if len(testCPMData) > 0:
                currentCPM = testCPMData[0]
            else:
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

                safetyLvlData = safetyLevel(currentCPM)
                safetyLvlInt = safetyLvlData[0]
                safetyLvl = [x for x in safetyLvlData[1:]]
                safetyLvlStr = " | ".join(safetyLvl)

                if currentCPM > peakCPM:
                    peakCPM = currentCPM

                print("{0} | {1} (Peak: {2}) [{3}]".format(currentDatetime, currentCPM, peakCPM, safetyLvlStr))

                if gmc is not None or len(testCPMData) > 0:
                    if sendToThingspeak:
                        try:
                            thingspeakAPI.writeField(currentCPM)
                            print("Sent to Thingspeak...")
                        except InvalidAPIKeyError:
                            print("Invalid API Key provided for Thingspeak.\nSending through MQTT...")

                            mqtt.sendToThingspeak(currentCPM)
                    else:
                        print("Thingspeak is disabled. Enable it in utils.py")
                else:
                    print("There is an issue with radiation detector...")
                
                if safetyLvlInt != 1 and sendIFTTTNotification and not sendToThingspeak:
                    if currentCPM != prevCPM:
                        print("Sending IFTTT Notification...")
                        ift.sendNotification(safetyLvl[0], currentCPM, safetyLvl[1])
                        print("IFTTT Notification sent")
                    else:
                        print("IFTTT notification for CPM {} sent before. Not sending.".format(currentCPM))

                prevCPM = currentCPM
            else:
                print("An error occured while trying to communicate with GMC-320!")

                if isinstance(gmc, serial.Serial):
                    gmc.close()

                gmc = None

            if len(testCPMData) > 0:
                testCPMData.pop(0)
                print(testCPMData)

            time.sleep(sleep)
    except KeyboardInterrupt:
        if isinstance(gmc, serial.Serial):
            gmc.close()
        
        pass