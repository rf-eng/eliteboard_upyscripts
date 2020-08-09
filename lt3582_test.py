from machine import I2C
import ustruct
from lt3582 import LT3582

i2c = I2C(2, freq=100000)
adr = 0b1000101

for reg in range(5):
    print("reg {}:".format(reg))
    print(bin(ustruct.unpack("<b", i2c.readfrom_mem(adr, reg, 1))[0]))

lt3582 = LT3582(i2c, adr)

volt_p = 10
volt_n = -10

lt3582.set_voltage(10, -10)



