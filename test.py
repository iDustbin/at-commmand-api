#!/usr/bin/env python

import serial

ser = serial.Serial('/dev/tty.usbserial-143130',115200,timeout=None)

while True:
        ser.write(bytes("ATI\r\n", 'utf-8'))
        msg = ser.readline().decode("utf-8")
        #ser.write(msg)
        print(msg)