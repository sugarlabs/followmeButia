
RD_VERSION = 0x00
SET_VEL_2MTR = 0x01

def getVersion(dev):
    dev.send([RD_VERSION])
    raw = dev.read(3)
    return raw[1] + raw[2] * 256

def setvel2mtr(dev, sentido1, vel1, sentido2, vel2):
    msg = [SET_VEL_2MTR, sentido1, vel1 / 256, vel1 % 256, sentido2, vel2 / 256, vel2 % 256]
    dev.send(msg)
    raw = dev.read(1)
    return raw[0]

