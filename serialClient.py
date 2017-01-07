#!/usr/bin/env python3

import sys
import serial
import readline
import argparse


def rawToBytes(rawinput):
    return bytes(rawinput + "\r\n", encoding="UTF-8")


class SerialClient:

    def __init__(self, port, baudrate=57600, timeout=2):
        ser = serial.Serial()
        ser.baudrate = baudrate
        ser.port = port
        ser.bytesize = 8
        ser.parity = 'N'
        ser.stopbits = 1
        ser.timeout = timeout
        ser.open()
        if not ser.isOpen():
            print('Failed to open serial port %s' % port)
            sys.exit(-1)
        else:
            print('Serial port %s is opened' % port)
            self.ser = ser

    def interactive(self):
        while True:
            try:
                rawinput = input(">>> ").strip()
                if rawinput == '':
                    continue
                if rawinput == "exit":
                    break
                self.ser.write(rawToBytes(rawinput))
                print('>>> %s' % self.ser.readlines())
            except EOFError:
                if self.ser.isOpen():
                    self.ser.close()
                break
            except KeyboardInterrupt:
                if self.ser.isOpen():
                    self.ser.close()
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Serial Client')
    parser.add_argument('dev', help='Path of serial device')
    args = parser.parse_args()

    client = SerialClient(args.dev)
    client.interactive()
