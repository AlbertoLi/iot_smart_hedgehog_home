#include "mbed.h"
#include "SDFileSystem.h"
#include "wave_player.h"
#include "rtos.h"
Serial pc(USBTX, USBRX);
SDFileSystem sd(p5, p6, p7, p8, "sd"); // the pinout on the mbed Cool Components workshop board
AnalogOut DACout(p18);
//On Board Speaker
//PwmOut PWMout(p25);
wave_player waver(&DACout);

int main() {

	//FILE *wave_file = fopen("/sd/wavfiles/crickets.wav","r");
	//if(wave_file == NULL) {
	//        pc.printf(" AAAHHHHHHHHHHHHHHHH");
	//    }
	while (true) {
		FILE *wave_file = fopen("/sd/wavfiles/crickets.wav", "r");
		waver.play(wave_file);
		pc.printf(" PPPPPPOOOOOOOOOOOOOOOOOOOOOOOOPPPPPP");
		fclose(wave_file);
		Thread::wait(1000);
	}
}
