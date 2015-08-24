__author__ = 'Terry'
import re
import logging
import json

class CanPacket(object):
    OK = 0
    BADPACKET = 1
    def __init__(self, canid, rtr, ext, err, len, data, canstring=None):
        self.canid = canid
        self.rtr = rtr
        self.ext = ext
        self.err = err
        self.len = len
        self.data = data
        self.canstring = canstring

    @classmethod
    def fromString(cls, canstring):
        #0123456789
        #T0000C04080765A78000000000
        #T00004040704800200001000
        #Following SLCAN - With provision for a timestamp from the serial collector..

        thisData = []

        thisExt = False
        thisRtr = False

        try:
            if canstring[0] in ['T', 'R']:
                thisExt = True
            if canstring[0] in ['r', 'R']:
                thisRtr = True

            if thisExt:
                thisCanId = int(canstring[1:9], 16)
                thisLen = int(canstring[9])
                if thisLen > 0:
                    thisData = [int(x, 16) for x in re.findall('..', canstring[10:])]
            else:
                thisCanId = int(canstring[1:4], 16)
                thisLen = int(canstring[4])
                if thisLen > 0:
                    thisData = [int(x, 16) for x in re.findall('..', canstring[5:])]

            return cls(thisCanId, thisRtr, thisExt, CanPacket.OK, thisLen, thisData, canstring)

        except:
            logging.error("Malformed SLCAN string: {0}".format(canstring))
            return cls(None, thisRtr, thisExt, CanPacket.BADPACKET, 0, [], canstring)

    def packetserialize(self):
        return {
            'canid': self.canid,
            'rtr': self.rtr,
            'ext': self.ext,
            'err': self.err,
            'len': self.len,
            'data': self.data,
            'canstring': self.canstring,
        }

    def asciiData(self):
        return "".join([chr(x) for x in self.data])

class GMLANPacket(CanPacket):
    def __init__(self, canid, rtr, ext, err, len, data, canstring=None):
        CanPacket.__init__(self, canid, rtr, ext, err, len, data, canstring)
        if self.err == GMLANPacket.OK and self.ext:
            self.priority = self.canid >> 26
            self.arbid = ((self.canid) >> 13) & (2**13 -1)
            self.senderid = self.canid & (2**13-1)
        else:
            self.priority = 0
            self.arbid = 0
            self.senderid = 0

    def packetserialize(self):
        packetdict = super(GMLANPacket, self).packetserialize()

        #Include GMLAN specific stuff.
        packetdict['arbid'] = self.arbid
        packetdict['priority'] = self.priority
        packetdict['senderid'] = self.senderid

        return packetdict

if __name__ == '__main__':

    pkt2 = GMLANPacket.fromString("T0000C04080765A78000000000")
    print pkt2.data
    print pkt2.arbid
    print pkt2.senderid
    print pkt2.packetserialize()


