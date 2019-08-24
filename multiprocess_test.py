import time
import serial
import pymodbus
import logging
import math
from multiprocessing import Process, Queue
from threading import Thread
from queue import Empty

from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

client= ModbusClient(method = "rtu", port="/dev/ttyUSB0",timeout=(1/100), stopbits = 1, bitsize = 32, parity = 'N', baudrate = 115200)
connection = client.connect()
print (connection)

ser = serial.Serial(port="/dev/ttyACM0", baudrate = 115200, timeout=1)

servo = "ServoOff"

path5value = (5, 0)
speedpath6 = client.write_registers(0x050E, path5value, unit = 0x0077)

if (servo == "ServoOn"):
    valueservo = (0x0001, 0x0000)
    setservo = client.write_registers(0x0214, valueservo, unit = 0x0077)
       
else :
   valueservo = (0x0101, 0x0000)
   setservo = client.write_registers(0x0214, valueservo, unit = 0x0077)

def bacadata(client, serial, queue):
    while True:
        try:
            posisi = client.read_holding_registers(0x0520, 2, unit = 0x0077)
            posisireg0 = posisi.getRegister(0)
            posisireg1 = posisi.getRegister(1)
            puu = posisireg0 - posisireg1
            sudut = (puu*9)/2500

            kecepatan = client.read_holding_registers(0x0012, 2, unit = 0x0077)
            kecepatan0 = kecepatan.getRegister(0)
            kecepatan1 = kecepatan.getRegister(1)
            speed = kecepatan0 - kecepatan1
            
            x=ser.readline(None)  
            queue.put([puu,speed,sudut,x])
            time.sleep(1/6)
        except:
            pass

def prosesdata(servo,client,queue):
    while True:
        try:
            data = queue.get()
            x = data[3] 
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
            y=int(y)
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
            setreg = client.write_registers(0x0616, valuespeed, unit = 0x0077)
            sudut = data[2]
            puu = data[0]
            speed = data[1]
            print (servo, 'sudut =', sudut, "| puu = ", puu, "| speed =", speed, "| setspeed =", y)
            time.sleep(1/6)
        except Empty:
            pass


queue = Queue()

thread_bacadata = Thread(target=bacadata, args=(client, ser, queue,))
thread_bacadata.start()

thread_prosesdata = Thread(target=prosesdata, args=(servo, client, queue,))
thread_prosesdata.start()
