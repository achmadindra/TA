import time
import os
import serial
import datetime
import threading
import queue
import pymodbus
import socket
import struct
from queue import Empty, Full, Queue
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

client= ModbusClient(method = "ascii", port="/dev/ttyUSB0",timeout=0.003, stopbits = 1, bytesize = 8, parity = 'N', baudrate = 115200)
servo = "ServoOff"
datashare1 = Queue()
datashare2 = Queue()

file = open("/home/pi/Desktop/log.csv", "a+")
if os.stat("/home/pi//Desktop/log.csv").st_size == 0:
    file.write("Time; servo; y; speed; puu; sudut\n")

if (servo == "ServoOn"):
    valueservo = (0x0001, 0x0000)
    setservo = client.write_registers(0x0214, valueservo, unit = 0x007F)
else :
   valueservo = (0x0101, 0x0000)
   setservo = client.write_registers(0x0214, valueservo, unit = 0x007F)
    
def udp():
    IP = "167.205.66.57"
    PORT = 5900
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((IP, PORT))
    datashare1.put([8])
    while True:
        t=time.time()
        try :
            data, addr = sock.recvfrom(1024)
            data0=data[0]
            data0=int(data0)
            #datashare1.put([data0])
            #print ("received message:", data0, data1, data2, y, time.time()-t)
        except Exception as e:
            print("error t1", e)
            pass

def modbus():
    p=0    
    while True:
        t=time.time()
        data = datashare1.get()
        y = data[0]
        posisi = client.read_holding_registers(0x0520, 2, unit = 0x007F)
        kecepatan = client.read_holding_registers(0x0012, 2, unit = 0x007F)
        posisireg0 = posisi.getRegister(0)
        posisireg1 = posisi.getRegister(1)
        kecepatan0 = kecepatan.getRegister(0)
        kecepatan1 = kecepatan.getRegister(1)
        puu = posisireg0 - posisireg1
        speed = kecepatan0 - kecepatan1
        sudut = (puu*9)/2500
        sudut = int(sudut)
        p = p + speed*0.03*685
        errorposisi= y-sudut
        if (errorposisi > 0):
            input0 = errorposisi
            input1 = 0
        elif (errorposisi < 0):
            input0 = 65535 + errorposisi + 1
            input1 = 65535 
        else:
            input0 = 0
            input1 = 0

        valuespeed = [input0, input1]
        setreg = client.write_registers(0x0118, valuespeed, unit = 0x007F)

        path5value = (0x0016, 0x0000)
        speedpath6 = client.write_registers(0x0218, path5value, unit = 0x007F)

        datashare2.put([servo, y, speed, input0-input1, puu, sudut])            
        tt = time.time()-t
        ttt = 0.05-tt
        time.sleep(ttt) 
        #print("t2", y, speed, puu, p, time.time()-t)

def data():
    while True :
        try :
            t=time.time()
            now=str(datetime.datetime.now())
            data=datashare2.get()
            servo=str(data[0])
            y=str(data[1])
            speed=str(data[2])
            puu=str(data[4])
            sudut=str(data[5])
            datalog=(now, ";", servo, ";", y, ";", speed, ";", puu, ";", sudut)
            file.writelines(datalog)
            file.write("\n")
            file.flush()
            print(data, time.time()-t)
        except Exception as e:
                print("error main", e)
                pass            

if __name__ == "__main__":   

    t1=threading.Thread(target=udp, args=())
    t2=threading.Thread(target=modbus, args=())
    t3=threading.Thread(target=data, args=())
    
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
