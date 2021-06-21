from MCP42010 import MCP42010
import FaBo9Axis_MPU9250
import sys
import time
from mag_field_control import MAG_CONTROL


test = MAG_CONTROL(0,22,23,24)
try:
    while True:
        #test.set_coil_output_open(1,255)
        test.print_coil_state()
        
        time.sleep(.15) 
        test.print_mag_output()

except KeyboardInterrupt:
    test.stop_coil()
    sys.exit()
