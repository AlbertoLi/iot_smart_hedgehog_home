// Hello World to sweep a servo through its full range

#include "mbed.h"
#include "Servo.h"

Servo myservo(p21);

int main() {
    while (1) {
        myservo = 1; //closed position
        wait(10);
        myservo = .7; //open position
        wait(.3); // open for .3 secs delivers half a small tupperware
        myservo = 1;
//        for(float p=0; p<2.0; p += 0.1) {
//            myservo = p;
//            wait(0.2);
//        }
        wait(.5);
    }
}
