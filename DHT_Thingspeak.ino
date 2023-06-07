#include <ESP8266WiFi.h>
#include <WiFiManager.h>
#include <ThingSpeak.h>
#include <DHT.h> //Import DHT Library


#define DHTPIN 2 // Should be GPIO #
#define DHTTYPE DHT11 // DHT11 or DHT22
DHT dht(DHTPIN, DHTTYPE); //Create DHT object

String apiKey = "P52R2XE3FPOXLDMU";     //  Enter your Write API key from ThingSpeak
const char* server = "api.thingspeak.com"; 


const int ledPin = 5; // LED connected to GPIO 2

WiFiClient client;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  dht.begin();


  WiFiManager wifiManager;


  // Uncomment the following line to reset the Wi-Fi settings
  // wifiManager.resetSettings();


  wifiManager.autoConnect("NodeMCU");


  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

// unsigned long myChannelNumber = 2078520; //Your Channel Number (Without Brackets)
// const char * myWriteAPIKey = ""; //Your Write API Key

void loop() {

  digitalWrite(ledPin, LOW); // turn the LED on (active LOW)
  delay(500); // wait for 0.5 second
  digitalWrite(ledPin, HIGH); // turn the LED off (active LOW)
  delay(500); // wait for 0.5 second


  float h = dht.readHumidity();
  float t = dht.readTemperature();
              if (isnan(h) || isnan(t)) 
                 {
                     Serial.println("Failed to read from DHT sensor!");
                      return;
                 }
 
                         if (client.connect(server,80))   //   "184.106.153.149" or api.thingspeak.com
                      {  
                            
                             String postStr = apiKey;
                             postStr +="&field1=";
                             postStr += String(t);
                             postStr +="&field2=";
                             postStr += String(h);
                             postStr += "\r\n\r\n";
 
                             client.print("POST /update HTTP/1.1\n");
                             client.print("Host: api.thingspeak.com\n");
                             client.print("Connection: close\n");
                             client.print("X-THINGSPEAKAPIKEY: "+apiKey+"\n");
                             client.print("Content-Type: application/x-www-form-urlencoded\n");
                             client.print("Content-Length: ");
                             client.print(postStr.length());
                             client.print("\n\n");
                             client.print(postStr);
 
                             Serial.print("Temperature: ");
                             Serial.print(t);
                             Serial.print(" degrees Celcius, Humidity: ");
                             Serial.print(h);
                             Serial.println("%. Send to Thingspeak.");
                        }
          client.stop();
 
          Serial.println("Waiting...");
  
  // thingspeak needs minimum 15 sec delay between updates
  delay(15000);
}