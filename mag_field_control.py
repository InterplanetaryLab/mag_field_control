import sys
from MCP42010 import MCP42010
import FaBo9Axis_MPU9250
import RPi.GPIO as GPIO
from simple_pid import PID
import time


class MAG_CONTROL:
    digi_pot = 0
    mpu = 0
    en_coil_pin = -1 # set to -1 as a precaution for checks later in case the pins are not set
    rev_coil_pin = -1
    for_coil_pin = -1
    close_pid = 0

    curr_dir = 0
    curr_en = 0
    curr_mag = 0

    kp = 0
    ki = 0 
    kd = 0

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


    def get_time_delta_sec(prev_time):
        return int(time.time()-prev_time)

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

    def set_pid_parameters(self,kp,ki,kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def set_coil_output_close(self, coil_mag, dir_ind, timeout): # coil mag is in units of microTesla for easy comparison to the MPU9250
        if (kp != 0):
            print "starting closed loop output, target: ", (coil_mag),"\n"

            mag_input = print_mag_output()[dir_ind%3]
            error = mag_input - coil_mag 

            print "error: " int(error), "\n"

            self.pid = PID(self.kp,self.ki,self.kd,setpoint=coil_mag,sample_time=0.01,output_limits=(-150,150))

            time_prev =  time.time()
            while abs(error ) > 10 and get_time_delta_sec(time_prev) < timeout :
                output = int(self.pid(mag_input))
                self.set_coil_output_open_no_dir(output)
                
                mag_input = print_mag_output()[dir_ind%3]
                error = mag_input - coil_mag 
 
                print "error : " int(error), "\n"
                print "curr mag : output :", int(output), "\n"
                print "curr mag : sensor :", mag_input, "\n"
                print "curr_time_delta: ", get_time_delta_sec(time_prev) < timeout

        else:
            print "Error KP constant = 0. Set a value greater than zero"

    def set_coil_output_open_no_dir(self, coil_mag): # in voltage ish but negatives are applied
        if coil_mag >0:
            self.set_coil_output_open(1,abs(coil_mag))
        else:
            self.set_coil_output_open(0,abs(coil_mag))


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
