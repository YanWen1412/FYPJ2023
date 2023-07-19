import datetime

'''
Returns current date and time
'''
def getCurrentDatetime():
    return "{:%d/%m/%Y %H:%M:%S}".format(datetime.datetime.now())