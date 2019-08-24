import time
import serial
import pymodbus
import logging
import math
import threading

from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder


class kom:
    client = ModbusClient(method = "rtu", port="/dev/ttyUSB0",timeout=(1/100), stopbits = 1, bitsize = 32, parity = 'N', baudrate = 115200)
    ser = serial.Serial(port="/dev/ttyACM0", baudrate = 115200, timeout=1)
    path5value = (5, 0)
    speedpath6 = client.write_registers(0x050E, path5value, unit = 0x0077)
    
class inputservo:
    servo = "ServoOn"
    
class readmodbus:
    a = kom()
    while True:
        posisi = a.client.read_holding_registers(0x0520, 2, unit = 0x0077)
        posisireg0 = posisi.getRegister(0)
        posisireg1 = posisi.getRegister(1)
        puu = posisireg0 - posisireg1
        sudut = (puu*9)/2500
        kecepatan = a.client.read_holding_registers(0x0012, 2, unit = 0x0077)
        kecepatan0 = kecepatan.getRegister(0)
        kecepatan1 = kecepatan.getRegister(1)
        speed = kecepatan0 - kecepatan1

class inputsignal:
    f = kom()
    while True:
        x=f.ser.readline(None)
                
        if (x == b'0\r\n'):
            y= 0
        elif (x == b'1\r\n'):
            y= 5000
        elif (x == b'-1\r\n'):
            y= -5000
        elif (x == b'2\r\n'):
            y= 10000
        elif (x == b'-2\r\n'):
            y= -10000
        elif (x == b'3\r\n'):
            y= 15000
        else:
            y= -15000
 
class servo:
    b = inputservo()
    c = kom()
    k = b.servo
    if (b.servo == "ServoOn"):
        valueservo = (0x0001, 0x0000)
        setservo = c.client.write_registers(0x0214, valueservo, unit = 0x0077)
    else :
        valueservo = (0x0101, 0x0000)
        setservo = c.client.write_registers(0x0214, valueservo, unit = 0x0077)

class setposisi:
    e = kom()
    while True:
        errorposisi= y
        if (errorposisi > 0):
            input0 = errorposisi
            input1 = 0
        elif (errorposisi < 0):
            input0 = 65535 + errorposisi + 1
            input1 = 65535 
        else:
            input0 = 0
            input1 = 0 
        valuespeed = (input0, input1)
        setreg = e.client.write_registers(0x0616, valuespeed, unit = 0x0077)
    


class printdata:
    g = inputservo()
    h = posisi()
    i = kecepatan()
    j = inputsignal()
    while True:
        print (g.servo, 'sudut =', h.sudut, "| puu = ", h.puu, "| speed =", i.speed, "| setspeed =", j.y)
