#include "mbed.h"

//Print temperature from LM61 analog temperature sensor

//set p15 to analog input to read LM61 sensor's voltage output
AnalogIn LM61(p15);

//also setting unused analog input pins to digital outputs reduces A/D noise a bit
//see http://mbed.org/users/chris/notebook/Getting-best-ADC-performance/
DigitalOut P16(p16);
DigitalOut P17(p17);
DigitalOut P18(p18);
DigitalOut P19(p19);
DigitalOut P20(p20);

int main()
{
    float tempC, tempF;

    while(1) {
        //conversion to degrees C - from sensor output voltage per LM61 data sheet
        tempC = ((LM61*3.3)-0.600)*100.0;
        //convert to degrees F
        tempF = (9.0*tempC)/5.0 + 32.0;
        //print current temp
        printf("%5.2F C %5.2F F \n\r", tempC, tempF);
        wait(.5);
    }
}