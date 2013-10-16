
RD_VERSION = 0x00
TURN = 0x01

def getVersion(dev):
    dev.send([RD_VERSION])
    raw = dev.read(3)
    return raw[1] + raw[2] * 256

def turn(dev, on):
    msg = [TURN, on]
    dev.send(msg)
    raw = dev.read(1)
    return raw[0]

