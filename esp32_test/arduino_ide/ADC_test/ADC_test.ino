#include <ADC.h>

// define which pin you're using
const int analogPin = 34;  // change this to your pin number

// define the number of samples
const int numSamples = 2048;

// declare an array to hold the samples
int samples[numSamples];
int currentSample = 0;

// Create an ADC object
ADC adc;

void setup() {
  // begin serial communication for debugging
  Serial.begin(115200);

  // configure ADC
  adc.setResolution(12); // 12-bit resolution
  adc.setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);
  adc.setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED);

  // configure ADC pin
  adc.setPins(adc.channel(analogPin));

  // attach ADC interrupt handler
  adc.enableInterrupts(onADCRead, 1);

  // start ADC continuous conversion
  adc.startContinuous(analogPin);
}

void loop() {
  // empty loop as the ADC interrupt handler will handle the sampling and printing
}

void onADCRead(uint32_t val) {
  samples[currentSample] = val;
  currentSample++;

  if (currentSample >= numSamples) {
    // stop ADC continuous conversion
    adc.stopContinuous(analogPin);

    // print out all the samples
    Serial.print("[");
    for (int i = 0; i < numSamples; i++) {
      Serial.print(samples[i]);
      if (i < numSamples - 1) {
        Serial.print(", ");
      }
    }
    Serial.println("]");

    // stop the program from running further
    while (true) {
      continue;
    }
  }
}
