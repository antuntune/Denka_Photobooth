//declaring variables
#include <FastLED.h>

// How many leds in your strip?
#define NUM_LEDS 45

// For led chips like WS2812, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
// Clock pin only needed for SPI based chipsets when not using hardware SPI
#define DATA_PIN 7

// Define the array of leds
CRGB leds[NUM_LEDS];

int LED = 13;      // pin 13 is given variable LED
int data;              // Variable to store data

void setup()
{
      // Uncomment/edit one of the following lines for your leds arrangement.
    // ## Clockless types ##
    FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);  // GRB ordering is typical
    Serial.begin(9600);              //setting baud rate for communication
    pinMode(LED,OUTPUT);    //Pin 13 set as output
    digitalWrite(LED,LOW);       //LED is off by default
}
void loop()
{

while(Serial.available())                                 //check if data is available
  {
  data = Serial.read();                                       //while data is available read the data
  }

if(data == '1')                                                  //if data is value '1'
{
  for(int i=0; i<45; i++){
    leds[i] = CRGB(255,255,255);
    FastLED.show();
    //delay(500);
  }                  //print output on serial monitor
}
else if(data == '0')                                          //if data is value '0'
{
  for(int i=0; i<45; i++){
    leds[i] = CRGB(0,0,0);
    FastLED.show();
    //delay(500);
  }                        //print output on serial monitor
}
}