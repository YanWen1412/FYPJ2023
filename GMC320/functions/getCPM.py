import serial

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