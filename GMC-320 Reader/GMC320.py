from utils import *
from Thingspeak import Thingspeak

import time
import serial
import sys

try:
    gmc = serial.Serial("COM5", speed, timeout=3)
except serial.SerialException:
    gmc = None

peak = 0

'''
Gets live radiation data from GMC-320
'''
def getCPM(gmc : serial.Serial):
    gmc.write(b"<GETCPM>>")
    data = gmc.read(2)
    
    if len(data) >= 2:
        gv = data[1]
    else:
        gv = 0
    
    return gv

'''
Main function
'''
if __name__ == "__main__":
    cl = getClock()
    ts = Thingspeak(readAPIKey, writeAPIKey)

    if len(sys.argv) > 1:
        print("Interval: {0} sec".format(sys.argv[1]))

        try:
            slp = float(sys.argv[1])
        except:
            print("Usage: python gmc-320.py 10 (For 10 second interval)\nTimer argument [1] must be an integer.")
            sys.exit(1)

    try:
        while True:
            cl = getClock()

            currentCPM = -1

            if gmc is None:
                try:
                    gmc = serial.Serial("COM5", speed, timeout=3)
                except serial.SerialException:
                    gmc = None

            if gmc is not None:
                try:
                    currentCPM = getCPM(gmc)
                except serial.SerialException:
                    currentCPM = -1

            if currentCPM >= 0:
                cpm = "{0}, {1}\n".format(cl, currentCPM)

                sli = safetyLevelInt(currentCPM)
                sls = safetyLevelString(sli)

                if currentCPM > peak:
                    peak = currentCPM

                print("{0} | {1} (Peak: {2}) [{3}]".format(cl, currentCPM, peak, sls))

                if gmc is not None:
                    ts.writeField(currentCPM)
                    print("Sent to Thingspeak...")
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