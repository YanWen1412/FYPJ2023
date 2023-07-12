# GMC-320 Reader
### A Python script written to fetch live data from [GMC-320](https://www.gqelectronicsllc.com/comersus/store/comersus_viewItem.asp?idProduct=4579) and send it to [Thingspeak](https://thingspeak.com/)

The script now will send notification to IFTTT, if you want it to.

Written in **[Python 3.11](https://www.python.org/downloads/release/python-3110/)**.

**Library used:**
* [requests](https://pypi.org/project/requests/)
* [umqtt.robust](https://pypi.org/project/micropython-umqtt.robust/)
* [paho-mqtt](https://pypi.org/project/paho-mqtt/)

## Files

| File  | Purpose |
| ------------- |:-------------:|
| utils.py | Config file for the program. Contains information that user should change accordingly |
| Thingspeak.py | File that will handle receiving and sending data to and from Thingspeak |
| MQTT.py | File that will handle receiving and sending data to and from MQTT |
| GMC320.py | Main file for the program. Where the magic really happens |
| TS-Test.py | File used to test Thingspeak.py |
| IFTTT.py | File used for IFTTT |
