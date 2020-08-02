import busio
import adafruit_blinka
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_lis3mdl as lis3mdl
import time
from math import atan2, degrees

i2c = busio.I2C()
sensor = lis3mdl.LIS3MDL(i2c, address=30) # lis address = 30 decimal

def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle

def get_heading(_sensor):
    magnet_x, magnet_y, _ = _sensor.magnetic
    return vector_2_degrees(magnet_x, magnet_y)

while True:
    print("heading: {:.2f} degrees".format(get_heading(sensor)))
    time.sleep(0.2)
