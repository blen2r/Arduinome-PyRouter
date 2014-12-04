#test
import sys
sys.path.append("..")
from modules.MonomeXXhDevice import MonomeXXhDevice
from modules.OscOut import OscOut
from modules.OscIn import OscIn

import time

if __name__ == "__main__":
    monome = MonomeXXhDevice( serialNumber="a40h-001",  baudrate=57600,  device="/dev/ttyUSB0",  autoDetectPrefix=True)
    
    #tests clear all on(true)/off(false)
    print "tests clear all on(true)/off(false)"
    monome.oscLedClearEvent(True)
    time.sleep(1)
    monome.oscLedClearEvent(False)
    time.sleep(1)
    
    #tests individual leds
    print "tests individual leds"
    monome.oscLedClearEvent(False) #clear
    for i in range(8):
        for j in range(8):
            monome.oscLedStateChangeEvent(j, i, True)
            time.sleep(0.1)
            monome.oscLedStateChangeEvent(j, i, False)
    
    #tests led row
    print "tests led row"
    monome.oscLedClearEvent(False) #clear
    for i in range(8):
        monome.oscLedRowStateChangeEvent(i, 1, [255])
        time.sleep(0.1)
        monome.oscLedRowStateChangeEvent(i, 1,  [126])
        time.sleep(0.1)
        monome.oscLedRowStateChangeEvent(i, 1,  [60])
        time.sleep(0.1)
        monome.oscLedRowStateChangeEvent(i, 1,  [24])
        time.sleep(0.1)
        monome.oscLedRowStateChangeEvent(i, 1,  [0])
        time.sleep(0.1)
        
    #tests led column
    print "tests led column"
    monome.oscLedClearEvent(False) #clear
    for i in range(8):
        monome.oscLedColumnStateChangeEvent(i, 1, [255])
        time.sleep(0.1)
        monome.oscLedColumnStateChangeEvent(i, 1,  [126])
        time.sleep(0.1)
        monome.oscLedColumnStateChangeEvent(i, 1,  [60])
        time.sleep(0.1)
        monome.oscLedColumnStateChangeEvent(i, 1,  [24])
        time.sleep(0.1)
        monome.oscLedColumnStateChangeEvent(i, 1,  [0])
        time.sleep(0.1)
    
    #tests frame
    print "tests frame"
    monome.oscLedClearEvent(False) #clear
    i = range(255)
    i.reverse()
    for j in i:
        monome.oscLedFrameEvent(0, 0,  [j]*8)
        time.sleep(0.01)
    time.sleep(2)
    monome.oscLedClearEvent(False) #clear
    
    #tests intensity change
    print "tests intensity change"
    monome.oscLedClearEvent(True)
    for i in range (2):
        for j in [1,  0.75,  0.50,  0.25,  0]:
            monome.oscLedIntensityChangeEvent(j)
            time.sleep(0.5)
    monome.oscLedIntensityChangeEvent(1)
    time.sleep(1)
    monome.oscLedClearEvent(False)
    
    #tests mode change (shutdown/test state/shutdown)
#    monome.oscLedClearEvent(False)
#    for i in range(3):
#        monome.oscLedModeStateChangeEvent(i)
#        time.sleep(2)
#    monome.oscLedClearEvent(False)
    
    #disconnects
    monome = None #disconnects
