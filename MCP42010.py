import spidev
import sys

class MCP42010:
    spi = 0
    _cs = 0

    def __int__(self):
        self._cs = 0

    def setup_pot(self,CS):
        self._cs = CS
        self.spi = spidev.SpiDev()
        self.spi.open(0,CS)
        self.spi.max_speed_hz = 1000 # 1 khz
        self.spi.mode = 0
        self.spi.lsbfirst=False

    def set_pot(self,value, pot_num):
        data = ((pot_num & 0b11) | 0b00010000)
        self.spi.xfer2([data,value])
    def close(self):
        self.spi.close()

'''
test = MCP42010()
try:
    test.setup_pot(0)
    test.set_pot(50,1)
    while True:
        print("test")

except KeyboardInterrupt:
    test.close()
    sys.exit()
'''
