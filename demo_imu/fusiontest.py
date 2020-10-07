from machine import Pin, UART
import math
import pyb
import utime as time
from fusion import Fusion

import busio
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_lis3mdl as lis3mdl
from adafruit_lsm6ds import LSM6DS33, LSM6DSOX, ISM330DHCT, Rate, AccelRange, GyroRange

i2c = busio.I2C()
magsensor = lis3mdl.LIS3MDL(i2c, address=30) # lis address = 30 decimal

lsmsensor = LSM6DSOX(i2c, address=107)
lsmsensor.accelerometer_range = AccelRange.RANGE_8G
print(
    "Accelerometer range set to: %d G" % AccelRange.string[lsmsensor.accelerometer_range]
)

lsmsensor.gyro_range = GyroRange.RANGE_2000_DPS
print("Gyro range set to: %d DPS" % GyroRange.string[lsmsensor.gyro_range])

lsmsensor.accelerometer_data_rate = Rate.RATE_1_66K_HZ
# sensor.accelerometer_data_rate = Rate.RATE_12_5_HZ
print("Accelerometer rate set to: %d HZ" % Rate.string[lsmsensor.accelerometer_data_rate])

lsmsensor.gyro_data_rate = Rate.RATE_1_66K_HZ
print("Gyro rate set to: %d HZ" % Rate.string[lsmsensor.gyro_data_rate])

fuse = Fusion()

uart = UART(4)
uart.init(115200, bits=8, parity=None, stop=1)

count = 0
while True:
    imu_accel_xyz = lsmsensor.acceleration
    tmpgyro = lsmsensor.gyro
    tmpgyro = (math.degrees(tmpgyro[0]), math.degrees(tmpgyro[1]), math.degrees(tmpgyro[2]))
    imu_gyro_xyz = tmpgyro    
    imu_mag_xyz = magsensor.magnetic
    
    #fuse.update(imu_accel_xyz, imu_gyro_xyz, imu_mag_xyz) # Note blocking mag read
    fuse.update_nomag(imu_accel_xyz, imu_gyro_xyz)
    if count % 5 == 0:
        print("Heading, Pitch, Roll: {:7.3f} {:7.3f} {:7.3f}".format(fuse.heading, fuse.pitch, fuse.roll))
    uart.write("{:7.3f},{:7.3f},{:7.3f}\n".format(fuse.heading, fuse.pitch, fuse.roll))
    time.sleep_ms(10)
    count += 1