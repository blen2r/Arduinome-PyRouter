#import 1
from Message import Message
from AbstractDevice import AbstractDevice
from OscMsg import OscMsg
from MonomeOscSuffixesUtil import MonomeOscSuffixesUtil
from MonomeOscInterpreter import MonomeOscInterpreter
from AbstractModule import AbstractModule

class MonomeXXhDevice(AbstractDevice, AbstractModule):
    """Class MonomeXXhDevice
    """
    
    #const
    iquadrant = [0,1,2,3,2,0,3,1,3,2,1,0,1,3,0,2]
    kDeviceType_40h, kDeviceType_100h, kDeviceType_256, kDeviceType_128, kDeviceType_64, kDeviceType_NumTypes = range(6)
    kCableOrientation_Left, kCableOrientation_Top, kCableOrientation_Right, kCableOrientation_Bottom, kCableOrientation_NumOrientations = range(5)
    kMessageSize_40h = 2
    kMessageSize_100h = 4
    
    myswap = [0x00, 0x80, 0x40, 0xC0, 0x20, 0xA0, 0x60, 0xE0, 0x10, 0x90, 0x50, 0xD0, 0x30, 0xB0, 0x70, 0xF0,\
      0x08, 0x88, 0x48, 0xC8, 0x28, 0xA8, 0x68, 0xE8, 0x18, 0x98, 0x58, 0xD8, 0x38, 0xB8, 0x78, 0xF8,\
      0x04, 0x84, 0x44, 0xC4, 0x24, 0xA4, 0x64, 0xE4, 0x14, 0x94, 0x54, 0xD4, 0x34, 0xB4, 0x74, 0xF4,\
      0x0C, 0x8C, 0x4C, 0xCC, 0x2C, 0xAC, 0x6C, 0xEC, 0x1C, 0x9C, 0x5C, 0xDC, 0x3C, 0xBC, 0x7C, 0xFC,\
      0x02, 0x82, 0x42, 0xC2, 0x22, 0xA2, 0x62, 0xE2, 0x12, 0x92, 0x52, 0xD2, 0x32, 0xB2, 0x72, 0xF2,\
      0x0A, 0x8A, 0x4A, 0xCA, 0x2A, 0xAA, 0x6A, 0xEA, 0x1A, 0x9A, 0x5A, 0xDA, 0x3A, 0xBA, 0x7A, 0xFA,\
      0x06, 0x86, 0x46, 0xC6, 0x26, 0xA6, 0x66, 0xE6, 0x16, 0x96, 0x56, 0xD6, 0x36, 0xB6, 0x76, 0xF6,\
      0x0E, 0x8E, 0x4E, 0xCE, 0x2E, 0xAE, 0x6E, 0xEE, 0x1E, 0x9E, 0x5E, 0xDE, 0x3E, 0xBE, 0x7E, 0xFE,\
      0x01, 0x81, 0x41, 0xC1, 0x21, 0xA1, 0x61, 0xE1, 0x11, 0x91, 0x51, 0xD1, 0x31, 0xB1, 0x71, 0xF1,\
      0x09, 0x89, 0x49, 0xC9, 0x29, 0xA9, 0x69, 0xE9, 0x19, 0x99, 0x59, 0xD9, 0x39, 0xB9, 0x79, 0xF9,\
      0x05, 0x85, 0x45, 0xC5, 0x25, 0xA5, 0x65, 0xE5, 0x15, 0x95, 0x55, 0xD5, 0x35, 0xB5, 0x75, 0xF5,\
      0x0D, 0x8D, 0x4D, 0xCD, 0x2D, 0xAD, 0x6D, 0xED, 0x1D, 0x9D, 0x5D, 0xDD, 0x3D, 0xBD, 0x7D, 0xFD,\
      0x03, 0x83, 0x43, 0xC3, 0x23, 0xA3, 0x63, 0xE3, 0x13, 0x93, 0x53, 0xD3, 0x33, 0xB3, 0x73, 0xF3,\
      0x0B, 0x8B, 0x4B, 0xCB, 0x2B, 0xAB, 0x6B, 0xEB, 0x1B, 0x9B, 0x5B, 0xDB, 0x3B, 0xBB, 0x7B, 0xFB,\
      0x07, 0x87, 0x47, 0xC7, 0x27, 0xA7, 0x67, 0xE7, 0x17, 0x97, 0x57, 0xD7, 0x37, 0xB7, 0x77, 0xF7,\
      0x0F, 0x8F, 0x4F, 0xCF, 0x2F, 0xAF, 0x6F, 0xEF, 0x1F, 0x9F, 0x5F, 0xDF, 0x3F, 0xBF, 0x7F, 0xFF]

    #baudrate:
    #   arduinome: 57600
    #   monome: 115200
    def __init__(self,  serialNumber,  baudrate,  device, autoDetectPrefix=True, orientation=0):
        AbstractModule.__init__(self)
        AbstractDevice.__init__(self,  serialNumber,  baudrate,  device)

        # Attributes:
        self.setOrientation(orientation)  # (int) 
        self.__adcState = [False,  False,  False,  False,]  # (boolean[]) 
        self.__encState =   [False, False]# (boolean[]) 
        self.__tiltState = False  # (boolean) 
        self.__lastTiltX = 0.0  # (float) 
        self.__lastTiltY = 0.0  # (float) 
        self.setOscStartColumn(0)  # (int) 
        self.setOscStartRow(0)  # (int) 
        self.setOscAdcOffset(0)  # (int) 
        self.setOscEncOffset(0)  # (int) 
        self.setOscInterpreter(MonomeOscInterpreter(self))
        
        #determines which type of monome it is depending on the serial number
        if  serialNumber[1] == '4': #40h
            self.__type = MonomeXXhDevice.kDeviceType_40h #kDeviceType_256 kDeviceType_40h #change temp to work on 256
        elif serialNumber[1] == '2': #256
            self.__type = MonomeXXhDevice.kDeviceType_256
        elif serialNumber[1] == '1' : #128
            self.__type = MonomeXXhDevice.kDeviceType_128
        elif serialNumber[1] == '6': #64
            self.__type = MonomeXXhDevice.kDeviceType_64
        else:
            raise ValueError("Bad serial number!")
        
        #sets the address prefix, rows and columns
        if self.__type == MonomeXXhDevice.kDeviceType_40h:
            self.__columns = 8
            self.__rows = 8
            if autoDetectPrefix:
                self.getOscInterpreter().addAcceptedAddressPrefixIn("/40h")
        elif self.__type == MonomeXXhDevice.kDeviceType_256:
            self.__columns = 16
            self.__rows = 16
            if autoDetectPrefix:
                self.getOscInterpreter().addAcceptedAddressPrefixIn("/256")
        elif self.__type == MonomeXXhDevice.kDeviceType_128: # _columns and _rows for _cable == left or right only, always use columns() and rows() to check values
            self.__columns = 16
            self.__rows = 8
            if autoDetectPrefix:
                self.getOscInterpreter().addAcceptedAddressPrefixIn("/128")
        elif self.__type == MonomeXXhDevice.kDeviceType_64:
            self.__columns = 8
            self.__rows = 8
            if autoDetectPrefix:
                self.getOscInterpreter().addAcceptedAddressPrefixIn("/m64")
        else:
            raise ValueError("Unknown device type!")
        
        self.setMessageSize(MonomeXXhDevice.kMessageSize_40h)
        
        #runnables for the CLI
        self.runnables.append("getActive()")
        self.runnables.append("setActive(bool active)")
        self.runnables.append("getColumns()")
        self.runnables.append("getRows()")
        self.runnables.append("getOrientation()")
        self.runnables.append("setOrientation(int orientation)")
        self.runnables.append("getType()")
        self.runnables.append("getDevice()")
        self.runnables.append("setDevice(string device)")
            
    # Operations
    def getColumns(self):
        """function getColumns
        
        returns int
        """
        if  self.__type == MonomeXXhDevice.kDeviceType_128:
            if  self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left or self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
                return self.__columns
            else:
                return self.__rows
        
        return self.__columns
    
    def getRows(self):
        """function getRows
        
        returns int
        """
        if  self.__type == MonomeXXhDevice.kDeviceType_128:
            if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left or self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
                return self.__rows
            else:
                return self.__columns
        
        return self.__rows
    
    def getOrientation(self):
        """function getOrientation
        
        returns int
        """
        if self.__type == MonomeXXhDevice.kDeviceType_128:
            return (self.__orientation+3)%4
            
        return self.__orientation
    
    def getType(self):
        """function getType
        
        returns int
        """
        return self.__type
    
    def setOrientation(self, orientation):
        """function setOrientation
        
        orientation: int
        
        returns void
        """
        if  orientation >= MonomeXXhDevice.kCableOrientation_NumOrientations:
            self.__orientation = MonomeXXhDevice.kCableOrientation_Left
        else:
            self.__orientation = orientation
        
        self.notify("orientation")
    
    def getAdcState(self, index):
        """function getAdcState
        
        index: int
        
        returns boolean
        """
        if index >= 4: #should be replaced by a "try" statement
            return False

        return self.__adcState[index]
    
    def getEncState(self, index):
        """function getEncState
        
        index: int
        
        returns boolean
        """
        if index >= 2: #should be replaced by a "try" statement
            return False

        return self.__encState[index]
    
    def getTiltState(self):
        """function getTiltState
        
        returns boolean
        """
        return self.__tiltState
    
    def getLastTiltX(self):
        """function getLastTiltX
        
        returns float
        """
        return self.__lastTiltX
    
    def getLastTiltY(self):
        """function getLastTiltY
        
        returns float
        """
        return self.__lastTiltY
    
    def setOscStartColumn(self, column):
        """function setOscStartColumn
        
        column: int
        
        returns void
        """
        self.__oscStartColumn = column
        self.notify("oscStartColumn")
    
    def getOscStartColumn(self):
        """function getOscStartColumn
        
        returns int
        """
        return self.__oscStartColumn
    
    def setOscStartRow(self, row):
        """function setOscStartRow
        
        row: int
        
        returns void
        """
        self.__oscStartRow = row
        self.notify("oscStartRow")
    
    def getOscStartRow(self):
        """function getOscStartRow
        
        returns int
        """
        return self.__oscStartRow
    
    def setOscAdcOffset(self, offset):
        """function setOscAdcOffset
        
        offset: int
        
        returns void
        """
        self.__oscAdcOffset = offset
        self.notify("oscAdcOffset")
    
    def getOscAdcOffset(self):
        """function getOscAdcOffset
        
        returns int
        """
        return self.__oscAdcOffset
    
    def setOscEncOffset(self, offset):
        """function setOscEncOffset
        
        offset: int
        
        returns void
        """
        self.__oscEncOffset = offset
        self.notify("oscEncOffset")
    
    def getOscEncOffset(self):
        """function getOscEncOffset
        
        returns int
        """
        return self.__oscEncOffset
    
    def setOscTiltEnableStateChangeEvent(self, tiltEnableState):
        """function setOscTiltEnableStateChangeEvent
        
        tiltEnableState: boolean
        
        returns void
        """
        if self.__type == MonomeXXhDevice.kDeviceType_40h:
            return
        elif self.__type <= MonomeXXhDevice.kDeviceType_64: #256 128 64
            msg = None #Message256, 1byte
            if tiltEnableState:
                msg = messagePack_256_activatePort(1)
            else:
                msg = messagePack_256_activatePort(0) #was *de*activate, but its msg 12 either way
                
            self.writeMsg256_1byte(msg)
    
    def convertLocalCoordToOscCoord(self, column, row):
        """function convertLocalCoordToOscCoord
        
        column: int
        row: int
        
        returns int, int (column, row)
        """
        c = None
        r = None

        if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left:
            c = column
            r = row
        elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Top:
            c = self.getColumns() - row - 1
            r = column
        elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
            c = self.getColumns() - column - 1
            r = self.getRows() - row - 1
        elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Bottom:
            c = row
            r = self.getRows() - column - 1

        c2 = c + self.__oscStartColumn
        r2 = r + self.__oscStartRow
    
        #raise ValueError("convertLocalCoordToOscCoord retourne les nouvelles valeurs au lieu de mettre par reference!") #to remove later
    
        return c2, r2
    
    def convertOscCoordToLocalCoord(self, column, row):
        """function convertOscCoordToLocalCoord
        
        column: int
        row: int
        
        returns int, int (column, row)
        """
        c = column - self.__oscStartColumn
        r = row - self.__oscStartRow
        
        c2 = None
        r2 = None

        if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left:
            c2 = c
            r2 = r
        elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Top:
            c2 = r
            r2 = self.getColumns() - c - 1
        elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
            c2 = self.getColumns() - c - 1
            r2 = self.getRows() - r - 1
        elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Bottom:
            c2 = self.getRows() - r - 1
            r2 = c
            
        #raise ValueError("convertOscCoordToLocalCoord retourne les nouvelles valeurs au lieu de mettre par reference!") #to remove later
    
        return c2, r2
    
    def oscLedStateChangeEvent(self, column, row, state):
        """function oscLedStateChangeEvent
        
        column: int
        row: int
        state: boolean
        
        returns void
        """
        c2, r2 = self.convertOscCoordToLocalCoord(column, row)

        if c2 >= self.__columns or r2 >= self.__rows:
            return

        msg = None
        if self.__type == MonomeXXhDevice.kDeviceType_40h:
            if state:
                msg = messagePackLedStateChange(1, c2, r2)
                self.writeMsg(msg)
            else:
                msg = messagePackLedStateChange(0, c2, r2)
                self.writeMsg(msg)
        elif self.__type <= MonomeXXhDevice.kDeviceType_64: #256 128 64
            if state:
                msg = messagePack_256_led_on(c2, r2)
            else:
                msg = messagePack_256_led_off(c2, r2)
            self.writeMsg(msg)
            
        #raise ValueError("oscLedStateChangeEvent, les param sont supposes etre changes par reference dans convertOscCoord... = probleme?") #to remove later
    
    def oscLedIntensityChangeEvent(self, intensity):
        """function oscLedIntensityChangeEvent
        
        intensity: float
        
        returns void
        """
        if intensity > 1:
            intensity = 1
        elif intensity < 0:
            intensity = 0

        i = int(intensity * 0xF) & 0xF

        if self.__type == MonomeXXhDevice.kDeviceType_40h:
            msg = messagePackLedIntensity(i)
            self.writeMsg(msg)
        elif self__type <= MonomeXXhDevice.kDeviceType_64: #256 128 64
            msg = messagePack_256_intensity(i) #1 byte, only data0
            self.writeMsg_1byte(msg)
    
    def oscLedTestStateChangeEvent(self, testState):
        """function oscLedTestStateChangeEvent
        
        testState: boolean
        
        returns void
        """
        if self.__type == MonomeXXhDevice.kDeviceType_40h:
            if testState:
                msg = messagePackLedTest(1 )
                self.writeMsg(msg)
            else:
                msg = messagePackLedTest(0)
                self.writeMsg(msg)
        else:
            if testState:
                msg = messagePack_256_mode(1)
                self.writeMsg256_1byte(msg)
            else:
                msg = messagePack_256_mode(0)
                self.writeMsg256_1byte(msg)
    
    def oscLedModeStateChangeEvent(self, state):
        """function oscLedModeStateChangeEvent
        
        state: int
        
        returns void
        """
        if state == 0:
            self.oscShutdownStateChangeEvent(True)
        elif state == 1:
            self.oscLedTestStateChangeEvent(True)
        elif state == 2:
            self.oscShutdownStateChangeEvent(False)
    
    def oscLedClearEvent(self, clear):
        """function oscLedClearEvent
        
        clear: boolean
        
        returns void
        """
        if self.__type == MonomeXXhDevice.kDeviceType_40h:
            for i in range(self.__rows):
                if clear:
                    msg = messagePackLedRow(i, 0xFF)
                    self.writeMsg(msg)
                else:
                    msg = messagePackLedRow(i, 0x00)
                    self.writeMsg(msg)
        else:  #m256 (and new devices?) has clear message
            if clear:
                msg = messagePack_256_clear(1)
                self.writeMsg256_1byte(msg)
            else:
                msg = messagePack_256_clear(0)
                self.writeMsg256_1byte(msg)
    
    def oscShutdownStateChangeEvent(self, shutdownState):
        """function oscShutdownStateChangeEvent
        
        shutdownState: boolean
        
        returns void
        """
        if self.__type == MonomeXXhDevice.kDeviceType_40h:
            if shutdownState:
                msg = messagePackShutdown(0)
                self.writeMsg(msg)
            else:
                msg = messagePackShutdown(1)
                self.writeMsg(msg)
        else:
            if shutdownState:
                msg = messagePack_256_mode(2)
                self.writeMsg256_1byte(msg)
            else:
                msg = messagePack_256_mode(0)
                self.writeMsg256_1byte(msg)
    
    def oscLedRowStateChangeEvent(self, row, numBitMaps, bitMaps): #bitMaps = list
        """function oscLedRowStateChangeEvent
        
        row: int
        numBitMaps: int
        bitMaps: byte list
        
        returns void
        """
        #added by dan - check that column offset is not greater than the highest value in the bitmap
        if row < self.__oscStartRow or row >= self.__oscStartRow + self.getRows() or self.__oscStartColumn >= numBitMaps * 8:
            return #should raise an exception

        #use columns() and rows() instead of _columns and _rows to get correct values in case _type == kDeviceType_128
        r = row - self.__oscStartRow
        index = self.__oscStartColumn / 8
        shift = self.__oscStartColumn % 8
        bitMap = bitMaps[index] >> shift

        if index + 1 < numBitMaps:
            bitMap |= bitMaps[index + 1] << (8 - shift)

        if self.__type == MonomeXXhDevice.kDeviceType_40h:# maybe include 64 here too, and select the appropriate messagePackLedRow macro?
            msg = None
            
            if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left:
                msg = messagePackLedRow(r, bitMap)
            elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Top:
                msg = messagePackLedColumn(r, MonomeXXhDevice.myswap[bitMap])
            elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
                msg = messagePackLedRow(self.getRows() - r - 1, MonomeXXhDevice.myswap[bitMap])
            elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Bottom:
                msg = messagePackLedColumn(self.getColumns() - r - 1, bitMap)
            
            self.writeMsg(msg)
        elif self.__type <= MonomeXXhDevice.kDeviceType_64: #256, 128 and 64
            # 1-byte row command:
            #	- 64 -> always use this, since there is only 1 byte-row
            #  - 256 -> if there is only 1 bitMap, or offsets allow use of last bitMap only
            #  - 126 -> cable is up or down, or if left or right then offsets allow use of last bitMap only
            if self.getColumns() <= 8 or index + 1 == numBitMaps:
                msg = None

                if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left:
                    msg = messagePack_256_led_row1(r, bitMap)
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Top:
                    msg = messagePack_256_led_col1(r, MonomeXXhDevice.myswap[bitMap])
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
                    msg = messagePack_256_led_row1(self.getRows() - r - 1, MonomeXXhDevice.myswap[bitMap])
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Bottom:
                    msg = messagePack_256_led_col1(self.getColumns() - r - 1, bitMap)

                self.writeMsg(msg)
            # 2-byte row command: numBitMaps > 1
            #  - 256 -> column offset not in last bitMap
            #  - 128 -> cable is left or right, AND column offset not in last bitMap
            else:
                msg = None #msg256 3 bytes
                bitMap2 = bitMaps[index + 1] >> shift

                if index + 2 < numBitMaps:
                    bitMap2 |= bitMaps[index + 2] << (8 - shift)

                if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left:
                    msg = messagePack_256_led_row2(r, bitMap, bitMap2)
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Top:
                    msg = messagePack_256_led_col2(r, MonomeXXhDevice.myswap[bitMap2], MonomeXXhDevice.myswap[bitMap])
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
                    msg = messagePack_256_led_row2(self.getRows() - r - 1, MonomeXXhDevice.myswap[bitMap2], MonomeXXhDevice.myswap[bitMap])
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Bottom:
                    msg = messagePack_256_led_col2(self.getColumns() - r - 1, bitMap, bitMap2)

                self.writeMsg256_3bytes(msg)
    
    def oscLedColumnStateChangeEvent(self, column, numBitMaps, bitMaps):
        """function oscLedColumnStateChangeEvent
        
        column: int
        numBitMaps: int
        bitMaps: byte list
        
        returns void
        """
        #added by dan - check that column offset is not greater than the highest value in the bitmap
        if column < self.__oscStartColumn or column >= self.__oscStartColumn + self.getColumns() or self.__oscStartRow >= numBitMaps * 8:
            return

        #use columns() and rows() instead of _columns and _rows to get correct values in case _type == kDeviceType_128
        c = column - self.__oscStartColumn
        index = self.__oscStartRow / 8
        shift = self.__oscStartRow % 8
        bitMap = bitMaps[index] >> shift

        if index + 1 < numBitMaps:
            bitMap |= bitMaps[index + 1] << (8 - shift)

        if self.__type == MonomeXXhDevice.kDeviceType_40h:  #maybe include 64 here too, and select the appropriate messagePackLedRow macro?
            msg = None

            if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left:
                msg = messagePackLedColumn(c, bitMap)
            elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Top:
                msg = messagePackLedRow(self.__rows - c - 1, bitMap)
            elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
                msg = messagePackLedColumn(self.__columns - c - 1, MonomeXXhDevice.myswap[bitMap])
            elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Bottom:
                msg = messagePackLedRow(c, MonomeXXhDevice.myswap[bitMap])

            self.writeMsg(msg)
        elif self.__type <= MonomeXXhDevice.kDeviceType_64: #256, 128 and 64
            # 1-byte col command:
            #	- 64 -> always use this, since there is only 1 byte-col
            #  - 256 -> if there is only 1 bitMap, or offsets allow use of last bitMap only
            #  - 126 -> cable is up or down, or if left or right then offsets allow use of last bitMap only
            if self.getRows() <= 8 or index + 1 == numBitMaps:
                msg = None

                if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left:
                    msg = messagePack_256_led_col1(c, bitMap)
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Top:
                    msg = messagePack_256_led_row1(self.__rows - c - 1, bitMap)
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
                    msg = messagePack_256_led_col1(self.__columns - c - 1, MonomeXXhDevice.myswap[bitMap])
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Bottom:
                    msg = messagePack_256_led_row1(c, MonomeXXhDevice.myswap[bitMap])

                self.writeMsg(msg)
                
            # 2-byte col command: numBitMaps > 1
            #  - 256 -> row offset not in last bitMap
            #  - 128 -> cable is left or right, AND row offset not in last bitMap
            else:
                msg = None #msg256 3 bytes
                bitMap2 = bitMaps[index + 1] >> shift

                if index + 2 < numBitMaps:
                    bitMap2 |= bitMaps[index + 2] << (8 - shift)

                if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left:
                    msg = messagePack_256_led_col2(c, bitMap, bitMap2)
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Top:
                    msg = messagePack_256_led_row2(self.__rows - c - 1, bitMap, bitMap2)
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
                    msg = messagePack_256_led_col2(self.__columns - c - 1,  MonomeXXhDevice.myswap[bitMap2], MonomeXXhDevice.myswap[bitMap])
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Bottom:
                    msg = messagePack_256_led_row2(c, MonomeXXhDevice.myswap[bitMap2],  MonomeXXhDevice.myswap[bitMap])

                self.writeMsg256_3bytes(msg)
    
    def oscAdcEnableStateChangeEvent(self, adcIndex, adcEnableState):
        """function oscAdcEnableStateChangeEvent
        
        adcIndex: int
        adcEnableState: boolean
        
        returns void
        """
        if adcIndex >= 4:
            return
            
        self.__adcState[adcIndex] = adcEnableState

        if (adcEnableState):
            for i in range(2):
                self.__encState[i] = False
                self.oscEncEnableStateChangeEvent(i, False)

        if self.__type == MonomeXXhDevice.kDeviceType_40h:
            if adcEnableState:
                msg = messagePackAdcEnable(adcIndex, 1)
                self.writeMsg(msg)
            else:
                msg = messagePackAdcEnable(adcIndex, 0)
                self.writeMsg(msg)
        elif self.__type <= MonomeXXhDevice.kDeviceType_64: #256 128 64
            msg = None #msg256 1 byte
            if adcEnableState:
                msg = messagePack_256_activatePort(adcIndex)
            else:
                msg = messagePack_256_deactivatePort(adcIndex)
                
            self.writeMsg256_1byte(msg)
    
    def oscEncEnableStateChangeEvent(self, encIndex, encEnableState):
        """function oscEncEnableStateChangeEvent
        
        encIndex: int
        encEnableState: boolean
        
        returns void
        """

        if self.__type != MonomeXXhDevice.kDeviceType_40h:
            return
        if encIndex >= 2:
            return

        self.__encState[encIndex] = encEnableState

        if encEnableState:
            for i in range(4):
                self.__adcState[i] = False
                self.oscAdcEnableStateChangeEvent(i, False)
        
        if encEnableState:
            msg = messagePackEncEnable(encIndex, 1)
            self.writeMsg(msg)
        else:
            msg = messagePackEncEnable(encIndex, 0)
            self.writeMsg(msg)

    
    def oscLedFrameEvent(self, column, row, bitMaps):
        """function oscLedFrameEvent
        
        column: int
        row: int
        bitMaps: byte list
        
        returns void
        """
        map = [None]*8 #8 elements
        rmap= [None]*8 #8 elements
        i = None
        shift = None
        r = None
        c = None

        if column >= self.__oscStartColumn + self.getColumns() or row >= self.__oscStartRow + self.__rows or column + 7 < self.__oscStartColumn or row + 7 < self.__oscStartRow:
            return

        if self.__type == MonomeXXhDevice.kDeviceType_40h:
            msg = None

            if column >= self.__oscStartColumn:
                shift = column - self.__oscStartColumn

                for i in range(8):
                    if self.__oscStartRow + i < row:
                        map[i] = 0
                    elif self.__oscStartRow + i >= row + 8:
                        map[i] = 0
                    else:
                        map[i] = bitMaps[self.__oscStartRow + i - row] << shift
            else:
                shift = self.__oscStartColumn - column

                for i in range(8):
                    if self.__oscStartRow + i < row:
                        map[i] = 0
                    elif self.__oscStartRow + i >= row + 8:
                        map[i] = 0
                    else:
                        map[i] = bitMaps[self.__oscStartRow + i - row] >> shift

            if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left:
                for i in range(8):
                    msg = messagePackLedRow(i, map[i])
                    self.writeMsg(msg)
            elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Top:
                rmap = [0]*8

                for r in range(8) :
                    for c in range(8):
                        if map[r] & (0x80 >> c):
                            rmap[c] |= 0x80 >> (7 - r)

                for i in range(8) :
                    msg = messagePackLedRow(i, rmap[i])
                    self.writeMsg(msg)
            elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
                for i in range(8):
                    msg = messagePackLedRow(7 - i, MonomeXXhDevice.myswap[map[i]])
                    self.writeMsg(msg)
            elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Bottom:
                rmap = [0]*8

                for r in range(8):
                    for c in range(8):
                        if map[r] & (0x80 >> c):
                            rmap[7 - c] |= 0x80 >> r

                for i in range(8):
                    msg = messagePackLedRow(i, rmap[i])
                    self.writeMsg(msg)
        elif self.__type <= MonomeXXhDevice.kDeviceType_64: #<- will this work for other devices than 256?
            quadrant = ((column - self.__oscStartColumn) / 8) + (((row - self.__oscStartRow) / 8) * 2)
            
            if (quadrant > 0):
                if self.__type == MonomeXXhDevice.kDeviceType_64:
                    return
                elif quadrant > 1 and self.__type == MonomeXXhDevice.kDeviceType_128:
                    return

            msg = None #msg256 frame, 8 bytes

            if (row == self.__oscStartRow or row == self.__oscStartRow + 8) and (column == self.__oscStartColumn or column == self.__oscStartColumn + 8):
                map = list(bitMaps)

                if self.getOrientation() == MonomeXXhDevice.kCableOrientation_Left:
                    for r in range(8):
                        rmap = list(map)
                    
                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Top:
                    rmap = [0]*8
                    
                    for r in range(8):
                        for c in range(8):
                            if map[r] & (0x80 >> c):
                                rmap[c] |= 0x80 >> (7 - r)
                                quadrant = iquadrant[quadrant+4]

                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Right:
                    for r in range(8):
                        rmap[r] = map[7-r]
                        quadrant = iquadrant[quadrant+8]

                elif self.getOrientation() == MonomeXXhDevice.kCableOrientation_Bottom:
                    rmap = [0]*8
                    
                    for r in range(8):
                        for c in range(8):
                            if map[r] & (0x80 >> c):
                                rmap[7 - c] |= 0x80 >> r
                                quadrant = iquadrant[quadrant+12]

                msg = messagePack_256_led_frame(quadrant, rmap[0], rmap[1], rmap[2], rmap[3], rmap[4], rmap[5], rmap[6], rmap[7])
                self.writeMsg256_frame(msg)
                
            else:
                for i in range(8):
                    localRow = row + i
                    
                    if localRow >= self.__oscStartRow and localRow < (self.__oscStartRow + 16): #don't call if not in this row
                        size = (column / 8) + 1
                        rowBitMap = None

                        if column < self.__oscStartColumn:
                            rowBitMap = [0]*size

                            shift = (self.__oscStartColumn - column) % 8
                            rowBitMap[size - 1] = bitMaps[i] >> shift
                            self.oscLedRowStateChangeEvent(localRow, size, rowBitMap)
                            rowBitMap = None
                        else:
                            size += 1
                            rowBitMap = [0]*size

                            shift = (column - self.__oscStartColumn) % 8

                            if column < (self.__oscStartColumn + 8):
                                rowBitMap[size - 2] = bitMaps[i] << shift
                                rowBitMap[size - 1] = bitMaps[i] >> (8 - shift)
                            else:
                                rowBitMap[size - 2] = bitMaps[i] << shift

                            self.oscLedRowStateChangeEvent(localRow, size, rowBitMap)
                            rowBitMap = None

    def handleSerialDeviceMessageReceivedEvent(self,  msg):
        """function handleSerialDeviceMessageReceivedEvent

        msg: Message

        returns void
        """
        msgType = messageGetType(msg)
        
        if self.__type == MonomeXXhDevice.kDeviceType_40h:
            if msgType == kMessageTypeButtonPress:
                self.handleButtonPressEvent(messageGetButtonX(msg), messageGetButtonY(msg), messageGetButtonState(msg))
            elif msgType == kMessageTypeAdcVal:
                self.handleAdcValueChangeEvent(messageGetAdcPort(msg), float(messageGetAdcVal(msg)) / float(0x3FF))
            elif msgType == kMessageTypeEncVal:
                self.handleRotaryEncoderEvent(messageGetEncPort(msg), messageGetEncVal(msg))

        elif self.__type <= MonomeXXhDevice.kDeviceType_64:#always 2 bytes from 256device
            if msgType == kMessageType_256_keydown:
                handleButtonPressEvent(messageGetButtonX(msg), messageGetButtonY(msg), True)
            
            elif msgType == kMessageType_256_keyup:
                handleButtonPressEvent(messageGetButtonX(msg), messageGetButtonY(msg), False)
            
            elif msgType == kMessageType_256_auxiliaryInput:
                handleRotaryEncoderEvent(messageGetEncPort(msg), messageGetEncVal(msg))	
            
            elif msgType == kMessageTypeTiltEvent:
                handleTiltValueChangeEvent(messageGetTiltAxis(msg),  messageGetEncVal(msg))	

    def handleButtonPressEvent(self, localColumn, localRow, state):
        """function handleButtonPressEvent

        localColumn: int
        localRow: int
        state: boolean

        returns void
        """
        coords = self.convertLocalCoordToOscCoord(localColumn, localRow)
        
        msg = OscMsg(oscAddress=MonomeOscSuffixesUtil.kOscDefaultAddrPatternButtonPressSuffix,\
                     typeTags=MonomeOscSuffixesUtil.kOscDefaultTypeTagsButtonPress,\
                     data=[coords[0], coords[1],  int(state)])
            
        self.sendMsgToOscOuts(msg)

    def handleAdcValueChangeEvent(self, localAdcIndex, value):
        """function handleButtonPressEvent

        localAdcIndex: int
        value: float

        returns void
        """
        msg = OscMsg(oscAddress=MonomeOscSuffixesUtil.kOscDefaultAddrPatternAdcValueSuffix,\
                     typeTags=MonomeOscSuffixesUtil.kOscDefaultTypeTagsAdcValue,\
                     data=[self.__oscAdcOffset+localAdcIndex, value])
            
        self.sendMsgToOscOuts(msg)

    def handleRotaryEncoderEvent(self, localEncoderIndex, steps):
        """function handleButtonPressEvent

        localEncoderIndex: int
        steps: int

        returns void
        """
        msg = OscMsg(oscAddress=MonomeOscSuffixesUtil.kOscDefaultAddrPatternEncValueSuffix,\
                     typeTags=MonomeOscSuffixesUtil.kOscDefaultTypeTagsEncValue,\
                     data=[self.__oscEncOffset + localEncoderIndex, steps])
            
        self.sendMsgToOscOuts(msg)

    def handleTiltValueChangeEvent(self, axis, value):
        """function handleButtonPressEvent

        axis: int
        value: float

        returns void
        """
        if axis == 0:
            self.__lastTiltX = value
        else:
            self.__lastTiltY = value

        msg = OscMsg(oscAddress=MonomeOscSuffixesUtil.kOscDefaultAddrPatternTiltValueSuffix,\
                     typeTags="ff",\
                     data=[float(self.__lastTiltX),  float(self.__lastTiltY)])
            
        self.sendMsgToOscOuts(msg)
    
    def setActive(self,  active):
        """function setActive

        active: boolean

        returns void
        """
        if not active:
            self.oscLedClearEvent(False)
        
        AbstractDevice.setActive(self, active)

