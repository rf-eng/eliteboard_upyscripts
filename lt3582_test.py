from machine import I2C
import ustruct
from lt3582 import LT3582

# print([hex(adrl<<1) for adrl in adr])
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

i2c = I2C(2, freq=100000)
adr = 0b1000101

for reg in range(5):
    print("reg {}:".format(reg))
    print(bin(ustruct.unpack("<b", i2c.readfrom_mem(adr, reg, 1))[0]))

lt3582 = LT3582(i2c, adr)

volt_p = 10
volt_n = -10

lt3582.set_voltage(10, -10)



