from Thingspeak import *
from utils import readAPIKey, writeAPIKey

if __name__ == "__main__":
    thingspeak = Thingspeak(readAPIKey, writeAPIKey)

    thingspeak.writeListToField([50, 40, 29, 100, 1000, 20, 10, 500], 1)
    # thingspeak.getField(2194131, 1, 0)