#############
# Utility functions #
#############

kMessageTypeButtonPress, kMessageTypeAdcVal, kMessageTypeLedStateChange, kMessageTypeLedIntensity, kMessageTypeLedTest, kMessageTypeAdcEnable,\
kMessageTypeShutdown, kMessageTypeLedSetRow, kMessageTypeLedSetColumn, kMessageTypeEncEnable, kMessageTypeEncVal, null,  kMessageTypeTiltVal,\
kMessageTypeTiltEvent, kMessageNumTypes = range(15)

kMessageType_256_keydown,\
kMessageType_256_keyup,\
kMessageType_256_led_on,\
kMessageType_256_led_off,\
kMessageType_256_led_row1,\
kMessageType_256_led_col1,\
kMessageType_256_led_row2,\
kMessageType_256_led_col2,\
kMessageType_256_led_frame,\
kMessageType_256_clear, \
kMessageType_256_intensity,\
kMessageType_256_mode,\
kMessageType_256_activatePort,\
kMessageType_256_deactivatePort,\
kMessageType_256_auxiliaryInput,\
kMessage_256_NumTypes = range(16)

kMessageSize_256 = [2,2,2,2, 3,2,3,3,9,1,1,1, 1,1,2]


def messageGetType(message):
    """function messageGetType
    
    message: Message
    
    returns byte
    """
    return (message.data[0] >> 4)

