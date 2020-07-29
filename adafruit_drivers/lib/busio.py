"""
`busio` - Bus protocol support like I2C and SPI
=================================================

See `CircuitPython:busio` in CircuitPython for more details.

* Author(s): cefn
"""

from adafruit_blinka import Enum, Lockable

# pylint: disable=import-outside-toplevel,too-many-branches,too-many-statements
# pylint: disable=too-many-arguments,too-many-function-args


class I2C(Lockable):
    """
    Busio I2C Class for CircuitPython Compatibility. Used
    for both MicroPython and Linux.
    """

    def __init__(self, frequency=400000):
        self.init(frequency)

    def init(self, frequency):
        """Initialization"""
        self.deinit()
        from machine import I2C as _I2C
        self._i2c = _I2C(2, freq=frequency)
        #self._lock = threading.RLock()

    def deinit(self):
        """Deinitialization"""
        try:
            del self._i2c
        except AttributeError:
            pass

    def __enter__(self):
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._lock.release()
        self.deinit()

    def scan(self):
        """Scan for attached devices"""
        return self._i2c.scan()

    def readfrom_into(self, address, buffer, *, start=0, end=None):
        """Read from a device at specified address into a buffer"""
        if start != 0 or end is not None:
            if end is None:
                end = len(buffer)
            buffer = memoryview(buffer)[start:end]
        stop = True  # remove for efficiency later
        return self._i2c.readfrom_into(address, buffer, stop)

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        """Write to a device at specified address from a buffer"""
        if isinstance(buffer, str):
            buffer = bytes([ord(x) for x in buffer])
        if start != 0 or end is not None:
            if end is None:
                return self._i2c.writeto(address, memoryview(buffer)[start:], stop)
            return self._i2c.writeto(address, memoryview(buffer)[start:end], stop)
        return self._i2c.writeto(address, buffer, stop)

    def writeto_then_readfrom(
        self,
        address,
        buffer_out,
        buffer_in,
        *,
        out_start=0,
        out_end=None,
        in_start=0,
        in_end=None,
        stop=False
    ):
        """"Write to a device at specified address from a buffer then read
        from a device at specified address into a buffer
        """
        # If we don't have a special implementation, we can fake it with two calls
        self.writeto(address, buffer_out, start=out_start, end=out_end, stop=False)
        self.readfrom_into(address, buffer_in, start=in_start, end=in_end)
        return 
