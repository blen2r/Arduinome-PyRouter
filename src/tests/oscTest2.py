#test2
import sys
sys.path.append("..")
from modules.MonomeXXhDevice import MonomeXXhDevice
from modules.OscOut import OscOut
from modules.OscIn import OscIn

import time

if __name__ == "__main__":
    monome = MonomeXXhDevice( serialNumber="a40h-001",  baudrate=57600,  device="/dev/ttyUSB0",  autoDetectPrefix=True)
   
    #OSC tests
    try:
        out1 = OscOut(oscAddressPatternPrefix="/box",  hostAddress="127.0.0.1",  hostPort=10000)
        monome.addOscOut( out1 )
        in1 = OscIn(listenAddress="192.168.1.100", listenPort=8080)
        in1.addOscInterpreter(monome.getOscInterpreter())
        monome.getOscInterpreter().addAcceptedAddressPrefixIn("/box")
        monome.getOscInterpreter().addAcceptedAddressPrefixIn("/max")
        monome.getOscInterpreter().addAcceptedAddressPrefixIn("/40h")
        in1.setActive(True)
        out1.setActive(True)
        monome.setActive(True)
        
        while 1:
            time.sleep(0.001)
    except KeyboardInterrupt:
        in1.setActive(False)
        out1.setActive(False)
        monome.setActive(False)
    
    
    #disconnects
    monome = None #disconnects
