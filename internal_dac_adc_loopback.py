from pyb import Pin, ADC, DAC, Timer
import time

led = Pin('LED1', Pin.OUT)
#adc_pin = Pin(Pin.cpu.C2, mode=Pin.ANALOG)
adc_pin = Pin(Pin.cpu.C3, mode=Pin.ANALOG)
#adc_pin = Pin(Pin.cpu.A0, mode=Pin.ANALOG)
#adc_pin = Pin(Pin.cpu.A1, mode=Pin.ANALOG)
#adc_pin = Pin(Pin.cpu.B0, mode=Pin.ANALOG) #on testpad
#adc_pin = Pin(Pin.cpu.B1, mode=Pin.ANALOG) #on testpad

dac_pin = Pin(Pin.cpu.A4, mode=Pin.ANALOG)
adc = ADC(adc_pin)
dac = DAC(dac_pin)

tim = Timer(6)
tim.init(freq=5)
tim.counter() # get counter value

def tick(timer):                # we will receive the timer object when being called
    if led.value()==0:
        led.on()
    else:
        led.off()
    print(adc.read())

tim.callback(tick)

time.sleep(10)
tim.deinit()

    