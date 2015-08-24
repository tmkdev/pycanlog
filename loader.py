__author__ = 'Terry'

import canlib

if __name__ == '__main__':

    file = open('ctsv_20150823.log', 'rb')

    for line in file:
        thisPacket = canlib.GMLANPacket.fromString(line.strip())
        if thisPacket.ext and thisPacket.err == canlib.CanPacket.OK and thisPacket.arbid in [ 0x001 ]:
            print hex(thisPacket.arbid), hex(thisPacket.senderid), thisPacket.data
            print thisPacket.packetserialize()
            print thisPacket.asciiData()

    file.close()
