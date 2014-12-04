#import 0
from OscInterpreter import OscInterpreter
from MonomeOscSuffixesUtil import MonomeOscSuffixesUtil
from OscMsg import OscMsg
from AbstractModule import AbstractModule

class MonomeOscInterpreter(OscInterpreter, AbstractModule):
    def receiveOscMsg(self,  msg):
        """function receiveOscMsg
        
        msg: OscMsg
        
        returns void
        """
        #if we received a system message
        if msg.getOscAddress().startswith("/sys"):
            self.handleOscSysMsg(msg)
            return
                
        if self.isPrefixValid(msg):
            suffix = self.findSuffix(msg)
            
            if suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternLedStateSuffix:  #prefix/led

                if  not msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsLedState):
                    return

                column = int(msg.getData()[0])
                row = int(msg.getData()[1])
                state = bool(int(msg.getData()[2]))

                self.device.oscLedStateChangeEvent(column, row, state)
                    
            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternLedIntensitySuffix: # prefix/intensity 
            
                if  not msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsLedIntensity):
                    return

                intensity = float(msg.getData()[0])

                self.device.oscLedIntensityChangeEvent(intensity)
                
            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternLedTestSuffix: # prefix/test
                if not msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsLedTest):
                    return

                testState = bool(int(msg.getData()[0]))

                self.device.oscLedTestStateChangeEvent(testState)

            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternLedClearSuffix: # prefix/clear
                clear = None

                if len(msg.getData()) == 0:
                    clear = False
                elif not msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsLedTest):
                    return
                else:
                    clear = bool(int(msg.getData()[0]))

                self.device.oscLedClearEvent(clear)
            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternAdcEnableSuffix: # prefix/adc_enable
                if not msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsAdcEnable):
                    return

                adcIndex = int(msg.getData()[0])
                adcState = bool(int(msg.getData()[1]))

                self.device.oscAdcEnableStateChangeEvent(adcIndex, adcState)

            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternShutdownSuffix: # prefix/shutdown
                if not msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsShutdown):
                    return

                shutdownState = bool(int(msg.getData()[0]))

                self.device.oscShutdownStateChangeEvent(shutdownState)
                
            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternLed_ModeSuffix: # prefix/led_mode 
                stateout = 5
                if msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscTypeTagString): 	
                    testmode = msg.getData()[0]
                    if testmode == "off":
                        stateout = 0
                    elif testmode == "on":
                        stateout = 1
                    elif testmode == "normal":
                        stateout = 2
                    else:
                        return
                else :
                    stateout = int(msg.getData()[0])

                self.device.oscLed_ModeStateChangeEvent(stateout)

            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternLedRowSuffix: # prefix/led_row
                if len(msg.getData()) < 2 or not msg.typeTagsMatch(["ii"]):
                    return

                row = int(msg.getData()[0])

                index = 0
                bitmap = [0]*256
                
                for i in range(1,  len(msg.getData())):
                    bitmap[index] = int(msg.getData()[i])
                    index += 1

                self.device.oscLedRowStateChangeEvent(row, index, bitmap)
                
            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternLedColumnSuffix: # prefix/led_col 
                if len(msg.getData()) < 2 or not msg.typeTagsMatch(["ii"]):
                    return

                column = msg.getData()[0]

                index = 0
                bitmap = [0]*256

                for i in range(1,  len(msg.getData())):
                    bitmap[index] = int(msg.getData()[i])
                    index += 1

                self.device.oscLedColumnStateChangeEvent(column, index, bitmap)

            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternEncEnableSuffix: # prefix/enc_enable
                if not msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsEncEnable):
                    return

                encIndex = int(msg.getData()[0])
                encState = bool(int(msg.getData()[1]))

                self.device.oscEncEnableStateChangeEvent(encIndex, encState)

            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternLedFrameSuffix: # prefix/frame
                if msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsLedOffsetFrame): # 10 Ints, first 2 for offset
                    bitmap = [0] * 8

                    column = int(msg.getData()[0])
                    row = int(msg.getData()[1])
                    index = 0

                    for i in range(2,  len(msg.getData())):
                        bitmap[index] = int(msg.getData()[i])
                        index += 1

                    self.device.oscLedFrameEvent(column, row, bitmap)

                elif msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsLedFrame): # 8 Ints
                    index = 0
                    bitmap = [0]*8

                    for i in range(2,  len(msg.getData())):
                        bitmap[index] = int(msg.getData()[i])
                        index += 1

                    self.device.oscLedFrameEvent(0, 0, bitmap)
                    
            # Tilt - 64 only! - (added by Steve)
            elif suffix == MonomeOscSuffixesUtil.kOscDefaultAddrPatternTilt_ModeSuffix: # 1 int, as bool
                if not msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsTiltMode):
                    return

                tiltmode = bool(int(msg.getData()[0]))

                self.device.oscTiltEnableStateChangeEvent(tiltmode)
    
    def handleOscSysMsg(self, msg):
        """function handleOscSysMsg
        
        msg: OscMsg
        
        returns void
        """
        if msg.getOscAddress() == MonomeOscSuffixesUtil.kOscDefaultAddrPatternSystemPrefix:
            if msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysPrefixAll): #changes the prefix for all monomes
                pre = msg.getData()[0]
                if not pre.startswith("/"):
                    pre = "/" + pre

                self.addAcceptedAddressPrefixIn(pre)
            elif msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysPrefixSingle): #changes the prefix for a single monome
                raise NotImplementedError()

        elif msg.getOscAddress() == MonomeOscSuffixesUtil.kOscDefaultAddrPatternSystemCable:
            if msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysCableAll): #changes the orientation for all monomes
                orientation = msg.getData()[0]

                if orientation == "left":
                    self.device.setOrientation(MonomeXXhDevice.kCableOrientation_Left)
                elif orientation == "right":
                    self.device.setOrientation(MonomeXXhDevice.kCableOrientation_Right)
                elif orientation == "up":
                    self.device.setOrientation(MonomeXXhDevice.kCableOrientation_Top)
                elif orientation == "down":
                    self.device.setOrientation(MonomeXXhDevice.kCableOrientation_Bottom)
                
            elif msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysCableSingle): #changes the orientation for a single monome
                raise NotImplementedError()

        elif msg.getOscAddress() == MonomeOscSuffixesUtil.kOscDefaultAddrPatternSystemOffset:
            if msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysOffsetAll): #changes the offset for all monomes
                x = int(msg.getData()[0])
                y = int(msg.getData()[1])

                self.device.setOscStartColumn(x)
                self.device.setOscStartRow(y)
            
            elif msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysOffsetSingle) : #changes the offset for a single monome
                raise NotImplementedError()
                
        elif msg.getOscAddress() == MonomeOscSuffixesUtil.kOscDefaultAddrPatternSystemLedIntensity:
            if msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysLedIntensityAll):
                intensity = float(msg.getData()[0])

                self.device.oscLedIntensityChangeEvent(intensity)
            
            elif msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysLedIntensitySingle):
                raise NotImplementedError()

        elif msg.getOscAddress() == MonomeOscSuffixesUtil.kOscDefaultAddrPatternSystemLedTest:
            if msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysLedTestAll): #changes the leds intensity for all monomes
                state = bool(int(msg.getData()[0]))

                self.device.oscLedTestStateChangeEvent(state)
                
            elif msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysLedTestSingle): #changes the leds intensity for a single monome
                raise NotImplementedError()

        elif msg.getOscAddress() == MonomeOscSuffixesUtil.kOscDefaultAddrPatternSystemReport:
            if len(msg.getData()) == 0:
                raise NotImplementedError()

            elif msg.typeTagsMatch(MonomeOscSuffixesUtil.kOscDefaultTypeTagsSysReportSingle):
                raise NotImplementedError()
