#include <MCP42010.h>
#include "math_functions.h"
MCP42010 digipot(10,13,11);

#define EN_COIL 2
#define REV_COIL 3
#define FOR_COIL 4

bool dir; // false = forward, true = reverse
uint8_t alt_dir; // used to get the relatively smoothed curve
uint8_t inten;

void setup() {
  // put your setup code here, to run once:
    dir = 0;
    alt_dir = 0; // 0 = pos positve slope, 1 = pos neg slope, 2 = neg neg slope, 3 = neg pos slope
    inten = 0;
    pinMode(EN_COIL, OUTPUT);
    pinMode(REV_COIL, OUTPUT);
    pinMode(FOR_COIL, OUTPUT);
    set_coil_output(inten,dir);
    Serial.begin(9600);
    Serial.println("beginning magnetic field generation");
}

//note the potentiometer is currently reversed so higher .setPot equates to a lower voltage. Inconvient but will be fixed later.
void set_coil_output(uint8_t volt, bool dir)
{
    digipot.setPot(1,255-(volt));
    digitalWrite(EN_COIL, (volt == 0) ? 0 : 1);
    digitalWrite(REV_COIL, !dir);
    digitalWrite(FOR_COIL, dir);
}

void loop() {
  // order of sending command, first byte indicates dir, second byte indicates intensity (only up to 8 bit of precision).
  if (Serial.available() > 0)
  {
    //dir = (Serial.read() != 0) ? 0 : 1;
    //inten = (int) Serial.read() % 150; 
  }
  sine_demo();
  set_coil_output(inten,dir);

  delay(200);
  Serial.print("curr dir: "); Serial.print((!dir) ? "Forward" : "Reversed");
  Serial.print("  curr inten: "); Serial.println(inten); 
}

void sine_demo()
{
	double time_multiplier = (double) millis()/100000; // x in the sin function is time *2pi

	double inten_temp = range_limit(151*sin((float) (time_multiplier* PI)),-151,151);

	inten = abs((int)inten_temp);

	dir = (inten_temp >= 0) ? 1 : 0;
} 


void triag_demo()
{
	switch (alt_dir)
	{
		case 0:
			if (inten == 151)
			{
				alt_dir = 1;
				dir = 0;
			}
			else
			{
				dir = 0;
				inten += 1;
			}
		break;
		case 1:
			if (inten == 0)
			{
				alt_dir = 2;
				dir = 1;
			}
			else
			{
				inten -= 1;
				dir =0;	
			}
		break;
		case 2:
			if (inten == 151)
			{
				alt_dir = 3;
				dir = 1;
			}
			else
			{
				dir =1;
				inten += 1;
			}
		break;
		case 3:
			if (inten == 0)
			{
				alt_dir = 0;
				dir =0;
			}
			else
			{
				inten -= 1;
				dir =1;
			}
	}
}
