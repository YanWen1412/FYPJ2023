# Final Year Project 2023 (Nanyang Polytechnic, IT)
## Created by Yan Wen and Zakir

# Task:
**Internet Of Things Based Environmental Monitoring System**

Written in **[Python 3.11](https://www.python.org/downloads/release/python-3110/)**, **[Arduino](https://www.arduino.cc/en/software)** and **[NodeRED](https://nodered.org/)**.

## Sensors used

| Sensor | Purpose |
| ------------- |:-------------:|
| [GMC320](https://www.gqelectronicsllc.com/comersus/store/comersus_viewItem.asp?idProduct=4579) | Radiation sensor |
| DHT11 | Temperature and Humidity sensor |
| ESP8266 | Main board used. Arduino, contains WIFI too. |

## Files

| File/Folder  | Purpose |
| ------------- |:-------------:|
| GMC320 | Anything in this folder is for GMC320. Handles ThingSpeak, MQTT and IFTTT for GMC320 |
| DHT_MQTT.ino | Arduino code to handle MQTT for DHT11 sensor |
| DHT_Thingspeak.ino | Arduino code to handle Thingspeak for DHT11 sensor |
| TempHum_LEDBlink.ino | Test code for DHT11 sensor |