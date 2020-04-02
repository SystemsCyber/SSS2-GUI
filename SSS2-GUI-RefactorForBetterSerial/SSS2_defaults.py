#SSS2 Default Settings Generator
import json

def get_default_settings():

    settings = {}
    settings["1: Message to User"]="This file is used to store settings for the SSS2.The SSS2 can be adjusted to match different ECUs. It is your responsibility to ensure the adjustments match the  application. Using the Smart Sensor Simulator 2 cannot guarantee a fault free environment for all electronic control units. If the elimination of fault codes is critical, then the user is encouraged to test the SSS2 settings with an exemplar module and adjust the settings accordingly. Only properly trained experts should use this software and product. This file should only be modified within the SSS2 Interface application."
    settings["Original File SHA"]="Current Settings Not Saved."
    settings["SSS2 Product Code"]="UNIVERSAL"
    settings["Component ID"] = "SYNER*SSS2-R05*XXXX*UNIVERSAL"
    settings["Software ID"]="SOFTWARE ID"
    settings["SSS2 Source Address"] = 0xFA
    settings["ECU Year"] = "YEAR"
    settings["ECU Make"] = "MAKE"
    settings["ECU Model"] = "MODEL"
    settings["Engine Serial Number"] = "SERIAL NUMBER"
    settings["Engine Model"] = "MODEL"
    settings["Engine Configuration"] = "CONFIGURATION"
    settings["Vehicle VIN"] = "VEHICLE IDENTIFICATION NUMBER"
    settings["Vehicle Year"] = "YEAR"
    settings["Vehicle Make"] = "MAKE"
    settings["Vehicle Model"] = "MODEL"
    settings["ECU Component ID"] = "COMPONENT IDENTIFICATION"
    settings["ECU Software Version"] = "SOFTWARE VERSION"
    settings["User Notes"]="USER ENTERED NOTES"
    settings["Programmed By"]="USER NAME"
    settings["Company"]="COMPANY NAME"
    settings["Original Creation Date"]="21 April 2017"
    settings["Saved Date"]="NOT SAVED"
    settings["Location"]="ADDRESS, CITY, STATE, ZIP"
    settings["Case Number"]="CASE IDENTIFIER"
    settings["Date of Loss"]="DATE"
    settings["SSS2 Cable"]=" "
    settings["SSS2 Interface Version"]="File Not Saved"
    settings["SSS2 Interface Release Date"]="File Not Saved"
    settings["Warnings"] = "Using the Smart Sensor Simulator 2 cannot guarantee a fault free environment for all electronic control units. If the elimination of fault codes is critical, then the user is encouraged to test the SSS2 settings with an exemplar module and adjust the settings accordingly. Only properly trained experts should use this software and product." 
    settings["Send SSS2 Component ID"] = "1"
    settings["Resistor Box Used"] = "Yes"
    settings["File Name"] = ""

    settings["Analog Calibration"] = [[.00000842,.00000842,.00000842,.00000842,.00000842,.00000842],
                                      [.0086833,.0086833,.0086833,.0086833,.0086833,.0086833],
                                      [.03378,.03378,.03378,.03378,.03378,.03378]]
    
    
    
    settings["Potentiometers"]={}
    p=settings["Potentiometers"]
    p["Group A"]={}
    p["Group B"]={}
    p["Others"]={}

    g=p["Group A"]
    g["Terminal A Connection"]=True
    g["SSS2 Setting"] = 73
    g["Label"]="Potentiometers 1 though 8"
    g["Pairs"]={"U1U2":{},"U3U4":{},"U5U6":{},"U7U8":{}}
    
    pair = g["Pairs"]["U1U2"]
    pair["Terminal A Voltage"] = "+5V"
    pair["SSS Setting"] = 25
    pair["Name"]="Terminal A Voltage for U1 and U2"
    pair["Pots"] = {"U1":{},"U2":{}}

    u=pair["Pots"]["U1"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=210
    u["Pin"]="J24:1"
    u["Wire Color"]="PPL/WHT"
    u["Port"]="1"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 1"
    u["SSS2 Wiper Setting"]=1
    u["SSS2 TCON Setting"]=51
    u["Resistance"]="10k"
    u["ECM Fault Low Setting"]=0
    u["ECM Fault High Setting"]=255
    
    u=pair["Pots"]["U2"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=200
    u["Pin"]="J24:2"
    u["Wire Color"]="BRN/WHT"
    u["Port"]="2"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 2"
    u["SSS2 Wiper Setting"]=2
    u["SSS2 TCON Setting"]=52
    u["Resistance"]="10k"

    pair = g["Pairs"]["U3U4"]
    pair["Terminal A Voltage"] = "+12V"
    pair["SSS Setting"] = 26
    pair["Name"]="Terminal A Voltage for U3 and U4"
    pair["Pots"] = {"U3":{},"U4":{}}

    u=pair["Pots"]["U3"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=190
    u["Pin"]="J24:3"
    u["Wire Color"]="YEL/BLK"
    u["Port"]="3"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 3"
    u["SSS2 Wiper Setting"]=3
    u["SSS2 TCON Setting"]=53
    u["Resistance"]="10k"
    
    u=pair["Pots"]["U4"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=False
    u["Wiper Connect"]=True
    u["Wiper Position"]=180
    u["Pin"]="J24:4"
    u["Wire Color"]="PNK/BLK"
    u["Port"]="4"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 4"
    u["SSS2 Wiper Setting"]=4
    u["SSS2 TCON Setting"]=54
    u["Resistance"]="10k"
        
    pair = g["Pairs"]["U5U6"]
    pair["Terminal A Voltage"] = "+12V"
    pair["SSS Setting"] = 27
    pair["Name"]="Terminal A Voltage for U5 and U6"
    pair["Pots"] = {"U5":{},"U6":{}}

    u=pair["Pots"]["U5"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=170
    u["Pin"]="J24:5"
    u["Wire Color"]="Blue"
    u["Port"]="5"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 5"
    u["SSS2 Wiper Setting"]=5
    u["SSS2 TCON Setting"]=55
    u["Resistance"]="10k"
    
    u=pair["Pots"]["U6"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=160
    u["Pin"]="J24:6"
    u["Wire Color"]="GRN/BLK"
    u["Port"]="6"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 6"
    u["SSS2 Wiper Setting"]=6
    u["SSS2 TCON Setting"]=56
    u["Resistance"]="100k"
    
    pair = g["Pairs"]["U7U8"]
    pair["Terminal A Voltage"] = "+12V"
    pair["SSS Setting"] = 28
    pair["Name"]="Terminal A Voltage for U7 and U8"
    pair["Pots"] = {"U7":{},"U8":{}}

    u=pair["Pots"]["U7"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=150
    u["Pin"]="J24:7"
    u["Wire Color"]="ORN/BLK"
    u["Port"]="7"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 7"
    u["SSS2 Wiper Setting"]=7
    u["SSS2 TCON Setting"]=57
    u["Resistance"]="100k"
    
    u=pair["Pots"]["U8"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=140
    u["Pin"]="J24:8"
    u["Wire Color"]="YEL/RED"
    u["Port"]="8"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 8"
    u["SSS2 Wiper Setting"]=8
    u["SSS2 TCON Setting"]=58
    u["Resistance"]="100k"
    


    g=p["Group B"]
    g["Terminal A Connection"]=True
    g["SSS2 Setting"] = 74
    g["Label"]="Potentiometers 9 though 16"
    g["Pairs"]={"U09U10":{},"U11U12":{},"U13U14":{},"U15U16":{}}
    
    pair = g["Pairs"]["U09U10"]
    pair["SSS Setting"] = 29
    pair["Terminal A Voltage"] = "+12V"
    pair["Name"]="Terminal A Voltage for U9 and U10"
    pair["Pots"] = {"U09":{},"U10":{}}

    u=pair["Pots"]["U09"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=130
    u["Pin"]= "J24:9"
    u["Wire Color"]="RED/WHT"
    u["Port"]= "9"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer  9"
    u["SSS2 Wiper Setting"]=9
    u["SSS2 TCON Setting"]=59
    u["Resistance"]="10k"
    
    u=pair["Pots"]["U10"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=120
    u["Pin"]= "J24:10"
    u["Wire Color"]="RED/BLK"
    u["Port"]="10"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 10"
    u["SSS2 Wiper Setting"]=10
    u["SSS2 TCON Setting"]=60
    u["Resistance"]="100k"

    pair = g["Pairs"]["U11U12"]
    pair["Terminal A Voltage"] = "+12V"
    pair["SSS Setting"] = 30
    pair["Name"]="Terminal A Voltage for U11 and U12"
    pair["Pots"] = {"U11":{},"U12":{}}

    u=pair["Pots"]["U11"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=110
    u["Pin"]="J24:11"
    u["Wire Color"]="BLU/WHT"
    u["Port"]="11"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 11"
    u["SSS2 Wiper Setting"]=11
    u["SSS2 TCON Setting"]=61
    u["Resistance"]="10k"
    
    u=pair["Pots"]["U12"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=100
    u["Pin"]="J24:12"
    u["Wire Color"]="TAN/BLK"
    u["Port"]="12"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 12"
    u["SSS2 Wiper Setting"]=12
    u["SSS2 TCON Setting"]=62
    u["Resistance"]="100k"
        
    pair = g["Pairs"]["U13U14"]
    pair["Terminal A Voltage"] = "+12V"
    pair["SSS Setting"] = 31
    pair["Name"]="Terminal A Voltage for U13 and U14"
    pair["Pots"] = {"U13":{},"U14":{}}

    u=pair["Pots"]["U13"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=90
    u["Pin"]="J24:13"
    u["Wire Color"]="Brown"
    u["Port"]="13"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 13"
    u["SSS2 Wiper Setting"]=13
    u["SSS2 TCON Setting"]=63
    u["Resistance"]="10k"
    
    u=pair["Pots"]["U14"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=80
    u["Pin"]="J24:14"
    u["Wire Color"]="BLK/WHT"
    u["Port"]="14"
    u["ECU Pins"] = "ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 14"
    u["SSS2 Wiper Setting"]=14
    u["SSS2 TCON Setting"]=64
    u["Resistance"]="100k"
    
    pair = g["Pairs"]["U15U16"]
    pair["Terminal A Voltage"] = "+12V"
    pair["SSS Setting"] = 32
    pair["Name"]="Terminal A Voltage for U15 and U16"
    pair["Pots"] = {"U15":{},"U16":{}}

    u=pair["Pots"]["U15"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=70
    u["Pin"]= "J24:15"
    u["Wire Color"]="GRN/WHT"
    u["Port"]="15"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 15"
    u["SSS2 Wiper Setting"]=15
    u["SSS2 TCON Setting"]=65
    u["Resistance"]="10k"
    
    u=pair["Pots"]["U16"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=60
    u["Pin"]= "J24:16"
    u["Wire Color"]="RED/GRN"
    u["Port"]= "16"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Potentiometer 16"
    u["SSS2 Wiper Setting"]=16
    u["SSS2 TCON Setting"]=66
    u["Resistance"]="100k"
    


    g=p["Others"]
    g["Terminal A Connection"]=None
    g["Label"]="Potentiometers 17 though 19"
    g["SSS2 Setting"] = None
    g["Pairs"]={"I2CPots":{}}
    
    pair = g["Pairs"]["I2CPots"]
    pair["Terminal A Voltage"] = None
    pair["Name"] = "Terminal A Voltage is Fixed at +5V"
    pair["SSS Setting"] = None    
    pair["Pots"] = {"U34":{},"U36":{},"U37":{}}

    u=pair["Pots"]["U34"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=20
    u["Pin"]= "J18:12"
    u["Wire Color"]="TAN/BLK"
    u["Port"]= "28"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Port 28 Potentiometer"
    u["SSS2 Wiper Setting"]=75
    u["SSS2 TCON Setting"]=78
    u["Resistance"]="100k"
    
    u=pair["Pots"]["U36"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=50
    u["Pin"]= "J18:13"
    u["Wire Color"]="BROWN"
    u["Port"]= "29"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Port 29 Potentiometer"
    u["SSS2 Wiper Setting"]=76
    u["SSS2 TCON Setting"]=79
    u["Resistance"]="10k"

    u=pair["Pots"]["U37"]
    u["Terminal Value"]=7
    u["Term. A Connect"]=True
    u["Term. B Connect"]=True
    u["Wiper Connect"]=True
    u["Wiper Position"]=50
    u["Pin"]= "J18:14"
    u["Wire Color"]="GRN/WHT"
    u["Port"]= "30"
    u["ECU Pins"]="ECU Pins"
    u["Application"]="Application Description"
    u["Name"]="Port 30 Potentiometer"
    u["SSS2 Wiper Setting"]=77
    u["SSS2 TCON Setting"]=80
    u["Resistance"]="100k"
    
    settings["DACs"]={}
    for i in range(1,9):
        settings["DACs"]["Vout{}".format(i)]={}
    

    d=settings["DACs"]["Vout1"]
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Average Voltage"]=2.5 #DC value
    d["Amplitude"]=0
    d["SSS2 setting"] = 17
    d["Show Amplitude"]=False
    d["Frequency"]=0
    d["Show Frequency"]=False
    d["Shape"]="Constant" #Sine, Square, Triangle or Sawtooth
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Pin"]= "J18:2"
    d["Wire Color"]="BRN/WHT"
    d["Port"]= "18"
    d["Alt. Pin"]="J24:15"
    d["Alt. Pin Connect"]=False
    d["Name"] = "Vout A"
     
    d=settings["DACs"]["Vout2"]
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Average Voltage"]=2.5 #DC value
    d["SSS2 setting"] = 18
    d["Amplitude"]=0
    d["Show Amplitude"]=False
    d["Frequency"]=0
    d["Show Frequency"]=False
    d["Shape"]="Constant" #Sine, Square, Triangle or Sawtooth
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Pin"]= "J18:3"
    d["Wire Color"]="WHT/BLK"
    d["Port"]= "19"
    d["Alt. Pin"]="J24:10"
    d["Alt. Pin Connect"]=False
    d["Name"] = "Vout B"
 

    d=settings["DACs"]["Vout3"]
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Average Voltage"]=2.5 #DC value
    d["Amplitude"]=0
    d["SSS2 setting"] = 19
    d["Show Amplitude"]=False
    d["Frequency"]=0
    d["Show Frequency"]=False
    d["Shape"]="Constant" #Sine, Square, Triangle or Sawtooth
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Pin"]= "J18:4"
    d["Wire Color"]="PNK/BLK"
    d["Port"]= "20"
    d["Alt. Pin"]=None
    d["Alt. Pin Connect"]=False
    d["Name"] = "Vout C"
  
    d=settings["DACs"]["Vout4"]
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Average Voltage"]=2.5 #DC value
    d["SSS2 setting"] = 20
    d["Amplitude"]=0
    d["Show Amplitude"]=False
    d["Frequency"]=0
    d["Show Frequency"]=False
    d["Shape"]="Constant" #Sine, Square, Triangle or Sawtooth
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Pin"]= "J18:5"
    d["Wire Color"]="Pink"
    d["Port"]= "21"
    d["Alt. Pin"]=None
    d["Alt. Pin Connect"]=False
    d["Name"] = "Vout D"
 
    d=settings["DACs"]["Vout5"]
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Average Voltage"]=2.5 #DC value
    d["SSS2 setting"] = 21
    d["Amplitude"]=0
    d["Show Amplitude"]=False
    d["Frequency"]=0
    d["Show Frequency"]=False
    d["Shape"]="Constant" #Sine, Square, Triangle or Sawtooth
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Pin"]= "J18:6"
    d["Wire Color"]="Blue"
    d["Port"]= "22"
    d["Alt. Pin"]=None
    d["Alt. Pin Connect"]=False
    d["Name"] = "Vout E"
 
    d=settings["DACs"]["Vout6"]
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Average Voltage"]=2.5 #DC value
    d["SSS2 setting"] = 22
    d["Amplitude"]=0
    d["Show Amplitude"]=False
    d["Frequency"]=0
    d["Show Frequency"]=False
    d["Shape"]="Constant" #Sine, Square, Triangle or Sawtooth
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Pin"]= "J18:7"
    d["Wire Color"]="Tan"
    d["Port"]= "23"
    d["Alt. Pin"]=None
    d["Alt. Pin Connect"]=False
    d["Name"] = "Vout F"

    d=settings["DACs"]["Vout7"]
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Average Voltage"]=2.5 #DC value
    d["SSS2 setting"] = 23
    d["Amplitude"]=0
    d["Show Amplitude"]=False
    d["Frequency"]=0
    d["Show Frequency"]=False
    d["Shape"]="Constant" #Sine, Square, Triangle or Sawtooth
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Pin"]= "J18:8"
    d["Wire Color"]="ORN/BLK"
    d["Port"]= "24"
    d["Alt. Pin"]=None
    d["Alt. Pin Connect"]=False
    d["Name"] = "Vout G"

    d=settings["DACs"]["Vout8"]
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Average Voltage"]=2.5 #DC value
    d["SSS2 setting"] = 24
    d["Amplitude"]=0
    d["Show Amplitude"]=False
    d["Frequency"]=0
    d["Show Frequency"]=False
    d["Shape"]="Constant" #Sine, Square, Triangle or Sawtooth
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Pin"]= "J18:9"
    d["Wire Color"]="YEL/BLK"
    d["Port"]= "25"
    d["Alt. Pin"]=None
    d["Alt. Pin Connect"]=False
    d["Name"] = "Vout H"

    settings["HVAdjOut"]={}
    d=settings["HVAdjOut"]
    d["Shape"]="Constant" #Sine, Square, Triangle or Sawtooth
    d["ECU Pins"]="ECU Pins"
    d["Show Amplitude"]=False
    d["Frequency"]=0
    d["Show Frequency"]=False
    d["Frequency"]= 0
    d["Average Voltage"]=8.5
    d["Lowest Voltage"]= 1.9
    d["Pin"]= "J24:19"
    d["Wire Color"]="TAN"
    d["Port"]= " "
    d["Alt. Pin"]=None
    d["Alt. Pin Connect"]=False
    d["Name"] ="High Current Regulator"
    d["Application"]="Application Description"
    d["SSS2 setting"] = 49
    d["Highest Voltage"] = 11.0
    d["Amplitude"]=0
    d["Value"] = 100

            
    settings["PWMs"]={}
    for i in range(1,7):
        settings["PWMs"]["PWM{}".format(i)]={}

    d=settings["PWMs"]["PWM1"]
    d["Name"] = "PWM1"
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Duty Cycle"]=1 
    d["SSS2 setting"] = 33
    d["Frequency"]=400
    d["Lowest Frequency"]=245
    d["Highest Frequency"]=5000
    d["SSS2 freq setting"] = 81
    d["Show Frequency"]=True
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Port"]= "31"
    d["Pin"]= "J24:13"
    d["Wire Color"]="BROWN"
    d["Pin Connect"]=True
    d["SSS2 pin setting"] = 67
    d["Alt. Port"]="13"
    d["Alt. Pin"]="J18:15"
    d["Alt. Pin Connect"]=True
    d["SSS2 alt setting"] = 40


    d=settings["PWMs"]["PWM2"]
    d["Name"] = "PWM2"
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Duty Cycle"]=2
    d["SSS2 setting"] = 34
    d["Frequency"]=400
    d["Lowest Frequency"]=245
    d["Highest Frequency"]=5000
    d["SSS2 freq setting"] = 82
    d["Show Frequency"]=True
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Port"]= "32"
    d["Pin"]= "J24:14"
    d["Wire Color"]="BLK/WHT"
    d["Pin Connect"]=True
    d["SSS2 pin setting"] = 68
    d["Alt. Port"]="14"
    d["Alt. Pin"]="J18:16"
    d["Alt. Pin Connect"]=True
    d["SSS2 alt setting"] = 40

    d=settings["PWMs"]["PWM3"]
    d["Name"] = "PWM3"
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Duty Cycle"]=3 
    d["SSS2 setting"] = 35
    d["Frequency"]=400
    d["Lowest Frequency"]=0
    d["Highest Frequency"]=5000
    d["SSS2 freq setting"] = 83
    d["Show Frequency"]=True
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Port"]= "27"
    d["Pin"]= "J18:10"
    d["Wire Color"]="Orange"
    d["Pin Connect"]=True
    d["SSS2 pin setting"] = 69
    d["Alt. Port"]=None
    d["Alt. Pin"]=""
    d["Alt. Pin Connect"]=None
    d["SSS2 alt setting"] =None

    d=settings["PWMs"]["PWM4"]
    d["Name"] = "PWM4"
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Duty Cycle"]=4 
    d["SSS2 setting"] = 36
    d["Frequency"]=400
    d["Lowest Frequency"]=0
    d["Highest Frequency"]=5000
    d["SSS2 freq setting"] = 84
    d["Show Frequency"]=True
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Port"]= "17"
    d["Pin"]= "J18:1"
    d["Wire Color"]="PPL/WHT"
    d["Pin Connect"]=True
    d["SSS2 pin setting"] = 70
    d["Alt. Port"]=None
    d["Alt. Pin"]=""
    d["Alt. Pin Connect"]=None
    d["SSS2 alt setting"] =None

    d=settings["PWMs"]["PWM5"]
    d["Name"] = "PWM5"
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Duty Cycle"]=50 
    d["SSS2 setting"] = 87
    d["Frequency"]=200
    d["Lowest Frequency"]=0
    d["Highest Frequency"]=5000
    d["SSS2 freq setting"] = 85
    d["Show Frequency"]=True
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Port"]= "17"
    d["Pin"]= "J24:2"
    d["Wire Color"]="BRN/WHT"
    d["Pin Connect"]=True
    d["SSS2 pin setting"] = 70
    d["Alt. Port"]=None
    d["Alt. Pin"]=""
    d["Alt. Pin Connect"]=None
    d["SSS2 alt setting"] =None

    d=settings["PWMs"]["PWM6"]
    d["Name"] = "PWM6"
    d["Lowest Voltage"]=0
    d["Highest Voltage"]=5
    d["Duty Cycle"]=50
    d["SSS2 setting"] = 88
    d["Frequency"]=200
    d["Lowest Frequency"]=0
    d["Highest Frequency"]=5000
    d["SSS2 freq setting"] = 85
    d["Show Frequency"]=True
    d["ECU Pins"]="ECU Pins"
    d["Application"]="Application Description"
    d["Port"]= "17"
    d["Pin"]= "J24:1"
    d["Wire Color"]="PPL/WHT"
    d["Pin Connect"]=True
    d["SSS2 pin setting"] = 70
    d["Alt. Port"]=None
    d["Alt. Pin"]=""
    d["Alt. Pin Connect"]=None
    d["SSS2 alt setting"] =None

    
    
    settings["Switches"]={}
    s=settings["Switches"]
    s["Port 10 or 19"]={"SSS2 setting":37,"State":False,"Label A":"Connect Vout B to J24:10","Label B":"Connect Potentiometer 10 to J24:10"}
    s["Port 15 or 18"]={"SSS2 setting":38,"State":False,"Label A":"Connect Vout A to J24:15","Label B":"Connect Potentiometer 15 to J24:15"}
    s["CAN2 or J1708"]={"SSS2 setting":39,"State":True,"Label A":"Connect J1708 to J24:17 and J24:18","Label B":"Connect CAN2 to J24:17 and J24:18"}
    s["PWMs or CAN2"]={"SSS2 setting":40,"State":True,"Label A":"Connect CAN2 to J18:15 and J18:16","Label B":"Connect PWM1 to J18:15 and PWM2 to J18:16"}
    s["CAN0 Resistor 1"]={"SSS2 setting":41,"State":True,"Label":"Connect CAN0 (FlexCAN0) Termination Resistor 1(J1939)"}
    s["CAN1 Resistor 1"]={"SSS2 setting":42,"State":True,"Label":"Connect CAN1 (MCP-CAN) Termination Resistor 1"}
    s["CAN2 Resistor 1"]={"SSS2 setting":43,"State":True,"Label":"Connect CAN2 (FlexCAN1) Termination Resistor 1 (E-CAN)"}
    s["LIN Master Pullup Resistor"]={"SSS2 setting":44,"State":True,"Label":"Connect LIN Master Pullup Resistor"}
    s["PWM3 or 12V"]={"SSS2 setting":45,"State":False,"Label A":"Connect J18:10 to +12VDC","Label B":"Connect PWM3 Output to J18:10"}
    s["12V Out 2"]={"SSS2 setting":46,"State":False,"Label":"Connect +12V to Port 11 (J24:11)"}
    s["PWM4 or Ground"]={"SSS2 setting":47,"State":False,"Label A":"Connect J18:1 to Ground","Label B":"Connect PWM4 Output to J18:1"}
    s["Ground Out 2"]={"SSS2 setting":48,"State":False,"Label":"Connect Ground to Port 12 (J24:12)"}
    s["Ignition"]={"SSS2 setting":50,"State":False,"Label":"Ignition Key Switch Relay (J24:20)"}
    s["PWM1 Connect"]={"SSS2 setting":67,"State":True,"Label":"Connect PWM1 Output to J24:13"}
    s["PWM2 Connect"]={"SSS2 setting":68,"State":True,"Label":"Connect PWM2 Output to J24:14"}
    s["PWM3 Connect"]={"SSS2 setting":69,"State":True,"Label":"Connect PWM3 Output to J18:10"}
    s["PWM4 Connect"]={"SSS2 setting":70,"State":True,"Label":"Connect PWM4 Output to J18:1"}
    s["LIN to SHLD"]={"SSS2 setting":71,"State":False,"Label":"Connect LIN to Round Pin E (J10:5)"}
    s["LIN to Port 16"]={"SSS2 setting":72,"State":False,"Label":"Connect LIN to Port 16 (J24:16)"}
    s["PWM4_28 Connect"]={"SSS2 setting":86,"State":True,"Label":"Connect PWM4 Output to J18:12"}
    s["PWM5 Connect"]={"SSS2 setting":89,"State":False,"Label":"Connect PWM5 Output to J24:2"}
    s["PWM6 Connect"]={"SSS2 setting":90,"State":False,"Label":"Connect PWM6 Output to J24:1"}
    s["CAN1 Connect"]={"SSS2 setting":91,"State":False,"Label":"Connect CAN1 (MCPCAN) to J24:3 and J24:4"}
    s["CAN0 Resistor 2"]={"SSS2 setting":93,"State":True,"Label":"Connect CAN0 (FlexCAN0) Termination Resistor 2 (J1939)"}
    s["CAN1 Resistor 2"]={"SSS2 setting":94,"State":True,"Label":"Connect CAN1 (MCP-CAN) Termination Resistor 2"}
    s["CAN2 Resistor 2"]={"SSS2 setting":95,"State":True,"Label":"Connect CAN2 (FlexCAN1) Termination Resistor 2 (E-CAN)"}
     
    
    
    settings["CAN Config"]={"CAN0 Baudrate":"250000", "MCPCAN Baudrate":"250000","CAN1 Baudrate":"500000", "Buffer Size":1000000}

    settings["CAN"]={}
    t=settings["CAN"]
    t["  1.000"]="DDEC MCM 01,1,1,0,1,10,   0,0,1, 8FF0001,8, 0, 0, 0, 0, 0, 0, 0, 0,No" 
    t["  2.000"]="DDEC TCM 01,2,1,0,1,10,   0,0,1, CF00203,8, 0, 0, 0, 0, 0, 0, 0, 0,No" 
    t["  3.000"]="DDEC TCM 02,3,1,0,1,10,   0,0,1, 8FF0303,8, 0, 0, 0, 0, 0, 0, 0, 0,No" 
    t["  4.000"]="DDEC TCM 03,4,1,0,1,100,   0,0,1,18F00503,8, 0, 0, 0, 0, 0, 0, 0, 0,No"
    t["  5.000"]="HRW from Brake Controller,5,1,0,0,20,0,0,1, CFE6E0B,8, 0, 0, 0, 0, 0, 0, 0, 0,No" 
    t["  6.000"]="EBC1 from Cab Controller, 6,1,0,0, 100,0,0,1,18F00131,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
    t["  7.000"]="EBC1 from Brake Controller, 7,1,0,0, 100,0,0,1,18F0010B,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
    t["  8.000"]="CCVS1 from Instrument Cluster, 8,1,0,0, 100,0,0,1,18FEF117,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
    t["  9.000"]="CCVS1 from Cab Display 1, 9,1,0,0,100,0,0,1,18FEF128,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
    t[" 10.000"]="CCVS1 from Body Controller, 10,1,0,0,100,0,0,1,18FEF121,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
    t[" 11.000"]="CCVS1 from Cab Controller,11,1,0,0,100,0,0,1,18FEF131,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
    t[" 12.000"]="CM1 from Instrument Cluster,12,1,0,0,100,   0,0,1,18E00017,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes"
    t[" 13.000"]="CM1 from Climate Control 1,13,1,0,0,100,   0,0,1,18E00019,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
    t[" 14.000"]="CM1 from Body Controller,14,1,0,0,100,   0,0,1,18E00021,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
    t[" 15.000"]="CM1 from Cab Display,15,1,0,0,100,   0,0,1,18E00028,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes"
    t[" 16.000"]="CM1 from Cab Controller,16,1,0,0,100,   0,0,1,18E00031,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes"
    t[" 17.000"]="PTO from Instrument Cluster,17,1,0,0, 100,   0,0,1,18FEF017,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
    t[" 18.000"]="PTO from Body Controller,18,1,0,0,100,   0,0,1,18FEF021,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
    t[" 19.000"]="PTO from Cab Display,19,1,0,0, 100,   0,0,1,18FEF028,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes"
    t[" 20.000"]="PTO from Cab Controller,20,1,0,0, 100,   0,0,1,18FEF031,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes"
    t[" 21.000"]="AMB from Body Controller,21,1,0,0,1000,   0,0,1,18FEF521,8, 0, 0, 0, 0, 0, 0, 0, 0,Yes" 
                
    return settings

def get_default_wiring():
    wiring_dict={}
    wiring_dict["J24:17"]={"Wire Color":"PURPLE","Application":"CAN2L/J1708-","ECU Pins":""}
    wiring_dict["J24:18"]={"Wire Color":"PINK","Application":"CAN2H/J1708+","ECU Pins":""}
    wiring_dict["J24:19"]={"Wire Color":"TAN","Application":"Adj Pwr Out","ECU Pins":""}
    wiring_dict["J24:20"]={"Wire Color":"ORANGE","Application":"Ignition","ECU Pins":""}
    wiring_dict["J24:21"]={"Wire Color":"GREEN","Application":"J1939L","ECU Pins":""}
    wiring_dict["J24:22"]={"Wire Color":"YELLOW","Application":"J1939H","ECU Pins":""}
    wiring_dict["J24:23"]={"Wire Color":"RED","Application":"+12V Out","ECU Pins":""}
    wiring_dict["J24:24"]={"Wire Color":"BLACK","Application":"Ground","ECU Pins":""}
    wiring_dict["J18:18"]={"Wire Color":"BLACK","Application":"Ground","ECU Pins":""}
    wiring_dict["J18:17"]={"Wire Color":"RED","Application":"Battery +","ECU Pins":""}
    wiring_dict["J18:16"]={"Wire Color":"YELLOW","Application":"CAN2H","ECU Pins":""}
    wiring_dict["J18:15"]={"Wire Color":"GREEN","Application":"CAN2L","ECU Pins":""}
    wiring_dict["J18:11"] ={"Wire Color":"PURPLE","Application":"Adj Pwr Out","ECU Pins":""}
    return wiring_dict

if __name__ == '__main__':
    settings=get_default_settings()
    with open('defaults.SSS2','w') as outfile:
        json.dump(settings,outfile,indent=4,sort_keys=True)
    
