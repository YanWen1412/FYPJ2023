'''
Returns a list containing integer from 1 -5 to show how safe CPM is, and the radiation level and advice

Parameters:
cpm => Radiation level (in cpm) obtained from GMC-320

Returns:
1 => Safe | No action needed
2 => Medium | Check reading regularly
3 => High | Closely watch reading, find out why
4 => Very high | Leave area asap and find out why
5 => Extremely high | Evacuate immediately and inform government
'''
def safetyLevel(cpm : int):
    cpm = int(cpm)

    if cpm <= 50:
        return  [1, "Safe", "No action needed."]
    elif cpm >= 51 and cpm <= 99:
        return [2, "Medium", "Check reading regularly."]
    elif cpm >= 100 and cpm <= 1000:
        return [3, "High", "Closely watch reading, find out why. Avoid staying in the area for too long."]
    elif cpm > 1000 and cpm <= 2000:
        return [4, "Very high", "Leave area as soon as possible and find out what is causing the high radiation."]
    else:
        return [5, "Extremely high", "Evacuate immediately and inform government and respective authorities."]