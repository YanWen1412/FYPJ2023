import datetime
import time
import serial
import sys
import requests
import json

# Change API key to your own
readAPIKey = ""
writeAPIKey = ""
baseURL = "https://api.thingspeak.com/"

speed = 115200
try:
    gmc = serial.Serial("COM5", speed, timeout=3)
except serial.SerialException:
    gmc = None
peak = 0
slp = 3

def writeField(data : int):
    if (data < 0):
        data = 0

    url = "{baseurl}/update?api_key={apikey}&field1={data}".format(
        baseurl=baseURL, 
        apikey=writeAPIKey, 
        data=data
    )
    
    r = requests.get(url)
    
    print(r.text)

def getField(channelID, fieldID = 1, results = 0):
    data = []

    if results > 0:
        url = "{base}/channels/{channelid}/fields/{fieldid}.json?api_key={apikey}&results={results}".format(
			base=baseURL, 
			channelid=channelID,
			fieldid=fieldID,
			apikey=readAPIKey,
			results=results
		)
    else:
        url = "{base}/channels/{channelid}/fields/{fieldid}.json?api_key={apikey}".format(
			base=baseURL, 
			channelid=channelID,
			fieldid=fieldID,
			apikey=readAPIKey
		)  

    bodyraw = requests.get(url).text
    body = json.loads(bodyraw)
    
    feedsData = body["feeds"]
    
    for feed in feedsData:
        field1Data = feed["field1"]
        
        data.append(field1Data)
        
    return data

# 1 => Safe | No action needed
# 2 => Medium | Check reading regularly
# 3 => High | Closely watch reading, find out why
# 4 => Very high | Leave area asap and find out why
# 5 => Extremely high | Evacuate immediately and inform government
def safetyLevelString(safetyLevel: int):
    msg = "Unknown | Check if there are any readings... error occured"
    if safetyLevel == 1:
        msg = "Safe | No action needed"
    elif safetyLevel == 2:
        msg = "Medium | Check reading regularly"
    elif safetyLevel == 3:
        msg = "High | Closely watch reading, find out why"
    elif safetyLevel == 4:
        msg = "Very high | Leave area asap and find out why"
    elif safetyLevel == 5:
        msg = "Extremely high | Evacuate immediately and inform government"

    return msg

def safetyLevelInt(cpm : int):
    cpm = int(cpm)

    if cpm <= 50:
        return  1
    elif cpm >= 51 and cpm <= 99:
        return 2
    elif cpm >= 100 and cpm <= 1000:
        return 3
    elif cpm > 1000 and cpm <= 2000:
        return 4
    else:
        return 5

def getCPM(gmc : serial.Serial):
    gmc.write(b"<GETCPM>>")
    data = gmc.read(2)
    
    if len(data) >= 2:
        gv = data[1]
    else:
        gv = 0
    
    return gv

def gmcCommand(gmc : serial.Serial, cmd, returnlength, byteformat=True):
    try:
        gmc.write(cmd)
    except:
        print("\nSend error")
        gmc.close()
        sys.exit(1)

    try:
        rtn = gmc.read(returnlength)
    except:
        print("\nReceive ERROR")
        gmc.close()
        sys.exit(1)

    if byteformat:
        rtn = map(ord, rtn)

    return rtn

def getClock():
    clockval = "<SETDATETIME[YYMMDDHHMMSS]>>"
    datenow = "{:%m/%d/%Y %H:%M:%S}".format(datetime.datetime.now())

    return datenow

cl = getClock()

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

        currentCPM = 0

        if gmc is None:
            try:
                gmc = serial.Serial("COM5", speed, timeout=3)
            except serial.SerialException:
                gmc = None

        if gmc is not None:
            currentCPM = getCPM(gmc)

        cpm = "{0}, {1}\n".format(cl, currentCPM)

        sli = safetyLevelInt(currentCPM)
        sls = safetyLevelString(sli)
        print(sls)

        if currentCPM > peak:
            peak = currentCPM

        print("{0} | {1} (Peak: {2})".format(cl, currentCPM, peak))

        if gmc is not None:
            writeField(currentCPM)
            print("Sent to Thingspeak...")
        else:
            print("There is an issue with radiation detector...")


        time.sleep(slp)
except KeyboardInterrupt:
    pass
