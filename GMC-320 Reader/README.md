# GMC-320 Reader
### A Python script written to fetch live data from [GMC-320](https://www.gqelectronicsllc.com/comersus/store/comersus_viewItem.asp?idProduct=4579) and send it to [Thingspeak](https://thingspeak.com/)

Written in **[Python 3.11](https://www.python.org/downloads/release/python-3110/)**.

**Library used:**
* [requests](https://pypi.org/project/requests/)

## Files

| File  | Purpose |
| ------------- |:-------------:|
| utils.py | Config file for the program. Contains information that user should change accordingly |
| Thingspeak.py | File that will handle receiving and sending data to and from Thingspeak |
| GMC320.py | Main file for the program. Where the magic really happens |
