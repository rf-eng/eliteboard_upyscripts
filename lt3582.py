from micropython import const
import ustruct

_LT3582_REG0_ADR = const(0x0)
_LT3582_REG1_ADR = const(0x1)
_LT3582_REG2_ADR = const(0x2)
_LT3582_CMDR_ADR = const(0x4)

_LT3582_VPLUS_BIT_NUM = const(5)
_LT3582_PDDIS_BIT_NUM = const(2)
_LT3582_PUSEQ_BIT_NUM = const(0)
_LT3582_PUSEQ_MASK = const(0b11)

_LT3582_RSEL2_BIT_NUM = const(2)
_LT3582_RSEL1_BIT_NUM = const(1)
_LT3582_RSEL0_BIT_NUM = const(0)

class LT3582:
    def __init__(self, i2c, adr):
        self.i2c = i2c
        self.address = adr #0b1000101
        
    def set_voltage(self, volt_p, volt_n):
        if (volt_p < 0) or (volt_p > 10) or (volt_n > 0) or (volt_n < -10):
            raise(ValueError("pos./neg. voltage must not exceed +/- 10V"))
        cmdrval = int((1<<_LT3582_RSEL2_BIT_NUM) | (1<<_LT3582_RSEL1_BIT_NUM) | (1<<_LT3582_RSEL0_BIT_NUM))
        data = ustruct.pack("<b", cmdrval)
        self.i2c.writeto_mem(self.address, _LT3582_CMDR_ADR, data)
        
        reg0val=int((volt_p-3.2)/50e-3)
        vplusbit=None;

        if (abs(volt_p-(3.2+reg0val*50e-3)) < abs(volt_p-(3.2+reg0val*50e-3+25e-3))):
            vplusbit=0
        else:
            vplusbit=1

        data = ustruct.pack("<b", reg0val)
        self.i2c.writeto_mem(self.address, _LT3582_REG0_ADR, data)

        reg1val = int(-(volt_n+1.2)/50e-3)
        data = ustruct.pack("<b", reg1val)
        self.i2c.writeto_mem(self.address, _LT3582_REG1_ADR, data)

        reg2val = int((vplusbit<<_LT3582_VPLUS_BIT_NUM) | (1<<_LT3582_PDDIS_BIT_NUM) | _LT3582_PUSEQ_MASK)
        data = ustruct.pack("<b", reg2val)
        self.i2c.writeto_mem(self.address, _LT3582_REG2_ADR, data)
        
