
RD_VERSION = 0x00
SET_VEL_2MTR = 0x01
SET_VEL_MTR = 0x02
TEST_MOTORS = 0x03
GET_TYPE = 0x04

def getVersion(dev):
    dev.send([RD_VERSION])
    raw = dev.read(3)
    return raw[1] + raw[2] * 256

def setvel2mtr(dev, sentido1, vel1, sentido2, vel2):
    msg = [SET_VEL_2MTR, sentido1, vel1 / 256, vel1 % 256, sentido2, vel2 / 256, vel2 % 256]
    dev.send(msg)
    raw = dev.read(1)
    return raw[0]

def setvelmtr(dev, motor_id, sentido, vel):
    msg = [SET_VEL_MTR, motor_id, sentido, vel / 256, vel % 256]
    dev.send(msg)
    raw = dev.read(1)
    return raw[0]

def testMotors(dev):
    dev.send([TEST_MOTORS])
    raw = dev.read(1)
    return raw[0]

def getType(dev):
    dev.send([GET_TYPE])
    raw = dev.read(2)
    return raw[1]

