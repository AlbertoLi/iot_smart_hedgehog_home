#include "mbed.h"

Serial pc(USBTX, USBRX);
Timer t;
InterruptIn risingEdge(p5);

DigitalOut myled(LED1);
DigitalOut myled2(LED2);

volatile long int count;

void pulses() {
	if (myled2 == 1) {
		myled2 = 0;
	}
	else {
		myled2 = 1;
	}
	count++;
}

int main() {
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
		pc.printf(" %0.2f RPM", rpm);
		pc.printf(" speed: %f m/s", speed);
		pc.putc(0xA);
		pc.putc(0xD);
	}
}