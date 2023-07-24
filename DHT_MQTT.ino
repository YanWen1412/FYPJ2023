#include <WiFiManager.h>

// Ensure that the credentials here allow you to publish and subscribe to the ThingSpeak channel.
#define channelID 2175640
const char mqttUserName[] = "KCkfGAEMBxwLJQUiFD08FTI";
const char clientID[] = "KCkfGAEMBxwLJQUiFD08FTI";
const char mqttPass[] = "1+f8tsV0PcDNyDO9Vq36socN";

// It is strongly recommended to use secure connections. However, certain hardware does not work with the WiFiClientSecure library.
// Comment out the following #define to use non-secure MQTT connections to ThingSpeak server.

#define USESECUREMQTT
// Comment the following line if not using an ESP8266.

#define ESP8266BOARD

#include <PubSubClient.h>
#ifdef ESP8266BOARD
#include <ESP8266WiFi.h>
const char* PROGMEM thingspeak_cert_thumbprint = "9780c25078532fc0fd03dae01bfd8c923fff9878";
#else
#include <WiFi.h>
const char* PROGMEM thingspeak_ca_cert =
  "-----BEGIN CERTIFICATE-----\n"
  "MIIDxTCCAq2gAwIBAgIQAqxcJmoLQJuPC3nyrkYldzANBgkqhkiG9w0BAQUFADBs\n" \
  "MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3\n" \
  "d3cuZGlnaWNlcnQuY29tMSswKQYDVQQDEyJEaWdpQ2VydCBIaWdoIEFzc3VyYW5j\n" \
  "ZSBFViBSb290IENBMB4XDTA2MTExMDAwMDAwMFoXDTMxMTExMDAwMDAwMFowbDEL\n" \
  "MAkGA1UEBhMCVVMxFTATBgNVBAoTDERpZ2lDZXJ0IEluYzEZMBcGA1UECxMQd3d3\n" \
  "LmRpZ2ljZXJ0LmNvbTErMCkGA1UEAxMiRGlnaUNlcnQgSGlnaCBBc3N1cmFuY2Ug\n" \
  "RVYgUm9vdCBDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMbM5XPm\n" \
  "+9S75S0tMqbf5YE/yc0lSbZxKsPVlDRnogocsF9ppkCxxLeyj9CYpKlBWTrT3JTW\n" \
  "PNt0OKRKzE0lgvdKpVMSOO7zSW1xkX5jtqumX8OkhPhPYlG++MXs2ziS4wblCJEM\n" \
  "xChBVfvLWokVfnHoNb9Ncgk9vjo4UFt3MRuNs8ckRZqnrG0AFFoEt7oT61EKmEFB\n" \
  "Ik5lYYeBQVCmeVyJ3hlKV9Uu5l0cUyx+mM0aBhakaHPQNAQTXKFx01p8VdteZOE3\n" \
  "hzBWBOURtCmAEvF5OYiiAhF8J2a3iLd48soKqDirCmTCv2ZdlYTBoSUeh10aUAsg\n" \
  "EsxBu24LUTi4S8sCAwEAAaNjMGEwDgYDVR0PAQH/BAQDAgGGMA8GA1UdEwEB/wQF\n" \
  "MAMBAf8wHQYDVR0OBBYEFLE+w2kD+L9HAdSYJhoIAu9jZCvDMB8GA1UdIwQYMBaA\n" \
  "FLE+w2kD+L9HAdSYJhoIAu9jZCvDMA0GCSqGSIb3DQEBBQUAA4IBAQAcGgaX3Nec\n" \
  "nzyIZgYIVyHbIUf4KmeqvxgydkAQV8GK83rZEWWONfqe/EW1ntlMMUu4kehDLI6z\n" \
  "eM7b41N5cdblIZQB2lWHmiRk9opmzN6cN82oNLFpmyPInngiK3BD41VHMWEZ71jF\n" \
  "hS9OMPagMRYjyOfiZRYzy78aG6A9+MpeizGLYAiJLQwGXFK3xPkKmNEVX58Svnw2\n" \
  "Yzi9RKR/5CYrCsSXaQ3pjOLAEFe4yHYSkVXySGnYvCoCWw9E1CAx2/S6cCZdkGCe\n" \
  "vEsXCS+0yx5DaMkHJ8HSXPfqIbloEpw8nL+e/IBcm2PN7EeqJSdnoDfzAIJ9VNep\n" \
  "+OkuE6N36B9K\n" \
  "-----END CERTIFICATE-----\n";
