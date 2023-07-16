#include <Arduino.h>
#include <driver/adc.h>

const int analogInPin = 34;  // The pin that you're measuring the voltage at
const int digitalOutPin = 32; // The pin that will output 3.3V

const int numReadings = 2048;
int readings[numReadings]; // the readings from the analog input

void setup() {
  // Initialize serial communications
  Serial.begin(9600); 

  // Initialize the digital pin as an output.
  pinMode(digitalOutPin, OUTPUT);

  adc1_config_width(ADC_WIDTH_BIT_12);
  adc1_config_channel_atten(ADC1_CHANNEL_0, ADC_ATTEN_DB_0);

  // Enable ULP mode and set the ADC sample rate to 10 Hz
  adc1_ulp_enable();
  //adc1_ulp_rate(204800);

  // Wait for 1 second
  delay(1000);
  
  // Turn on the digital output
  digitalWrite(digitalOutPin, LOW);
}

void loop() {
  digitalWrite(digitalOutPin, HIGH);

  for(int count = 0; count < numReadings; count++){
    // Read the analog in value
    readings[count] = analogRead(analogInPin);

    // Wait a bit before the next reading
   }

  digitalWrite(digitalOutPin, LOW);

  // create a string that contains all the readings
  String readingsStr = "";
  for(int count = 0; count < numReadings; count++){
    readingsStr += String(readings[count]);
    if (count < numReadings - 1) {
      readingsStr += ", "; // add a comma between the readings
    }
  }

  // print the string
  Serial.println(readingsStr);

  // After all readings, wait for 10 seconds
  delay(10000);
}
