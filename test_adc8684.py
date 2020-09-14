import machine
import time

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
    
spi = machine.SPI(1, baudrate=156250, polarity=0, phase=1, bits=8)
cs = machine.Pin('G10', mode=machine.Pin.OUT)
cs.high()

cmd = 0xC000  # man ch 0
try:
    while(True):
        valraw = adc8684_cmd(spi, cs, cmd)
        print((valraw-2**15)*312.5e-6)  # todo: check scaling
        time.sleep(0.1)
except KeyboardInterrupt:
    print('Good bye')
except:
    raise