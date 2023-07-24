# GMC-320 Reader
### A Python script written to fetch live data from [GMC-320](https://www.gqelectronicsllc.com/comersus/store/comersus_viewItem.asp?idProduct=4579) and send it to [Thingspeak](https://thingspeak.com/)

The script now will send notification to IFTTT, if you want it to.

Written in **[Python 3.11](https://www.python.org/downloads/release/python-3110/)**.

**Library used:**
* [requests](https://pypi.org/project/requests/)
* ~~[umqtt.robust](https://pypi.org/project/micropython-umqtt.robust/)~~
* [pyserial](https://pypi.org/project/pyserial/)

## Files

| File  | Purpose |
| ------------- |:-------------:|
| Thingspeak.py | File that will handle receiving and sending data to and from Thingspeak |
| MQTT.py | File that will handle receiving and sending data to and from MQTT |
| GMC320.py | Main file for the program. Where the magic really happens |
| TS-Test.py | File used to test Thingspeak.py |
| IFTTT.py | File used for IFTTT |
| utils/sample-utils.py | Sample utils file. Follow instructions in the file to know how to set it up |

**Everything else in utils and functions folder, SHOULD NOT BE TOUCHED**

## Folders

| Folder | Purpose |
| ------------- |:-------------:|
| functions | Contains function(s) that is used by the main program |
| utils | Utilities folder. Contains utility function(s) and the config file for the program (utils.py from sample-utils.py) |
