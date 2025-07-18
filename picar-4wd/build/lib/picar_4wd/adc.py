#!/usr/bin/env python3
from .i2c import I2C

class ADC(I2C):
    # Default I2C address of the SunFounder ADC module. Older boards
    # use 0x14 while newer revisions may respond on 0x15.  When the
    # default address fails we fall back to 0x15 automatically.
    ADDR = 0x14

    def __init__(self, chn):    # adc channel:"A0, A1, A2, A3, A4, A5, A6, A7"
        super().__init__()
        if isinstance(chn, str):
            if chn.startswith("A"):     
                chn = int(chn[1:])
            else:
                raise ValueError("ADC channel should be between [A0, A7], not {0}".format(chn))
        if chn < 0 or chn > 7:          
            self._error('Incorrect channel range')
        chn = 7 - chn
        self.chn = chn | 0x10          
        self.reg = 0x40 + self.chn
        # Attempt to communicate using the default address.  If it fails
        # with an I/O error, try the alternative address (0x15).
        try:
            self.send([self.chn, 0, 0], self.ADDR)
            self.recv(1, self.ADDR)
        except OSError as e:
            print(f"I/O error in ADC.__init__: {e}, switching to 0x15")
            self.ADDR = 0x15
        
    def read(self):                     
        self.send([self.chn, 0, 0], self.ADDR)

        # self._debug("Read from 0x%02X"%(self.ADDR))
        # value_h = self.bus.read_byte(self.ADDR)
        value_h = self.recv(1, self.ADDR)[0]            

        # self._debug("Read from 0x%02X"%(self.ADDR))
        # value_l = self.bus.read_byte(self.ADDR)
        value_l = self.recv(1, self.ADDR)[0]           

        value = (value_h << 8) + value_l
        # self._debug("Read value: %s"%value)
        return value


def test():
    import time
    adc = ADC(0)
    while True:
        print(adc.read())
        time.sleep(1)

if __name__ == '__main__':
    test()