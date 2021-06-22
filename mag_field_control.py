import sys
from MCP42010 import MCP42010
import FaBo9Axis_MPU9250
import RPi.GPIO as GPIO


class MAG_CONTROL:
    digi_pot = 0
    mpu = 0
    en_coil_pin = -1
    rev_coil_pin = -1
    for_coil_pin = -1

    curr_dir = 0
    curr_en = 0
    curr_mag = 0

    def __init__(self, CS, en_coil_pin, rev_coil_pin, for_coil_pin):
       self.digi_pot = MCP42010()
       self.digi_pot.setup_pot(CS)

       self.en_coil_pin = en_coil_pin
       self.rev_coil_pin = rev_coil_pin
       self.for_coil_pin = for_coil_pin

       GPIO.setmode(GPIO.BCM)
       GPIO.setup(en_coil_pin, GPIO.OUT)
       GPIO.setup(rev_coil_pin, GPIO.OUT)
       GPIO.setup(for_coil_pin, GPIO.OUT)

       self.set_coil_output_open(1,0)

       self.mpu = FaBo9Axis_MPU9250.MPU9250()

    def print_mag_output(self):
        mag = self.mpu.readMagnet()
        x = mag['x']
        y = mag['y']
        z = mag['z']
        print " mx = " , ( x )
        print " my = " , ( y )
        print " mz = " , ( z )
        print
        return [x,y,z]

    def print_coil_state(self):
        print "en_status = ", (self.curr_en)
        print "dir_status = ", (self.curr_dir)
        print "mag_status = ", (self.curr_mag)
        return [self.curr_en,self.curr_dir,self.curr_mag]

    def set_coil_output_open(self, coil_dir, volt):
        self.curr_mag = volt
        self.curr_dir = coil_dir
        self.curr_en = (True if volt != 0 else False)

        self.digi_pot.set_pot(self.curr_mag,1)
        GPIO.output(self.en_coil_pin, self.curr_en) 
        GPIO.output(self.for_coil_pin, self.curr_dir)
        GPIO.output(self.rev_coil_pin, not self.curr_dir)

    def stop_coil(self):
        self.set_coil_output_open(0,0)
        self.digi_pot.close()
        GPIO.cleanup()
