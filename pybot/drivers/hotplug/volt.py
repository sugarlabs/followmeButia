
import math

RD_VERSION = 0x00
GET_VALUE = 0x01

VCC = 65536

def getVersion(dev):
    dev.send([RD_VERSION])
    raw = dev.read(3)
    return raw[1] + raw[2] * 256

def getValue(dev):
    dev.send([GET_VALUE])
    raw = dev.read(3)
    volt = (raw[1] + raw[2] * 256) * 5.0 / VCC
    return math.floor(volt * 1000.0) / 1000

