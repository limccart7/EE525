#include "DHT.h"

//dht lib definitions
#define DHTPIN 2      //pin number for data
#define DHTTYPE DHT11 //sensor type

// Initialize the DHT sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600); 
  dht.begin(); //from adafruit
}

void loop() {
  //sample time 1.5s
  delay(1500);

  //gives us celsius
  float temp = dht.readTemperature();

  //did it fail?
  if (isnan(temp)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  //write out
  Serial.print("Temperature: ");
  Serial.println(temp);
  //Serial.println(" °C");
}
