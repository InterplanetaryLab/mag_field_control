from MCP42010 import MCP42010
import FaBo9Axis_MPU9250
import sys
import time

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

test = MCP42010()
try:
    test.setup_pot(0)
    test.set_pot(255,1)
    while True:
       test.set_pot(255,1)

       time.sleep(.15) 
       mag = mpu9250.readMagnet()
       print " mx = " , ( mag['x'] )
       print " my = " , ( mag['y'] )
       print " mz = " , ( mag['z'] )

except KeyboardInterrupt:
    test.close()
    sys.exit()
