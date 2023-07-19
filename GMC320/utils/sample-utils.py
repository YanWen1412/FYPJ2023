'''
FILL IN THE API KEYS AND CREDENTIALS BELOW

RENAME THIS FILE TO "utils.py"
'''

sendToThingspeak = False

# API Keys of channel in Thingspeak
readAPIKey = ""
writeAPIKey = ""

# Leave baseURL as it is if you don't know what it does
baseURL = "https://api.thingspeak.com/"

sendIFTTTNotification = True
iftttAPIKey = ""

mqttClientID = "" 
mqttUsername = mqttClientID 
mqttPassword = ""

gmc320Port = "COM3"

# Baud rate of Sensor. Leave as it is if you don't know what it does.
speed = 115200

# Delay before checking sensor for new data. In seconds
sleep = 15