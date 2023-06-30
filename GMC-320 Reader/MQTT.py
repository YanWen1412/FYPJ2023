from utils import mqttPassword, mqttUsername, sleep

import paho.mqtt.publish as publish
import time

# Basic MQTT class
class MQTT:
    mqttHost = "mqtt3.thingspeak.com"
    transport = "websockets"
    port = 80

    '''
    Initialise Thingspeak class
    '''
    
    def __init__(self, channelID, mqttUsername, mqttPassword, mqttClientID = None) -> None:
        self.__channelID = str(channelID)
        self.__topic = "channels/{}/publish".format(self.__channelID)
        self.__mqttUsername = str(mqttUsername)

        if mqttClientID is None:
            self.__mqttClientID = str(mqttUsername)
        else:
            self.__mqttClientID = str(mqttClientID)

        self.__mqttPassword = str(mqttPassword)

    def sendToThingspeak(self, cpm):
        payload = "field1={}".format(cpm)
        try:
            print("Sending to Thingspeak through MQTT.")
            publish.single(self.__topic, payload, hostname=self.mqttHost, transport=self.transport, port=self.port, client_id=self.__mqttClientID, auth={'username':self.__mqttUsername,'password':self.__mqttPassword})
        except Exception as e:
            print(e)

if __name__ == "__main__":
    import serial

    from utils import speed, getCurrentDatetime, safetyLevelInt, safetyLevelString

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

    try:
        gmc = serial.Serial("COM5", speed, timeout=3)
    except serial.SerialException:
        gmc = None

    peak = 0

    currentDatetime = getCurrentDatetime()

    while True:
        currentDatetime = getCurrentDatetime()
        currentCPM = -1

        mqtt = MQTT("2194131", mqttUsername, mqttPassword)

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
            cpm = "{0}, {1}\n".format(currentDatetime, currentCPM)

            safetyLvlInt = safetyLevelInt(currentCPM)
            safetyLvlStr = safetyLevelString(safetyLvlInt)

            if currentCPM > peak:
                peak = currentCPM

            print("{0} | {1} (Peak: {2}) [{3}]".format(currentDatetime, currentCPM, peak, safetyLvlStr))

            if gmc is not None:
                mqtt.sendToThingspeak(currentCPM)
        else:
            print("An error occured while trying to communicate with GMC-320!")

            if isinstance(gmc, serial.Serial):
                gmc.close()

            gmc = None

        time.sleep(sleep)
