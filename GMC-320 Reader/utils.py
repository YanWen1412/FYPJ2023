import datetime

readAPIKey = "08M2G2N3H2XZ88U3"
writeAPIKey = "RVBKFIENCP30ZJLG"
baseURL = "https://api.thingspeak.com/"

mqttClientID = "AS4iHDA9EyQWIzIgMgE7Fh4"
mqttUsername = mqttClientID #"AS4iHDA9EyQWIzIgMgE7Fh4"
mqttPassword = "ICC8Fs3k6KkIshjD7J97/CQq"

speed = 115200
sleep = 3

'''
Converts value given by safetyLevelInt() to a readable string. List is provided in safetyLevelInt()
'''
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

'''
Returns an integer to determine if radiation level is safe or not

Parameters:
cpm => Radiation level (in cpm) obtained from GMC-320

Returns:
1 => Safe | No action needed
2 => Medium | Check reading regularly
3 => High | Closely watch reading, find out why
4 => Very high | Leave area asap and find out why
5 => Extremely high | Evacuate immediately and inform government
'''
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
    
'''
Returns current date and time
'''
def getCurrentDatetime():
    return "{:%d/%m/%Y %H:%M:%S}".format(datetime.datetime.now())