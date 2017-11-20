#include "mbed.h"
#include "rtos.h"
//Pi mbed USB Slave function
// connect mbed to Pi USB
RawSerial  pi(USBTX, USBRX);
 
DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);
DigitalOut led4(LED4);

char* getOut();

float temp;
float rpm;
float wheel_speed;

void send_data()
{
    while(pi.readable()) 
    {
        while(1)
        {
            pi.puts(getOut());
            Thread::wait(1000);
        }
        Thread::wait(500);
    }    
}

char* getOut()
{
    char output[100];

    snprintf(output, 100, "%f,%f,%f", temp, rpm, wheel_speed);

//    printf("%s", output);
    return output;
}
 
void dev_recv()
{
    char temp = 0;
    led1 = !led1;
    while(pi.readable()) {
        temp = pi.getc();
        pi.putc(temp);
//        if (temp=='1') led2 = 1;
//        if (temp=='0') led2 = 0;
    }
}
int main()
{
    pi.baud(9600);
    pi.attach(&dev_recv, Serial::RxIrq);
    while(1) {
        sleep();
    }
}