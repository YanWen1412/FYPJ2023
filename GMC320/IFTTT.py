from utils.utils import iftttAPIKey

import requests #, random

class IFTTT():
    # Set up IFTTT with API Key
    def __init__(self, apikey : str) -> None:
        self.__apikey = apikey

    '''
    Activates Radiation IFTTT and sends an app and email to recipients through IFTTT

    Value1 => Radiation Level (Medium, Low, High or Unknown)
    Value2 => CPM
    Value3 => Advice
    '''
    def sendRadiationNotification(self, value1, value2, value3):
        data = {}

        data["value1"] = value1
        data["value2"] = value2
        data["value3"] = value3

        requests.post("https://maker.ifttt.com/trigger/Radiation_Level/with/key/{}"
                      .format(
                        self.__apikey
                    ), data=data)

# Test code
if __name__ == "__main__":
    from utils.safetyLevel import safetyLevel

    import random

    ifttt = IFTTT(iftttAPIKey)

    cpm = random.randint(51, 3000)
    safetyLvl = safetyLevel(cpm)

    ifttt.sendRadiationNotification("[TEST RUN] {}".format(safetyLvl[1]), cpm, safetyLvl[2])
 