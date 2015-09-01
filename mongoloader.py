__author__ = 'Terry'
from pymongo import MongoClient
import canlib
import re
import logging

if __name__ == '__main__':
    logname ='ctsv_candump_1.log'
    re_line = re.compile('[TRtr]\d+[ 0-9]*')

    mongohost = '192.168.1.41'
    client = MongoClient(mongohost, 27017)

    file = open(logname, 'rb')

    db = client.gmlan
    packetdb=db.gmlan_packets

    packetdb.remove({'filename': logname})

    packets = []

    for line in file:
        thisPacket = canlib.GMLANPacket.fromCandump(line.strip())
        packetDict = thisPacket.packetserialize()
        packetDict['filename'] = logname
        logging.error("Inserting {0}".format(thisPacket.arbid))
        packets.append(packetDict)

    packetdb.insert_many(packets)

    file.close()
