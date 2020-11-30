from machine import I2C
from umachine import Pin
import time
import struct
import binascii

i2c = I2C(2, freq=100000)

wm8731 = {'adr': 0x1a, 'name': 'WM8731/L Audio Codec', 'ok': False}
lis3mdltr = {'adr': 0x1e, 'name': 'LIS3MDLTR 3D Magnetometer', 'ok': False, 'whoami': 0x3d}
lsm6ds = {'adr': 0x6b, 'name': 'LSM6DSOXTR 3D Accelerometer + 3D Gyroscope', 'ok': False, 'whoami': 0x6c}
lps22hh = {'adr': 0x5d, 'name': 'LPS22HHTR Barometer', 'ok': False, 'whoami': 0xb3}
hts221 = {'adr': 0x5f, 'name': 'HTS221TR Relative Humidity + Temperature', 'ok': False, 'whoami': 0xbc}
m24512_mem = {'adr': 0x52, 'name': 'M24512-DFMC6TG I2C EEPROM mem array', 'ok': False}
m24512_id = {'adr': 0x5a, 'name': 'M24512-DFMC6TG I2C EEPROM ID page', 'ok': False}
lt3582 = {'adr': 0x31, 'name': 'LT3582EUD#PBF Programmable DC/DC Converter', 'ok': False}
isl28023 = {'adr': 0x45, 'name': 'ISL28023FR60Z-T7A Digital Power Monitor', 'ok': False}
tca9534 = {'adr': 0x38, 'name': 'TCA9534APWR Port Expander ADC2', 'ok': False}
ds2482s = {'adr': 0x18, 'name': 'DS2482S-100+T&R I2C One Wire Bridge', 'ok': False}
stusb4500 = {'adr': 0x28, 'name': 'STUSB4500LQTR USB-C controller', 'ok': False}

devices = [wm8731, lis3mdltr, lsm6ds, lps22hh, hts221, m24512_mem,
           m24512_id, lt3582, isl28023, tca9534, ds2482s, stusb4500]

cnt = 0
for dev in devices:
    try:
        i2c.writeto(dev['adr'], bytearray(0))
        # line above throws exception when device is not available
        cnt += 1
        print('{}: {} is responding at {}:'.format(cnt, dev['name'], hex(dev['adr'])), end='')
        if dev == wm8731 or dev == m24512_mem or dev == m24512_id or dev == lt3582:
            # WM8731/L Audio Codec is a write only device
            # EEPROM and LT3582 don't have a builtin ID
            dev['ok'] = True
            print(' ok')
        elif dev == lis3mdltr or dev == lsm6ds or dev == lps22hh or dev == hts221:
            result = i2c.readfrom_mem(dev['adr'], 0xF, 1) #whoami
            if struct.unpack('B',result)[0] == dev['whoami']:
                dev['ok'] = True
                print(' ok')
        elif dev == isl28023:
            result = i2c.readfrom_mem(dev['adr'], 0xAD, 9)  # device id
            if 'ISL28023' in result[1:].decode():  # first byte is len
                dev['ok'] = True
                print(' ok')
        elif dev == tca9534:          
            result = i2c.readfrom_mem(dev['adr'], 2, 1)  # pol. inversion should be 0x00
            if struct.unpack('B',result)[0] == 0:
                result = i2c.readfrom_mem(dev['adr'], 3, 1)  # config should be 0xff
                if struct.unpack('B',result)[0] == 0xff:
                    dev['ok'] = True
                    print(' ok')
        elif dev == ds2482s:
            i2c.writeto_mem(dev['adr'], 0xE1, b'\xf0')  # status register 
            result = i2c.readfrom(dev['adr'], 1)
            if struct.unpack('B',result)[0] == 0x18:
                dev['ok'] = True
                print(' ok')
        elif dev == stusb4500:
            result = i2c.readfrom_mem(dev['adr'], 0x2f , 1)  # password
            if struct.unpack('B',result)[0] == 0x25:
                dev['ok'] = True
                print(' ok')
        else:
            print(dev)
            print('unknown\r')
    except OSError:
        print('\ndevice {} not responding!'.format(dev['name']))
        pass
    
    
problem_dev = [dev for dev in devices if not(dev['ok'])]

if len(problem_dev)>0:
    print('\nErrors occurred in:')
    for dev in problem_dev:
        print(dev['name'])
        
        
print('running LED test')

seg = [Pin('LED{}'.format(i), Pin.OUT) for i in range(1,9)] 
for i in range(8):
    seg[i].off()

for i in range(8):
    seg[i].on()
    time.sleep(0.1)

for i in range(8):
    seg[i].off()
    time.sleep(0.1)

for i in range(8):
    seg[i].off()
    
btn1 = Pin(Pin.cpu.J12, mode=Pin.IN)
btn2 = Pin(Pin.cpu.J13, mode=Pin.IN)

print('Press BTN1 (closer to USB) to continue')
while btn1.value() == 1:
    pass
print('BTN1 ok')

print('Press BTN2 to continue')
while btn2.value() == 1:
    pass
print('BTN2 ok')

print('UID: 0x{}'.format(binascii.hexlify(machine.unique_id()).decode()))
