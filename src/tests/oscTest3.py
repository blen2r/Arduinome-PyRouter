#test3
import sys
sys.path.append("..")
from modules.OscOut import OscOut
from OscMsg import OscMsg

import time

if __name__ == "__main__":
    #OSC tests
    try:
        out1 = OscOut(oscAddressPatternPrefix="/test",  hostAddress="127.0.0.1",  hostPort=8080)
        out1.setActive(True)
        
        index = 0
        while 1:
            msg = OscMsg("/led",  "iii",  [index, index, 1])
            out1.addOscMsg(msg)
            
            time.sleep(0.5)
            msg = OscMsg("/led",  "iii",  [index, index, 0])
            out1.addOscMsg(msg)
            
            index += 1
            if index > 7:
                index = 0
                
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        out1.setActive(False)
