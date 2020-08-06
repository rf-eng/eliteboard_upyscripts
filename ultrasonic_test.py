from umachine import Pin, time_pulse_us
import time

pout = Pin(Pin.cpu.D13, Pin.OUT)
pin = Pin(Pin.cpu.D12, Pin.IN)

pout.off()

while True:
    pout.on()
    time.sleep_us(30)
    pout.off()
    p_duration = time_pulse_us(pin, 1)
    print('duration={} us'.format(p_duration))
    time.sleep_ms(300)