#endif

#ifdef USESECUREMQTT
#include <WiFiClientSecure.h>
#define mqttPort 8883
WiFiClientSecure client;
#else
#define mqttPort 1883
WiFiClient client;
#endif

#include <DHT.h>
#include <Arduino.h>

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);  //Create DHT object

const char* server = "mqtt3.thingspeak.com";
int status = WL_IDLE_STATUS;
long lastPublishMillis = 0;
int connectionDelay = 1;
int updateInterval = 15;
PubSubClient mqttClient(client);

// Function to handle messages from MQTT subscription.
void mqttSubscriptionCallback(char* topic, byte* payload, unsigned int length) {
  // Print the details of the message that was received to the serial monitor.
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

// Subscribe to ThingSpeak channel for updates.
void mqttSubscribe(long subChannelID) {
  String myTopic = "channels/" + String(subChannelID) + "/subscribe";
  mqttClient.subscribe(myTopic.c_str());
}

// Publish messages to a ThingSpeak channel.
void mqttPublish(long pubChannelID, String message) {
  String topicString = "channels/" + String(pubChannelID) + "/publish";
  mqttClient.publish(topicString.c_str(), message.c_str());
}

// Connect to WiFi.
void connectWifi() {
  Serial.begin(115200);

  WiFiManager wifiManager;

  wifiManager.autoConnect("NodeMCU");

  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

// Connect to MQTT server.
void mqttConnect() {
  // Loop until connected.
  while (!mqttClient.connected()) {
    // Connect to the MQTT broker.
    if (mqttClient.connect(clientID, mqttUserName, mqttPass)) {
      Serial.print("MQTT to ");
      Serial.print(server);
      Serial.print(" at port ");
      Serial.print(mqttPort);
      Serial.println(" successful.");
    } else {
      Serial.print("MQTT connection failed, rc = ");
      // See https://pubsubclient.knolleary.net/api.html#state for the failure code explanation.
      Serial.print(mqttClient.state());
      Serial.println(" Will try again in a few seconds");
      delay(connectionDelay * 1000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  // Delay to allow serial monitor to come up.
  delay(3000);
  // Connect to Wi-Fi network.
  connectWifi();
  // Configure the MQTT client
  mqttClient.setServer(server, mqttPort);
  // Set the MQTT message handler function.
  mqttClient.setCallback(mqttSubscriptionCallback);
  // Set the buffer to handle the returned JSON. NOTE: A buffer overflow of the message buffer will result in your callback not being invoked.
  mqttClient.setBufferSize(2048);
// Use secure MQTT connections if defined.
#ifdef USESECUREMQTT
// Handle functionality differences of WiFiClientSecure library for different boards.
#ifdef ESP8266BOARD
  client.setFingerprint(thingspeak_cert_thumbprint);
#else
  client.setCACert(thingspeak_ca_cert);
#endif
#endif
}

void loop() {
  // Reconnect to WiFi if it gets disconnected.
  if (WiFi.status() != WL_CONNECTED) {
    connectWifi();
  }

  // Connect if MQTT client is not connected and resubscribe to channel updates.
  if (!mqttClient.connected()) {
    mqttConnect();
    mqttSubscribe(channelID);
  }

  // Call the loop to maintain connection to the server.
  mqttClient.loop();

  // Update ThingSpeak channel periodically. The update results in the message to the subscriber.
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  Serial.print("Temperature = ");
  Serial.print(t,0);
  Serial.println("°C");
  Serial.print("Humidity = ");
  Serial.print(h,0);
  Serial.println("%");

  char tbuff[10];
  dtostrf(t, 4, 2, tbuff);
  char hbuff[10];
  dtostrf(h, 4, 2, hbuff);

  String payload = "field1=";
  payload += tbuff;
  payload += "&field2=";
  payload += hbuff;

  if (!isnan(t) && !isnan(h))
  {
    mqttPublish(channelID, (char*)payload.c_str());
    lastPublishMillis = millis();
  }
  else {
    Serial.println("Temperature and Humidity nan");
  }

  delay(15000);
}
