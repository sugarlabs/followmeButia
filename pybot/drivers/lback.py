
RD_VERSION = 0x00
SEND_DATA = 0x01

def getVersion(dev):
    dev.send([RD_VERSION])
    raw = dev.read(3)
    return raw[1] + raw[2] * 256

def send(dev, data):
    msg = [SEND_DATA] + dev.to_ord(data[0])
    dev.send(msg)
    raw = dev.read(len(msg))
    return dev.to_text(raw[1:])

