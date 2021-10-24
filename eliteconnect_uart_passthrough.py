from pyb import UART
import select

uart4 = UART(4, 115200, timeout=0, rxbuf=1024)  # to/from PC
uart7 = UART(7, 115200, timeout=0, rxbuf=1024)  # to/from eLITe-Connect

def pass_through(uart1, uart2):
    while True:
        select.select([uart1, uart2], [], [])
        if uart1.any():
            uart2.write(uart1.read(1020))
        if uart2.any():
            uart1.write(uart2.read(1020))

pass_through(uart4, uart7)
