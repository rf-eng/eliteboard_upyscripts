from machine import I2C

i2c = I2C(2, freq=100000)
adr = i2c.scan()
print([hex(adrl<<1) for adrl in adr])
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

