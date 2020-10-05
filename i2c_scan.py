from machine import I2C

i2c = I2C(2, freq=100000)
adr_list = i2c.scan()
for adr in adr_list:
    if '0x30' in hex(adr<<1):
        print('I2C One Wire Bridge at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0x50' in hex(adr<<1):
        print('USB-C Controller STUSB at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0x34' in hex(adr<<1):
        print('Audio Codec at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0x3c' in hex(adr<<1):
        print('3D Magnetometer at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0x62' in hex(adr<<1):
        print('Programmable DC/DC Converter at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0xa4' in hex(adr<<1):
        print('I2C EEPROM mem array at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0xb4' in hex(adr<<1):
        print('I2C EEPROM ID page at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0xba' in hex(adr<<1):
        print('Barometer at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0xbe' in hex(adr<<1):
        print('Relative Humidity + Temperature at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0xd6' in hex(adr<<1):
        print('3D Accelerometer + 3D Gyroscope at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0x8a' in hex(adr<<1):
        print('Digital Power Monitor at {}/{}'.format(hex(adr<<1), hex(adr)))
    elif '0x70' in hex(adr<<1):
        print('Port Expander ADC2 at {}/{}'.format(hex(adr<<1), hex(adr)))
    else:
        print('*** Unknown device at {}/{}'.format(hex(adr<<1), hex(adr)))


# '0x30' I2C One Wire Bridge
# '0x34' Audio Codec
# '0x3c' 3D Magnetometer
# '0x70'
# '0x8a' Programmable DC/DC Converter (Digital Power Monitor????)
# '0xa0' I2C EEPROM
# '0xb0' 
# '0xba' Barometer
# '0xbe' Relative Humidity + Temperature
# '0xd6' 3D Accelerometer + 3D Gyroscope

# Port Expander ADC2 0x40
# Digital Power Monitor????


