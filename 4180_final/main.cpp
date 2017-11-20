#include "mbed.h"
#include "Servo.h"
#include "rtos.h"
RawSerial  pi(USBTX, USBRX);
Mutex serial_mutex;

Servo myservo(p21);
AnalogIn LM61(p15);


volatile float temp_out;
volatile float rpm_out;
volatile float wheel_speed_out;

DigitalOut myled1(LED1);
DigitalOut myled2(LED2);

volatile long int count;

Serial pc(USBTX, USBRX);
Timer t;
InterruptIn risingEdge(p5);


void check_temp() {
    float tempC, tempF;

    while(1) {
        //conversion to degrees C - from sensor output voltage per LM61 data sheet
        tempC = ((LM61*3.3)-0.600)*100.0;
        //convert to degrees F
        tempF = (9.0*tempC)/5.0 + 32.0;
        temp_out = tempF;
        //print current temp
        printf("%5.2F C %5.2F F \n\r", tempC, tempF + 16.7);
        Thread::wait(500);
    }    
}

void deliver_snack()
{
    myservo = 1; //closed position
    Thread::wait(1000);
    myservo = .7; //open position
    Thread::wait(200); // open for .2 secs delivers half a small tupperware
    myservo = 1;

    Thread::wait(500);    
}




char* getOut()
{
    char output[100];

    snprintf(output, 100, "%f,%f,%f", temp_out, rpm_out, wheel_speed_out);

//    printf("%s", output);
    return output;
}

void send_data() {
    while(1)
    {
        pi.puts(getOut());
        Thread::wait(1000);
    }
}
 
void send_data()
{
    while(pi.readable()) 
    {
        char command = pi.getc();
        switch(command){
            case 'k':
                //drop a snack
                deliver_snack();
            case 'g':
                //play a song
                
            case 'a':
                //start data stream (mbed to pi)
                Thread t4(send_data);
        }
    }    
}

void pulses() {
    if (myled2 == 1) {
        myled2 = 0;
    }
    else {
        myled2 = 1;
    }
    count++;
}

void check_wheel() {
    risingEdge.rise(&pulses);
    while (1) {
        t.reset();
        t.start();
        count = 0;
        while (t.read_ms() < 1001) {
            ;
        }
        t.stop();
        long int temp = count;
        pc.printf("Count: %d", temp);
        double circumference = 0.06 * 3.1416; // 6 cm wheel diameter * pi 
        double rev = (double)temp;
        double rpm = rev * 60;
        double speed = circumference * rev;
        rpm_out = (float) rpm;
        wheel_speed_out = (float) speed;
//        pc.printf(" %0.2f// RPM", rpm);
//        pc.printf(" speed: %f m/s", speed);
//        pc.putc(0xA);
//        pc.putc(0xD);
    }
}


int main() {
    Thread t1(check_temp);
    Thread t2(send_data);
    Thread t3(check_wheel);
    
    pi.baud(9600);
    pi.attach(&pi_interface, Serial::RxIrq);
    
    while (1) {
        Thread::wait(10000000);
    }   
}
