#include "mbed.h"
#include "Servo.h"
#include "rtos.h"
#include "SDFileSystem.h"
#include "wave_player.h"
RawSerial  pi(USBTX, USBRX);
Mutex serial_mutex;

Servo myservo(p21);
AnalogIn LM61(p15);

SDFileSystem sd(p5, p6, p7, p8, "sd"); // the pinout on the mbed Cool Components workshop board
AnalogOut DACout(p18);
//On Board Speaker
//PwmOut PWMout(p25);
wave_player waver(&DACout);

volatile float temp_out;
volatile float rpm_out;
volatile float wheel_speed_out;
volatile int treat=0;
volatile int music=0;

DigitalOut myled1(LED1);

volatile long int count;

Serial pc(USBTX, USBRX);
Timer t;
InterruptIn risingEdge(p11);

void dev_recv()
{
    char temp = 0;
    myled1 = !myled1;
    while(pi.readable()) {
        temp = pi.getc();
        if (temp=='t') treat=1;
        if (temp=='m') music=1;
    }
}

void check_temp() {
    float tempC, tempF;
    while(1) {
        //conversion to degrees C - from sensor output voltage per LM61 data sheet
        tempC = ((LM61*3.3)-0.600)*100.0;
        //convert to degrees F
        tempF = (9.0*tempC)/5.0 + 32.0;
        temp_out = tempF+16.7;
        //print current temp
        Thread::wait(500);
    }    
}

void deliver_snack()
{
    if(treat=1){
        myservo = 1; //closed position
        Thread::wait(1000);
        myservo = .7; //open position
        Thread::wait(200); // open for .2 secs delivers half a small tupperware
        myservo = 1;
        Thread::wait(500);
        treat=0;
    }    
}




char* getOut()
{
    char output[22];

    snprintf(output, 22, "%f3.1, %f4.0, %f1.5", temp_out, rpm_out, wheel_speed_out);
    return output;
}

void send_data() {
    while(1)
    {
        pi.puts(getOut());
        Thread::wait(5000);
    }
}

void pulses() {
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
        double circumference = 0.06 * 3.1416; // 6 cm wheel diameter * pi 
        double rev = (double)temp;
        double rpm = rev * 60;
        double speed = circumference * rev;
        rpm_out = (float) rpm;
        wheel_speed_out = (float) speed;
    }
}


int main() {
    //printf("Hello, in Main");
    Thread t1(check_temp);
    Thread t2(send_data);
    Thread t3(check_wheel);
    
    pi.baud(9600);
    pi.attach(&dev_recv, Serial::RxIrq);
    
    while (1) {
        if(music==1) {
            FILE *wave_file = fopen("/sd/wavfiles/crickets.wav", "r");
            waver.play(wave_file);
            fclose(wave_file);
            Thread::wait(1000);
            music=0;
        }
    }   
}

