__author__ = 'Terry'
import canlib
import re
import logging

if __name__ == '__main__':
    file = open('ctsv_20150823.log', 'rb')
    re_line = re.compile('[TRtr]\d+[ 0-9]*')
    arbids = [0x055]


    for line in file:
        if re_line.match(line):
            thisPacket = canlib.GMLANPacket.fromString(line.strip())
            if thisPacket.ext and thisPacket.err == canlib.CanPacket.OK and thisPacket.arbid in arbids:
                print hex(thisPacket.arbid), hex(thisPacket.senderid), thisPacket.data
                print thisPacket.packetserialize()
                print thisPacket.asciiData()
        else:
            logging.error("Invalid Line: {0}".format(line))

    file.close()
