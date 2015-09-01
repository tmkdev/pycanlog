__author__ = 'Terry'
import re
import logging
import json

class CanPacket(object):
    OK = 0
    BADPACKET = 1
    def __init__(self, canid, rtr, ext, err, len, data, canstring=None, timestamp=None):
        self.canid = canid
        self.rtr = rtr
        self.ext = ext
        self.err = err
        self.len = len
        self.data = data
        self.canstring = canstring
        self.timestamp = timestamp

    @classmethod
    def fromString(cls, canstring):
        #0123456789
        #T0000C04080765A78000000000
        #T00004040704800200001000
        #Following SLCAN - With provision for a timestamp from the serial collector..

        thisData = []

        thisExt = False
        thisRtr = False

        timestamp = None

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

            return cls(thisCanId, thisRtr, thisExt, CanPacket.OK, thisLen, thisData, canstring, timestamp)

        except:
            logging.error("Malformed SLCAN string: {0}".format(canstring))
            return cls(None, thisRtr, thisExt, CanPacket.BADPACKET, 0, [], canstring)

    @classmethod
    def fromCandump(cls, canstring):
        # (1441054535.204928)  can0   C050040  [8] 00 A0 00 00 00 00 3C 00
        # (1441054535.210110)  can0   C052040  [8] 00 00 9C 00 06 4D 43 46
        # (1441054535.213229)  can0  1005C040  [2] 00 00
        # (1441054535.216882)  can0  1005E040  [5] 00 00 30 00 03
        # (1441054535.222535)  can0  10028040  [8] 1F 00 80 5F 8F 8C 29 03

        thisData = []

        thisExt = False
        thisRtr = False

        canregex = re.compile('[ ]?\(([0-9.]+)\)  ([a-z]+[0-9])  ([ 0-9A-F]+)  \[([0-8])][ ]?([0-9A-F ]*)')

        canmatch = canregex.match(canstring)

        if canmatch:
            try:
                timestamp = float(canmatch.group(1))

                thisLen = canmatch.group(4)
                datastring = canmatch.group(5).split()

                thisData = [int(x, 16) for x in datastring]

                thisCanId = canmatch.group(3)
                if len(thisCanId) > 3:
                    thisExt = True

                thisCanId = int(thisCanId, 16)

                return cls(thisCanId, thisRtr, thisExt, CanPacket.OK, thisLen, thisData, canstring, timestamp)

            except:
                logging.error("Malformed CANDUMP string: {0}".format(canstring))
                return cls(None, thisRtr, thisExt, CanPacket.BADPACKET, 0, [], canstring)

        else:
            logging.error("Malformed CANDUMP string. {0}".format(canstring))
            return cls(None, 0, 0, CanPacket.BADPACKET, 0, [], canstring)

    def packetserialize(self):
        return {
            'canid': self.canid,
            'rtr': self.rtr,
            'ext': self.ext,
            'err': self.err,
            'len': self.len,
            'data': self.data,
            'canstring': self.canstring,
            'timestamp': self.timestamp,
        }

    def asciiData(self):
        return "".join([chr(x) for x in self.data])

class GMLANPacket(CanPacket):
    def __init__(self, canid, rtr, ext, err, len, data, canstring=None, timestamp=None):
        CanPacket.__init__(self, canid, rtr, ext, err, len, data, canstring, timestamp)
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

    pkt2 = GMLANPacket.fromCandump(" (1441054535.204928)  can0   C050040  [8] 00 A0 00 00 00 00 3C 00")
    print(pkt2.data)
    print(pkt2.arbid)
    print(pkt2.timestamp)
    print(pkt2.packetserialize())


