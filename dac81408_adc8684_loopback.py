import machine
import time
from machine import I2C
import ustruct

from micropython import const

_LT3582_REG0_ADR = const(0x0)
_LT3582_REG1_ADR = const(0x1)
_LT3582_REG2_ADR = const(0x2)
_LT3582_CMDR_ADR = const(0x4)

_LT3582_VPLUS_BIT_NUM = const(5)
_LT3582_PDDIS_BIT_NUM = const(2)
_LT3582_PUSEQ_BIT_NUM = const(0)
_LT3582_PUSEQ_MASK = const(0b11)

_LT3582_RSEL2_BIT_NUM = const(2)
_LT3582_RSEL1_BIT_NUM = const(1)
_LT3582_RSEL0_BIT_NUM = const(0)

class LT3582:
    def __init__(self, i2c, adr):
        self.i2c = i2c
        self.address = adr #0b1000101
        
    def set_voltage(self, volt_p, volt_n):
        if (volt_p < 0) or (volt_p > 10) or (volt_n > 0) or (volt_n < -10):
            raise(ValueError("pos./neg. voltage must not exceed +/- 10V"))
        cmdrval = int((1<<_LT3582_RSEL2_BIT_NUM) | (1<<_LT3582_RSEL1_BIT_NUM) | (1<<_LT3582_RSEL0_BIT_NUM))
        data = ustruct.pack("<b", cmdrval)
        self.i2c.writeto_mem(self.address, _LT3582_CMDR_ADR, data)
        
        reg0val=int((volt_p-3.2)/50e-3)
        vplusbit=None;

        if (abs(volt_p-(3.2+reg0val*50e-3)) < abs(volt_p-(3.2+reg0val*50e-3+25e-3))):
            vplusbit=0
        else:
            vplusbit=1

        data = ustruct.pack("<b", reg0val)
        self.i2c.writeto_mem(self.address, _LT3582_REG0_ADR, data)

        reg1val = int(-(volt_n+1.2)/50e-3)
        data = ustruct.pack("<b", reg1val)
        self.i2c.writeto_mem(self.address, _LT3582_REG1_ADR, data)

        reg2val = int((vplusbit<<_LT3582_VPLUS_BIT_NUM) | (1<<_LT3582_PDDIS_BIT_NUM) | _LT3582_PUSEQ_MASK)
        data = ustruct.pack("<b", reg2val)
        self.i2c.writeto_mem(self.address, _LT3582_REG2_ADR, data)


DAC81408_DEVICEID = 0x01
DAC81408_SPICONFIG = 0x03
DAC81408_DACPWDWN = 0x09
DAC81408_GENCONFIG = 0x04
DAC81408_SYNCCONFIG = 0x06
DAC81408_BRDCONFIG = 0x05
DAC81408_DACRANGE0 = 0x0B
DAC81408_DACRANGE1 = 0x0C
DAC81408_DAC0 = 0x14
DAC81408_DAC1 = 0x15
DAC81408_DAC2 = 0x16
DAC81408_DAC3 = 0x17
DAC81408_DAC4 = 0x18
DAC81408_DAC5 = 0x19
DAC81408_DAC6 = 0x1A
DAC81408_DAC7 = 0x1B

def dac81408_writeReg(spi, cs, adr, val):
    data = ((adr & 0b111111) << 16) | (val)
    dat = data.to_bytes(3, 'big')
    cs.low()
    spi.write(dat)
    cs.high()
    
def dac81408_readReg(spi, cs, adr):
    dataTx=(1<<23) | ((adr & 0b111111) << 16) | (0)
    dat = dataTx.to_bytes(3, 'big')
    cs.low()
    spi.write(dat)
    cs.high()
    ba = bytearray(3)
    cs.low()
    spi.write_readinto(dataTx.to_bytes(3, 'big'), ba)
    cs.high()
    
    dataRx = int.from_bytes(ba, 'big')
    retval = dataRx & 0xFFFF
    adr_rx = ((( dataRx & (~(1<<23)))&(0xFF0000))>>16)
    if adr_rx != adr:
        print("wrong adr {} instead of {}".format(adr_rx, adr))
    return retval

