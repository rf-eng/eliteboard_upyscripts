from umachine import Pin
import time

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
    