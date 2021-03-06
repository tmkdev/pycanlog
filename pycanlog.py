__author__ = 'Terry'
import serial
import sys
import logging
import time
import re

def main(comport, filename, timestamp):
    ser = serial.Serial(port=comport, baudrate=250000, timeout=None)
    file = open(filename, 'wb')
    re_line = re.compile('[TRtr]\d+[ 0-9]+')

    try:
        while True:
            line = ser.readline().strip()
            if re_line.match(line):
                tstamp = time.time()
                print line

                if timestamp:
                    line += " {1}".format(timestamp)

                file.write("{{0}\n".format(line))
            else:
                logging.info("Invalid Line: {0}".format(line))

    except(KeyboardInterrupt, SystemExit):
        ser.close()
        file.close()
        return 0
    except:
        raise

if __name__ == '__main__':
    if len(sys.argv) < 3:
        logging.error("Needs COM port and outputfile args.")
        logging.error("pycanlog.py COMx logfile.log (t or timestamp)")
        exit(1)

    timestamp = false
    if 'timestamp' in sys.argv or 't' in sys.argv:
        timsstamp = True

    comport = sys.argv[1]
    filename = sys.argv[2]

    main(comport, filename, timestamp)
