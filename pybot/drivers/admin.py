
MESSAGE = 0x02
LOAD = 0x03
UNLOAD = 0x04
GET_USER_MODULES_SIZE = 0x05
GET_USER_MODULES_LINE = 0x06
BOOT = 0x09
GET_HANDLER_SIZE = 0x0A
GET_HANDLER_TYPE = 0x0B
GET_FIRMWARE_VERSION = 0xFE
RESET = 0xFF

def getVersion(dev):
    dev.send([GET_FIRMWARE_VERSION])
    raw = dev.read(2)
    return raw[1]

def send(dev, data):
    msg = [MESSAGE] + dev.to_ord(data[0])
    dev.send(msg)
    raw = dev.read(len(msg))
    return dev.to_text(raw[1:])

def reset(dev):
    dev.send([RESET])

