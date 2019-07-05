# -*- coding: utf-8 -*-
import serial
import time
import threading
from serial.tools.list_ports import comports
from datetime import datetime



class KernBalance:
    """Repeat `function` every `interval` seconds."""
    def __init__(self, com, timeout):
        self.com = com
        self.timeout = timeout
        self.port = serial.Serial(port=self.com, inter_byte_timeout=self.timeout)
        #self.get_name()
        #self.isOpen = self.port.isOpen()

    def we_talk(self, ascii):
        try:
            with self.port as ser:
                connectedOrNot = ser.isOpen()
                if connectedOrNot:
                    ser.flushInput()
                    ser.write(ascii+b'\r\n')
                    time.sleep(.1)
                    incommingBYTES =ser.inWaiting()
                    #incommingBYTES =self.port.inWaiting()
                    if incommingBYTES == 0:
                        value = "NAN"
                        print("balance eteinte")
                        return value

                    elif incommingBYTES == 5 :
                        value = "NAN"
                        print("out of range")
                        return value

                    else:
                        reception = ser.read(incommingBYTES-2)
                        value = reception[8:]
                        #print(value)
                        return value
                else:
                    value = "NAN"
                    print("sernotconnect")
                    return value
        except serial.serialutil.SerialException:
            print("serialexeption")
            value = "NAN"
            return value

    def get_weight(self):
        cmd = b'SI'
        rec = self.we_talk(cmd)
        if rec != "NAN":
            rec = float(rec.decode()[0:6])
        return rec


class Kerns:
    def __init__(self):
        self.comList = [p.device for p in comports()]
        self.kerns = self.comFilter()

    def comFilter(self):
        kernList = []
        for y in self.comList: 
            test = serial.Serial(port=y, inter_byte_timeout=3)
            test.flushInput()
            test.write(b'SI\r\n')
            time.sleep(.1)
            incommingBYTES =test.inWaiting()
            test.close()
            if incommingBYTES == 0:
                kernList = kernList
            else:
                kernList.append(KernBalance(y,3))
        return kernList

    def getWeights(self):
        weights = {}
        for r in self.kerns:
            weight = r.get_weight()
            weights.update({r.com:weight})
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        weights.update({"TIMESTAMP":timestamp})
        return weights
