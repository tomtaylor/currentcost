#!/usr/bin/env python
import serial
from xml.etree.cElementTree import fromstring
import time
import csv
import signal
import sys

serial = serial.Serial('/dev/ttyUSB0', 57600)

with open('/srv/currentcost/currentcost.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)

    def signal_term_handler(signal, frame):
        csvfile.flush()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_term_handler)

    try:
        while True:
            msg = serial.readline()
            if not msg:
                raise ValueError('Time out')

            xml = fromstring(msg)

            if xml.tag != 'msg':
                continue

            if xml.find('hist'):
                continue

            watts = int(xml.find('ch1').find('watts').text)

            now = time.time()
            timestamp = int(now)

            row = [timestamp, watts]
            writer.writerow(row)
    except KeyboardInterrupt:
        csvfile.flush()
