__author__ = 'Terry'
from pymongo import MongoClient
import canlib


if __name__ == '__main__':
    logname ='ctsv_20150823.log'
    mongohost = '192.168.1.41'
    client = MongoClient(mongohost, 27017)

    file = open(logname, 'rb')

    db = client.gmlan
    collection = db.gmlan_packets

    collection.remove({'filename': logname})

    for line in file:
        thisPacket = canlib.GMLANPacket.fromString(line.strip())
        packetDict = thisPacket.packetserialize()
        packetDict['filename'] = logname

        insertid = collection.insert_one(packetDict).inserted_id
        print insertid

    file.close()
