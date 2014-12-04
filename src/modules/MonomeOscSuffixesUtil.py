class MonomeOscSuffixesUtil:
    kOscTypeTagInt = "i"
    kOscTypeTagFloat = "f"
    kOscTypeTagString = "s"

    kOscDefaultAddrPatternButtonPressSuffix = "/press"
    kOscDefaultAddrPatternLedStateSuffix = "/led"
    kOscDefaultAddrPatternLedIntensitySuffix = "/intensity"
    kOscDefaultAddrPatternLedTestSuffix = "/test"
    kOscDefaultAddrPatternAdcEnableSuffix = "/adc_enable"
    kOscDefaultAddrPatternShutdownSuffix = "/shutdown"
    kOscDefaultAddrPatternLedClearSuffix = "/clear"
    kOscDefaultAddrPatternAdcValueSuffix = "/adc"
    kOscDefaultAddrPatternTiltValueSuffix = "/tilt"
    kOscDefaultAddrPatternLedRowSuffix = "/led_row"
    kOscDefaultAddrPatternLedColumnSuffix = "/led_col"
    kOscDefaultAddrPatternEncEnableSuffix = "/enc_enable"
    kOscDefaultAddrPatternEncValueSuffix = "/enc"
    kOscDefaultAddrPatternLedFrameSuffix = "/frame"
    kOscDefaultAddrPatternLed_ModeSuffix = "/led_mode"
    kOscDefaultAddrPatternTilt_ModeSuffix	= "/tiltmode"

    kOscDefaultAddrPatternSystemPrefix = "/sys/prefix"
    kOscDefaultAddrPatternSystemCable = "/sys/cable"
    kOscDefaultAddrPatternSystemOffset = "/sys/offset"
    kOscDefaultAddrPatternSystemLedIntensity = "/sys/intensity"
    kOscDefaultAddrPatternSystemLedTest = "/sys/test"
    kOscDefaultAddrPatternSystemReport = "/sys/report"
    kOscDefaultAddrPatternSystemNumDevices  = "/sys/devices"


    kOscDefaultTypeTagsButtonPress = kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsLedState = kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsLedIntensity = kOscTypeTagFloat
    kOscDefaultTypeTagsLedTest = kOscTypeTagInt
    kOscDefaultTypeTagsAdcEnable = kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsShutdown = kOscTypeTagInt
    kOscDefaultTypeTagsLedClear = kOscTypeTagInt
    kOscDefaultTypeTagsAdcValue = kOscTypeTagInt +  kOscTypeTagFloat
    kOscDefaultTypeTagsLedRow = kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsLedColumn  = kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsEncEnable = kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsEncValue = kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsLedFrame = kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsLedOffsetFrame = kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsTiltMode = kOscTypeTagInt # added by dan

    kOscDefaultTypeTagsSysPrefixAll = kOscTypeTagString
    kOscDefaultTypeTagsSysPrefixSingle = kOscTypeTagInt +  kOscTypeTagString
    kOscDefaultTypeTagsSysCableAll = kOscTypeTagString
    kOscDefaultTypeTagsSysCableSingle = kOscTypeTagInt +  kOscTypeTagString
    kOscDefaultTypeTagsSysOffsetAll = kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsSysOffsetSingle = kOscTypeTagInt +  kOscTypeTagInt +  kOscTypeTagInt
    kOscDefaultTypeTagsSysLedIntensityAll = kOscDefaultTypeTagsLedIntensity
    kOscDefaultTypeTagsSysLedIntensitySingle = kOscTypeTagInt +  kOscDefaultTypeTagsLedIntensity
    kOscDefaultTypeTagsSysLedTestAll = kOscDefaultTypeTagsLedTest
    kOscDefaultTypeTagsSysLedTestSingle = kOscTypeTagInt +  kOscDefaultTypeTagsLedTest
    kOscDefaultTypeTagsSysReportSingle = kOscTypeTagInt