def messageGetButtonState(message):
    """function messageGetButtonState
    
    message: Message
    
    returns byte
    """
    return (message.data[0] & 0x0F)

def messageGetButtonX(message):
    """function messageGetButtonX
    
    message: Message
    
    returns byte
    """
    return (message.data[1] >> 4)

def messageGetButtonY(message):
    """function messageGetButtonY
    
    message: Message
    
    returns byte
    """
    return (message.data[1] & 0x0F)

def messageGetAdcPort(message):
    """function messageGetAdcPort
    
    message: Message
    
    returns byte
    """
    return ((message.data[0] >> 2) & 0x3)

def messageGetAdcVal(message):
    """function messageGetAdcVal
    
    message: Message
    
    returns byte
    """
    return (((message.data[0] & 0x3) << 8) | message.data[1])

def messageGetEncPort(message):
    """function messageGetEncPort
    
    message: Message
    
    returns byte
    """
    return (message.data[0] & 0x0F)

def messageGetEncVal(message):
    """function messageGetEncVal
    
    message: Message
    
    returns byte
    """
    return message.data[1]

def messageGetTiltAxis(message):
    """function messageGetTiltAxis
    
    message: Message
    
    returns byte
    """
    return (message.data[0])-208

def messagePackAdcVal(port, val):
    """function messagePackAdcVal
    
    port: byte
    val: 2-bytes
    
    returns Message
    """
    msg = Message()
    msg.data.append( (kMessageTypeAdcVal << 4) | ((port << 2) & 0x0C) | ((val >> 8) & 0x03) )
    msg.data.append( val )
    return msg

