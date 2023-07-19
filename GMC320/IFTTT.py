import requests #, random

class IFTTT():
    # Set up IFTTT with API Key
    def __init__(self, apikey : str) -> None:
        self.__apikey = apikey

    '''
    Value1 => Radiation Level (Medium, Low, High or Unknown)
    Value2 => CPM
    Value3 => Advice
    '''
    def sendNotification(self, value1, value2, value3):
        data = {}

        data["value1"] = value1
        data["value2"] = value2
        data["value3"] = value3

        requests.post("https://maker.ifttt.com/trigger/Radiation_Level/with/key/{}"
                      .format(
                        self.__apikey
                    ), data=data)
 