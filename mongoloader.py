__author__ = 'Terry'
from pymongo import MongoClient
import canlib
import re
import logging

if __name__ == '__main__':
    logname ='ctsv_20150823.log'
    re_line = re.compile('[TRtr]\d+[ 0-9]*')

    mongohost = '192.168.1.41'
    client = MongoClient(mongohost, 27017)

    file = open(logname, 'rb')

    db = client.gmlan
    packetdb=db.gmlan_packets

    packetdb.remove({'filename': logname})

    packets = []

    for line in file:
        if re_line.match(line):
            thisPacket = canlib.GMLANPacket.fromString(line.strip())
            packetDict = thisPacket.packetserialize()
            packetDict['filename'] = logname
            packetdb.insert(packetDict)
        else:
            logging.error("Invalid Line: {0}".format(line))

    file.close()