#def dac81408_set_range(cfg_string):

i2c = I2C(2, freq=100000)
adr = 0x62>>1
lt3582 = LT3582(i2c, adr)

volt_p = 10
volt_n = -10

for reg in range(5):
    print("reg {}:".format(reg))
    print(bin(ustruct.unpack("<b", i2c.readfrom_mem(adr, reg, 1))[0]))

lt3582.set_voltage(volt_p, volt_n)

time.sleep_ms(100)

spi = machine.SPI(2, baudrate=156250, polarity=0, phase=1, bits=8)
cs = machine.Pin('I0', mode=machine.Pin.OUT)
cs.high()

val = 0b0101010100100 & (~(1<<5)) #disable power down
dac81408_writeReg(spi, cs, DAC81408_SPICONFIG, val)

retval = dac81408_readReg(spi, cs, DAC81408_DEVICEID) #read chip id

if (retval>>2) != 0x298:
    print('did not receive correct device id of DAC81408')
    print('got: {} instead of 0x298'.format(hex(retval>>2)))

#error+=dac81408_set_range(self, bipo_10);
dac81408_writeReg(spi, cs, DAC81408_DACRANGE0, 0xAAAA)  # -10 to 10 V
dac81408_writeReg(spi, cs, DAC81408_DACRANGE1, 0xAAAA)  # -10 to 10 V
dac81408_writeReg(spi, cs, DAC81408_DACPWDWN, 0xF00F)  # disable power down    
dac81408_writeReg(spi, cs, DAC81408_GENCONFIG, 0b0011111100000000)  # enable internal reference
dac81408_writeReg(spi, cs, DAC81408_SYNCCONFIG, 0x0)  # asynchronous mode -> writing to DAC register immediately changes analog voltage
dac81408_writeReg(spi, cs, DAC81408_BRDCONFIG, 0b1111000000001111)  # ignore BRDCAST commands

dac81408_writeReg(spi, cs, DAC81408_DAC0, 50000)
dac81408_writeReg(spi, cs, DAC81408_DAC1, 10000)


def adc8684_writeReg(spi, cs, adr, val):
    data = ((adr & 0b1111111) << 9) | 1 << 8| (val & 0xFF)
    dat = data.to_bytes(2, 'big')
    cs.low()
    spi.write(dat)
    cs.high()
    
def adc8684_readReg(spi, cs, adr):
    dataTx=((adr & 0b1111111) << 17) 
    dat = dataTx.to_bytes(3, 'big')
    ba = bytearray(3)
    cs.low()
    spi.write_readinto(dataTx.to_bytes(3, 'big'), ba)
    cs.high()
    
    dataRx = int.from_bytes(ba, 'big')
    retval = dataRx & 0xFFFF
    
    return retval
    
def adc8684_cmd(spi, cs, cmd):
    dataTx = cmd << 16 | 0xFFFF
    ba = bytearray(4)
    cs.low()
    spi.write_readinto(dataTx.to_bytes(4, 'big'), ba)
    cs.high()
    
    dataRx = int.from_bytes(ba, 'big')
    return dataRx


time.sleep_ms(100)
spi = machine.SPI(1, baudrate=156250, polarity=0, phase=1, bits=8)
cs2 = machine.Pin('G10', mode=machine.Pin.OUT)
cs2.high()

cmd = 0xC000  # man ch 0
try:
    while(True):
        valraw = adc8684_cmd(spi, cs2, cmd)
        print((valraw-2**15)*312.5e-6)  # todo: check scaling
        time.sleep(0.1)
except KeyboardInterrupt:
    print('Good bye')
except:
    raise
