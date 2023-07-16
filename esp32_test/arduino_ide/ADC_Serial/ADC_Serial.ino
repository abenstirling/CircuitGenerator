#include <driver/adc.h>
#include <driver/timer.h>

#define ADC_PIN 34
#define SAMPLE_RATE 2000 // Sample rate in Hz
#define SAMPLES_PER_CYCLE 1024 // Number of samples in a full cycle

volatile int IRAM_ATTR samples[SAMPLES_PER_CYCLE]; // Array to store the samples
volatile int IRAM_ATTR sampleCount = 0; // Number of samples taken so far

void IRAM_ATTR onTimer(void* arg) {
  // Clear the interrupt status
  timer_group_clr_intr_status_in_isr(TIMER_GROUP_0, TIMER_0);
  
  // Take a sample
  int adc_value = analogRead(ADC_PIN);
  // Store the sample in the array
  samples[sampleCount] = adc_value;
  // Update the sample count
  sampleCount++;

  // Check if a full cycle has been sampled
  if (sampleCount == SAMPLES_PER_CYCLE) {
    // Reset the sample count
    sampleCount = 0;
  }

  // Enable alarm again
  timer_group_enable_alarm_in_isr(TIMER_GROUP_0, TIMER_0);
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12); // Configure the resolution to 12 bits

  // Configure timer
  timer_config_t config = {
    .alarm_en = TIMER_ALARM_EN, // Enable timer alarm
    .counter_en = TIMER_PAUSE, // Start the timer counter paused
    .intr_type = TIMER_INTR_LEVEL, // Interrupt mode
    .counter_dir = TIMER_COUNT_UP, // Counter direction
    .auto_reload = TIMER_AUTORELOAD_EN, // Enable auto-reload
    .divider = 80 // 80 is the prescaler value
  };
  timer_init(TIMER_GROUP_0, TIMER_0, &config);

  // Set the timer counter value to 0
  timer_set_counter_value(TIMER_GROUP_0, TIMER_0, 0x00000000ULL);

  // Set the timer alarm value (the interval between interrupts)
  timer_set_alarm_value(TIMER_GROUP_0, TIMER_0, 1000000 / SAMPLE_RATE);

  // Enable the timer interrupt, and set the priority
  timer_enable_intr(TIMER_GROUP_0, TIMER_0);
  timer_isr_register(TIMER_GROUP_0, TIMER_0, &onTimer, NULL, ESP_INTR_FLAG_IRAM, NULL);

  // Start the timer
  timer_start(TIMER_GROUP_0, TIMER_0);
}

void loop() {
  // Check if a full cycle has been sample
    
    if (sampleCount == 0) {
      //Serial.println(6);
      // Send the samples over Serial
      //String data = "[";
      for (int i = 0; i < SAMPLES_PER_CYCLE; i++) {
        //int k = samples[i];
        
        Serial.println(samples[i]);
        //data += String(samples[i]);
        //if (i < SAMPLES_PER_CYCLE - 1) {
        //  data += ", ";
        
      }
      //data += "]";

  }
}