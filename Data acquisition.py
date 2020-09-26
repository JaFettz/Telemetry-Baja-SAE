""" programa de telemetria 


"""
from gpiozero.pins.mock import MockFactory
from gpiozero import Device
import smbus

DEVICE_BUS = 1
DEVICE_ADDR = 0x68

Device.pin_factory = MockFactory()

bus = smbus.SMBus(DEVICE_BUS)
bus.write_byte_data(DEVICE_ADDR,0x6B,0x00)

def setupMPU():
    bus.write_byte_data(DEVICE_ADDR,0x6B,0x00000000)
    bus.write_byte_data(DEVICE_ADDR,0x1B,0x00000000)
    bus.write_byte_data(DEVICE_ADDR,0x1C,0x00000000)
    pass

#setupMPU()

def recordAccelRegisters():
    bus.write_block_data(DEVICE_ADDR,0x3B)

    pass

print(DEVICE_BUS,DEVICE_ADDR,0x3B)