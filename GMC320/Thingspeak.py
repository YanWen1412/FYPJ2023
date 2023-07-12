from utils import baseURL

import requests
import json

class InvalidFieldIDError(Exception):
    """
    Exception raised when Field ID is invalid for Thingspeak.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message : str = "Invalid Field ID") -> None:
        self.__message = message
        super().__init__(self.__message)

class InvalidChannelIDError(Exception):
    """
    Exception raised when Channel ID is invalid for Thingspeak.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message : str = "Invalid Channel ID") -> None:
        self.__message = message
        super().__init__(self.__message)

class InvalidAPIKeyError(Exception):
    """
    Exception raised when API Key is invalid for Thingspeak.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message : str = "Invalid API Key") -> None:
        self.__message = message
        super().__init__(self.__message)

# Basic Thingspeak class
class Thingspeak():
    '''
    Initialise Thingspeak class
    '''
    def __init__(self, readAPIKey : str = "", writeAPIKey : str = "") -> None:
        self.__readAPIKey = readAPIKey
        self.__writeAPIKey = writeAPIKey
        
    ''' 
    Writes/Sends data to a specific Thingspeak field with field ID of fieldID

    Example url: 
    https://api.thingspeak.com/update?api_key={apikey}&field1=0
    https://api.thingspeak.com/update?api_key={apikey}&field{fieldID}={data}

    Parameters:
    data => data you want to be sent to Thingspeak (One integer)
    fieldID => ID of Field, seen after "?api_key={apikey}&" (Integer)

    Returns True if successful, otherwise False
    '''
    def writeField(self, data : int, fieldID : int = 1):
        if (data < 0):
            data = 0

        url = "{baseurl}/update?api_key={apikey}&field{fieldID}={data}".format(
            baseurl=baseURL, 
            apikey=self.__writeAPIKey,
            fieldID =fieldID,
            data=data
        )
    
        r = requests.get(url)

        if r.text == "0":
            raise InvalidAPIKeyError("Invalid Write API Key")
            
        return True

    ''' 
    Writes/Sends multiple data to a specific Thingspeak field with field ID of fieldID

    Example url: 
    https://api.thingspeak.com/update?api_key={apikey}&field1=0
    https://api.thingspeak.com/update?api_key={apikey}&field{fieldID}={data}

    Parameters:
    data => list of data you want to be sent to Thingspeak (List)
    fieldID => ID of Field, seen after "?api_key={apikey}&" (Integer)

    Returns True if successful, otherwise False
    '''
    def writeListToField(self, data : list, fieldID : int = 1):
        for d in data:
            self.writeField(data=d, fieldID=fieldID)

    '''
    Gets data from a specific field from Thingspeak

    Example url:
    https://api.thingspeak.com/channels/2194131/fields/1.json?api_key={apikey}
    https://api.thingspeak.com/channels/{channelid}/fields/{fieldid}.json?api_key={apikey}

    Parameters:
    channelID => ID of channel, as seen after /channels/ in example url above (Integer)
    fieldID => ID of field, as seen after /fields/ in example url above (Integer)
    results => Specify number of results to fetch from field. Leave 0 to fetch ll

    Returns a list of data
    '''
    def getField(self, channelID:int, fieldID:int = 1, results:int = 0):
        data = []

        url = "{base}/channels/{channelid}/fields/{fieldid}.json?api_key={apikey}".format(
			base=baseURL, 
			channelid=channelID,
			fieldid=fieldID,
			apikey=self.__readAPIKey
		)

        if results > 0:
            url = "{base}/channels/{channelid}/fields/{fieldid}.json?api_key={apikey}&results={results}".format(
                base=baseURL, 
                channelid=channelID,
                fieldid=fieldID,
                apikey=self.__readAPIKey
                 ,
                results=results
            )

        bodyraw = requests.get(url).text
        body = json.loads(bodyraw)
        
        if isinstance(body, int) and body == -1:
            return InvalidAPIKeyError("Invalid Read API Key")

        status = None
        try:
            status = body["status"]
        except:
            status = None

        if status == "404":
            raise InvalidChannelIDError()
        
        if status == "400":
            raise InvalidFieldIDError()

        feedsData = body["feeds"]
        
        try:
            for feed in feedsData:
                field1Data = feed["field1"]
                
                data.append(field1Data)
        except KeyError:
            data = []
            
        return data