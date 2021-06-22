from MCP42010 import MCP42010
import FaBo9Axis_MPU9250
import sys
import time
from mag_field_control import MAG_CONTROL


def get_mag_user():
    coil_dir = input(' Enter Coil Dir: 1 or 0 : ')
    coil_mag = input(' Enter Coil mag: 0 to 255: ')
    return [coil_dir,coil_mag]

test = MAG_CONTROL(0,24,22,23)

time_delta_sec = 20 # 10 seconds to wait to get to set point for now
try:
    while True:
        user_out = get_mag_user()
        test.set_coil_output_open(user_out[0],user_out[1])
        last_time = time.time()
        while int(last_time%60)+time_delta_sec > int(time.time()%60):
            test.print_coil_state() 
            time.sleep(.15) 
            test.print_mag_output()

except KeyboardInterrupt:
    test.stop_coil()
    sys.exit()
