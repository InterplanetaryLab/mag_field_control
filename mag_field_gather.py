from MCP42010 import MCP42010
import FaBo9Axis_MPU9250
import sys
import time
from mag_field_control import MAG_CONTROL
import csv

def get_time_delta_sec(prev_time):
    return int(time.time()-prev_time)


test = MAG_CONTROL(0,24,22,23)

time_delta_sec = 2 # 10 seconds to wait to get to set point for now
try:
    with open('mag_data.csv','w') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['x','y','z','en','dir','mag'])
        for mag_dir in range (0,2):
            for mag_mag in range (0,150):
                test.set_coil_output_open(mag_dir,mag_mag)
                last_time = time.time()
                mag_data = []
                while get_time_delta_sec(last_time) < time_delta_sec: # note there is some bug that causes this to miss its time delay or something of the sort
                    test.print_coil_state() 
                    print "time sec: ", int(time.time()%60)
                    time.sleep(.15) 
                    mag_data = test.print_mag_output()
                mag_data.append(test.print_coil_state())
                data_writer.writerow(mag_data)
    
    test.stop_coil()
    sys.exit()

except KeyboardInterrupt:
    test.stop_coil()
    sys.exit()
