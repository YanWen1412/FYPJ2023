#include <DHT.h>

#define LED 5
#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
}

void loop() {
  //LED will be blinking, LED can be use to do testing or condition 
  digitalWrite(LED, HIGH);
  delay(1000);
  digitalWrite(LED, LOW);
  delay(1000);

  //This is for the output for displaying the sensor readings
  Serial.print("Temperature = ");
  Serial.print(dht.readTemperature(),0);
  Serial.println("°C");

  Serial.print("Humidity = ");
  Serial.print(dht.readHumidity(),0);
  Serial.println("%");
 
  delay(1000);
}