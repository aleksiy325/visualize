#include "Arduino.h"
#include "FastLED/FastLED.h"

uint8_t led_pin = LED_BUILTIN;

int main(void) {
    pinMode(led_pin, OUTPUT);

    while(1) {
        digitalWrite(led_pin, HIGH);  // set the LED on
        delay(5000);             // wait for a second
        digitalWrite(led_pin, LOW);   // set the LED off
        delay(5000);             // wait for a second
    }
}