def messagePackLedStateChange(state, x, y):
    """function messagePackLedStateChange
    
    state: byte
    x: byte
    y: byte
    
    returns Message
    """
    msg = Message()
    msg.data.append( (kMessageTypeLedStateChange << 4) | state )
    msg.data.append( (x << 4) | y )
    return msg

def messagePackLedIntensity(intensity):
    """function messagePackLedIntensity
    
    intensity: byte
    
    returns Message
    """
    msg = Message()
    msg.data.append( (kMessageTypeLedIntensity << 4) )
    msg.data.append( intensity )
    return msg

def messagePackLedTest(state):
    """function messagePackLedTest
    
    state: byte
    
    returns Message
    """
    msg = Message()
    msg.data.append( (kMessageTypeLedTest << 4) )
    msg.data.append( state )#state must be 0 or 1
    return msg

def messagePackAdcEnable(adc, state):
    """function messagePackAdcEnable
    
    adc: byte
    state: byte
    
    returns Message
    """
    msg = Message()
    msg.data.append( kMessageTypeAdcEnable << 4 )
    msg.data.append( (adc << 4) | state ) #state must be 0 or 1
    return msg

def messagePackShutdown(state):
    """function messagePackShutdown
    
    state: byte
    
    returns Message
    """
    msg = Message()
    msg.data.append( kMessageTypeShutdown << 4 )
    msg.data.append( state ) #state must be 0 or 1
    return msg

def messagePackLedRow(rowIndex, state):
    """function messagePackLedRow
    
    rowIndex: byte
    state: byte
    
    returns Message
    """
    msg = Message()
    msg.data.append( (kMessageTypeLedSetRow << 4) | (rowIndex & 0xF) )
    msg.data.append( state )
    return msg

def messagePackLedColumn(columnIndex, state):
    """function messagePackLedColumn
    
    columnIndex: byte
    state: byte
    
    returns Message
    """
    msg = Message()
    msg.data.append( (kMessageTypeLedSetColumn << 4) | (columnIndex & 0xF) )
    msg.data.append( state )
    return msg

def messagePackEncEnable(enc, state):
    """function messagePackEncEnable
    
    enc: byte
    state: byte
    
    returns Message
    """
    msg = Message()
    msg.data.append( (kMessageTypeEncEnable << 4) | (enc & 0xF) )
    msg.data.append( state ) #state must be 0 or 1
    return msg

def messagePackEncVal(enc, val):
    """function messagePackEncVal
    
    enc: byte
    val: byte
    
    returns Message
    """
    msg = Message()
    msg.data.append( (kMessageTypeEncVal << 4) | (enc & 0xF) )
    msg.data.append( val )
    return msg


