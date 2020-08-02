from pyb import UART
import uos

uos.dupterm(None, 0) #slot 1 should be usb-vcp
# pyb.usb_mode('VCP+VCP+MSC')
uart = UART(4, 115200)
uart.init(115200, bits=8, parity=None, stop=1, timeout=2)

buf = bytearray(10)
nread = 99
def irq_fun(tmp):
    nread = uart.readinto(buf,3)
    print("Received {}: {}\n".format(nread, int(buf[0])))
    uart.write(buf)

uartIRQ = uart.irq(trigger = UART.IRQ_RXIDLE, handler = irq_fun)