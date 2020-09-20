#Python 3
"""
This program requires the usb driver libusb0_x86.dll
to be installed in a system path, like c:\Windows\System32
"""
#
from PyQt5.QtWidgets import (QMainWindow,
                             QWidget,
                             QTreeView,
                             QMessageBox,
                             QFileDialog,
                             QLabel,
                             QSlider,
                             QCheckBox,
                             QLineEdit,
                             QVBoxLayout,
                             QApplication,
                             QPushButton,
                             QTableWidget,
                             QTableView,
                             QTableWidgetItem,
                             QHeaderView,
                             QScrollArea,
                             QAbstractScrollArea,
                             QAbstractItemView,
                             QSizePolicy,
                             QGridLayout,
                             QGroupBox,
                             QComboBox,
                             QAction,
                             QTreeWidget,
                             QTreeWidgetItem,
                             QDialog,
                             QFrame,
                             QDialogButtonBox,
                             QInputDialog,
                             QProgressDialog,
                             QPlainTextEdit,
                             QSizePolicy,
                             QTabWidget)
from PyQt5.QtCore import Qt, QTimer, QAbstractTableModel, QCoreApplication, QSize, QAbstractItemModel, QSortFilterProxyModel, QVariant
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

import winshell
import hashlib

#from TableModel import *

import os
import sys
import threading
import queue
import time
import usb.core
import usb.util
import struct
import json
import traceback
import struct
import traceback

import logging
import logging.config
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
logging.basicConfig()
logger.debug("Starting SSS2 Interface")

from SSS2_defaults import *

release_title = "SSS2 Interface"
release_date = "1 September 2019"
release_version = "2.0.0"

CAN_MESSAGE_BASE    = 0x20
TIMESTAMP_OFFSET    = 0
CHANNEL_DLC_OFFSET  = 4
MICROSECONDS_OFFSET = 5
CAN_ID_OFFSET       = 8
CAN_DATA_OFFSET     = 12
CAN_SEND_MS         = 3
CAN_FRAME_LENGTH    = 20

MAX_COMMAND_STRING_LENGTH = 50

USB_HID_OUTPUT_ENDPOINT_ADDRESS = 0x04
USB_HID_INPUT_ENDPOINT_ADDRESS = 0x81
USB_HID_LENGTH = 64
USB_HID_TIMEOUT = 0 # 0 = Blocking
USB_MESSAGE_TIMEOUT = 5 #Seconds

USB_FRAME_TYPE_MASK =  0xF0
USB_FRAME_TYPE_LOC  =     0
STATUS_TYPE         =  0x00
COMMAND_TYPE        =  0x10
MESSAGE_TYPE        =  0x20
CAN_THREADS_TYPE    =  0x40
ESCAPE_TYPE         =  0x80

CONFIGSWITCH_1_LOC   = 34
U1U2P0ASWITCH_MASK   = 0x01
U3U4P0ASWITCH_MASK   = 0x02
U5U6P0ASWITCH_MASK   = 0x04
U7U8P0ASWITCH_MASK   = 0x08
U9U10P0ASWITCH_MASK  = 0x10
U11U12P0ASWITCH_MASK = 0x20
U13U14P0ASWITCH_MASK = 0x40
U15U16P0ASWITCH_MASK = 0x80

CONFIGSWITCH_2_LOC  = 33
LINTOSHIELD_MASK    = 0x01
LINTO16_MASK        = 0x02
P10OR19SWITCH_MASK  = 0x04
P15OR18SWITCH_MASK  = 0x08
U28P0AENABLE_MASK   = 0x10
U31P0AENABLE_MASK   = 0x20
J1708ORCAN1_MASK    = 0x40
CAN2CONNECT_MASK    = 0x80

PWMSWITCHES_LOC     = 47
CAN0TERM1_MASK    = 0x01
CAN1TERM1_MASK    = 0x02
CAN2TERM1_MASK    = 0x04
LIN_PULLUP_MASK   = 0x08
PWM1_CONNECT_MASK = 0x10
PWM2_CONNECT_MASK = 0x20
PWM3_CONNECT_MASK = 0x40
PWM4_CONNECT_MASK = 0x80

TERMSWITCHES_LOC  = 52
CAN0TERM2_MASK    = 0x01
CAN1TERM2_MASK    = 0x02
CAN2TERM2_MASK    = 0x04
PWM4_P28_MASK     = 0x08
MISSING_MASK      = 0x10
CAN1_CONNECT_MASK = 0x20
PWM5_CONNECT_MASK = 0x40
PWM6_CONNECT_MASK = 0x80

HBRIDGE_LOC         = 60
TWELVE_OUT_1_MASK   = 0x01
TWELVE_OUT_2_MASK   = 0x02
GROUND_OUT_1_MASK   = 0x04
GROUND_OUT_2_MASK   = 0x08
IGNITION_RELAY_MASK = 0x80

HVADJOUT_LOC = 48
HVADJOUT_MASK = 0xFF

U34_I2C_ADDR = 0x3C
U36_I2C_ADDR = 0x3F
U37_I2C_ADDR = 0x3D

U34_WIPER_LOC =  49
U36_WIPER_LOC =  50
U37_WIPER_LOC =  51

U34_TCON_LOC = 17
U36_TCON_LOC = 18
U37_TCON_LOC = 19

PWM1_LOC = 35
PWM2_LOC = 37
PWM3_LOC = 39
PWM4_LOC = 41
PWM5_LOC = 43
PWM6_LOC = 45


PWM1_FREQ_LOC = 52
PWM2_FREQ_LOC = 54
PWM3_FREQ_LOC = 56
PWM5_FREQ_LOC = 58

WIPER_TCON_MASK = 2
TERMB_TCON_MASK = 1
TERMA_TCON_MASK = 4

CAN_4K096BPS  = 0
CAN_5KBPS     = 1
CAN_10KBPS    = 2
CAN_20KBPS    = 3
CAN_31K25BPS  = 4
CAN_33K3BPS   = 5
CAN_40KBPS    = 6
CAN_50KBPS    = 7
CAN_80KBPS    = 8
CAN_100KBPS   = 9
CAN_125KBPS   = 10
CAN_200KBPS   = 11
CAN_250KBPS   = 12
CAN_500KBPS   = 13
CAN_1000KBPS  = 14
CAN_666KBPS   = 15

NET_STATUS_LOC    =  59
STREAM_CAN0_MASK  = 0x01
STREAM_CAN1_MASK  = 0x02
STREAM_CAN2_MASK  = 0x04
STREAM_J1708_MASK = 0x08
SEND_LIN_MASK     = 0x10
SEND_VOLTAGE_MASK = 0x20
SEND_COMPONENT_ID = 0x40
SUPPRESS_LIN_MASK = 0x80

CAN_SPEEDS = [4096,
              5000,  
              10000,  
              20000,  
              31250,
              33333, 
              40000,  
              50000,  
              80000,  
              100000, 
              125000, 
              200000, 
              250000, 
              500000, 
              1000000,
              666666]

CAN0_BAUD_LOC = 20
CAN1_BAUD_LOC = 21
CAN2_BAUD_LOC = 22

CAN0_RX_COUNT_LOC  = 29
CAN1_RX_COUNT_LOC  = 33
CAN2_RX_COUNT_LOC  = 37
CAN0_TX_COUNT_LOC  = 41
CAN1_TX_COUNT_LOC  = 45
CAN2_TX_COUNT_LOC  = 49
J1708_RX_COUNT_LOC = 53
LIN_RX_COUNT_LOC   = 55
LIN_TX_COUNT_LOC   = 57

SWITCH_NAMES = ["Port 10 or 19",
                "Port 15 or 18",
                "CAN2 or J1708",
                "PWMs or CAN2",
                "CAN0 Resistor 1",
                "CAN1 Resistor 1",
                "CAN2 Resistor 1",
                "LIN Master Pullup Resistor",
                "PWM3 or 12V",
                "12V Out 2",
                "PWM4 or Ground",
                "Ground Out 2",
                "PWM1 Connect",
                "PWM2 Connect",
                "PWM3 Connect",
                "PWM4 Connect",
                "LIN to SHLD",
                "LIN to Port 16",
                "Ignition",
                "PWM4_28 Connect",
                "PWM5 Connect",
                "PWM6 Connect",
                "CAN1 Connect",
                "CAN0 Resistor 2",
                "CAN2 Resistor 2",
                "CAN1 Resistor 2"]

PWM_NAMES = ["PWM1",
             "PWM2",
             "PWM3",
             "PWM4",
             "PWM5",
             "PWM6"]

VOUT_NAMES = ["Vout1",
              "Vout2",
              "Vout3",
              "Vout4",
              "Vout5",
              "Vout6",
              "Vout7",
              "Vout8"]

GROUP_NAMES = ["Group A",
               "Group A",
               "Group A",
               "Group A",
               "Group B",
               "Group B",
               "Group B",
               "Group B"]


PAIR_NAMES = ["U1U2",
              "U3U4",
              "U5U6",
              "U7U8",
              "U09U10",
              "U11U12",
              "U13U14",
              "U15U16"]

ALL_GROUPS = ["Group A",
              "Group A",
              "Group A",
              "Group A",
              "Group A",
              "Group A",
              "Group A",
              "Group A",
              "Group B",
              "Group B",
              "Group B",
              "Group B",
              "Group B",
              "Group B",
              "Group B",
              "Group B",
              "Others",
              "Others",
              "Others"]

ALL_PAIRS = ["U1U2",
             "U1U2",
             "U3U4",
             "U3U4",
             "U5U6",
             "U5U6",
             "U7U8",
             "U7U8",
             "U09U10",
             "U09U10",
             "U11U12",
             "U11U12",
             "U13U14",
             "U13U14",
             "U15U16",
             "U15U16",
             "I2CPots",
             "I2CPots",
             "I2CPots"]

ALL_POTS = ["U1",
            "U2",
            "U3",
            "U4",
            "U5",
            "U6",
            "U7",
            "U8",
            "U09",
            "U10",
            "U11",
            "U12",
            "U13",
            "U14",
            "U15",
            "U16",
            "U34",
            "U36",
            "U37"]


def crc16_ccitt(crc, data):
    msb = (crc & 0xFF00) >> 8
    lsb = crc & 0xFF
    for c in data:
        x = c ^ msb
        x ^= (x >> 4)
        msb = (lsb ^ (x >> 3) ^ (x << 4)) & 255
        lsb = (x ^ (x << 5)) & 255
    return bytes([lsb, msb])

def calculate_sha256(filename):
    with open(filename,'rb') as infile:
        contents = infile.read()
    return hashlib.sha256(contents).hexdigest()

class USBThread(threading.Thread):
    def __init__(self, parent, rx_queue):
        self.root = parent
        threading.Thread.__init__(self)
        self.rx_queue = rx_queue
        self.root.usb_signal = True

    def run(self):
        while True:
            time.sleep(0.001)
            try:
                data_stream = bytes(self.root.sss.read(USB_HID_INPUT_ENDPOINT_ADDRESS, USB_HID_LENGTH, USB_HID_TIMEOUT))
                data_stream_crc = data_stream[62:64]
                calculated_crc = crc16_ccitt(0xFFFF, data_stream[0:62])
                if data_stream_crc == calculated_crc:
                  self.rx_queue.put(data_stream[:62])
                  self.root.usb_signal = True
                else:
                  logger.debug('CRC Check Failed.')
            except usb.core.USBError:
                break
            except AttributeError:
                break
            except:
                logger.debug(traceback.format_exc())
                break
        logger.debug("USBThread Ending.")
        usb.util.release_interface(self.root.sss,self.root.sss_interface)
        self.root.usb_signal = False
        time.sleep(1)

class SSS2Interface(QMainWindow):
    def __init__(self):
        super(SSS2Interface, self).__init__()
        self.settings_dict = get_default_settings()
        self.usb_signal = False
        self.last_usb_message_time = time.time()
        self.edit_settings = False
        self.load_settings = False
        self.can_dict={}
        self.can_generator_dict = {}
        #self.entryset = set()
        self.status_message_2 = b'\x00'*64
        self.export_path =  os.path.join(winshell.my_documents(), "SSS2")
        if not os.path.isdir(self.export_path):
            os.makedirs(self.export_path)
        self.filename = "default.SSS2"
        with open(os.path.join(self.export_path,self.filename),'w') as f:
            json.dump(self.settings_dict,f,indent=4,sort_keys=True)
        self.setWindowTitle('{} {} - {}'.format(release_title,
                                                release_version,
                                                self.filename))        
        self.init_gui()
        self.show()
        logger.debug("Done Initializing GUI")
        self.setup_usb()
        read_timer = QTimer(self)
        read_timer.timeout.connect(self.read_usb_hid)
        read_timer.start(109) #milliseconds

    def send_command(self, command_string):
        if self.usb_signal:
            data = b'\x10' + command_string.encode('ascii')
            padded_data = data + bytes([0 for i in range(62 - len(data))])
            crc = crc16_ccitt(0xFFFF, bytes(padded_data[0:62]))
            data_to_send = bytes(padded_data[0:62]) + crc
            self.sss.write(USB_HID_OUTPUT_ENDPOINT_ADDRESS, data_to_send, USB_HID_TIMEOUT)
            logger.debug(command_string)
            time.sleep(0.01)
        else:
            logger.debug("Failed to Send. No USB.")

    def setup_usb(self):
        # find our device
        self.sss = None
        for device in usb.core.find(find_all=True, idVendor=0x16c0, idProduct=0x0486):
            self.sss = device

        # was it found?
        if self.sss is None:
            #QMessageBox.warning(self,"SSS2 Missing","Please connect the Smart Sensor Simulator 2 with power and USB. Ensure the SSS2 has the latest firmware.")
            #logger.debug("No SSS2 Present.")
            return False

        logger.debug(self.sss)
        self.sss.set_configuration()
        # get an endpoint instance
        self.usb_cfg = self.sss.get_active_configuration()
        self.sss_interface = self.usb_cfg[(0,0)]

        ep = usb.util.find_descriptor(
            self.sss_interface,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)
        if ep is None:
            return False
        
        self.rx_queue = queue.Queue(100000)
        self.read_usb_hid_thread = USBThread(self, self.rx_queue)
        self.read_usb_hid_thread.setDaemon(True) #needed to close the thread when the application closes.
        self.read_usb_hid_thread.start()

        sm = self.settings_model["Potentiometers"]
        # Iterate though all the bytes in the incomming message
        for group,pair,pot in zip(ALL_GROUPS,ALL_PAIRS,ALL_POTS):
            sm[group]["Pairs"][pair]["Pots"][pot]["Wiper Position"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            sm[group]["Pairs"][pair]["Pots"][pot]["Term. A Connect"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            sm[group]["Pairs"][pair]["Pots"][pot]["Wiper Connect"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            sm[group]["Pairs"][pair]["Pots"][pot]["Term. B Connect"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            sm[group]["Pairs"][pair]["Terminal A Voltage"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)

        for group in GROUP_NAMES:
            sm[group]["Terminal A Connection"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)

        sm = self.settings_model["DACs"]    
        for dac in VOUT_NAMES:
            sm[dac]["Average Voltage"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        
        self.settings_model["HVAdjOut"]["Average Voltage"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsEditable)

        sm = self.settings_model["Switches"]
        for name in SWITCH_NAMES:
            sm[name]["State"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        
        sm = self.settings_model["PWMs"]
        for name in PWM_NAMES:
            sm[name]["Duty Cycle"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            sm[name]["Frequency"].setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        
        if self.filename != "default.SSS2":
            logger.debug("Reloading {}".format(self.filename))
            self.reload()    
        
        return True
                    
    def read_usb_hid(self):  
        if self.usb_signal:
            self.statusBar().showMessage("Success - SSS2 Connected.")
            self.ignition_key_button.setEnabled(True)  
            self.can0_stream_box.setEnabled(True)
            self.can1_stream_box.setEnabled(True)
            #self.can2_stream_box.setEnabled(True)
            self.J1708_stream_box.setEnabled(True)
            self.LIN_stream_box.setEnabled(True)
            self.LIN_suppress_box.setEnabled(True)
            while self.rx_queue.qsize():
                #Get a message from the queue. These are raw bytes
                rxmessage = self.rx_queue.get()
                #logger.debug(" ".join(["{:02X}".format(b) for b in rxmessage]))
                    
                self.last_usb_message_time = time.time()
                rxmessage_type = rxmessage[USB_FRAME_TYPE_LOC] & USB_FRAME_TYPE_MASK
                if rxmessage_type == STATUS_TYPE:
                    #Status Message
                    if   rxmessage[0] & 0x0F == 1:
                        self.parse_status_message_one(rxmessage)
                    elif rxmessage[0] & 0x0F == 2:
                        self.parse_status_message_two(rxmessage)
                    elif rxmessage[0] & 0x0F == 3:
                        self.parse_status_message_three(rxmessage)
                    #self.settings_tree.model().dataChanged.connect(self.change_setting)
                elif rxmessage_type == COMMAND_TYPE:
                    pass # the SSS2 doesn't send commands to the computer
                elif rxmessage_type == MESSAGE_TYPE:
                    # Received a network message
                    self.parse_can_message(rxmessage)    
                elif rxmessage_type == CAN_THREADS_TYPE:
                    # Received a network message
                    self.fill_can_table(rxmessage)    
                elif rxmessage_type == ESCAPE_TYPE:
                    #Future stuff
                    pass
        if (time.time() - self.last_usb_message_time) > USB_MESSAGE_TIMEOUT:
            self.show_no_usb()
            self.usb_signal = self.setup_usb()

    def parse_can_message(self, rxmessage):
        message_type = rxmessage[0]
        if (message_type & 0x20) != 0x20:
            return
        num_can_messages = message_type & 0x03
        for i in range(num_can_messages):
            can_message_index = i * CAN_FRAME_LENGTH + 1
            time_buff = rxmessage[(can_message_index + TIMESTAMP_OFFSET):(can_message_index + TIMESTAMP_OFFSET + 4)]
            timestamp = struct.unpack("<L",time_buff)[0]
            channel_dlc = rxmessage[can_message_index + CHANNEL_DLC_OFFSET]
            channel = (channel_dlc & 0xF0) >> 4
            dlc = (channel_dlc & 0x0F)
            microseconds_per_second = struct.unpack("<L",rxmessage[can_message_index + MICROSECONDS_OFFSET:can_message_index + MICROSECONDS_OFFSET  + 3]+b'\x00')[0]
            canID_EXT = struct.unpack("<L",rxmessage[can_message_index + CAN_ID_OFFSET:can_message_index + CAN_ID_OFFSET + 4])[0]
            canID = canID_EXT & 0x1FFFFFFF
            extended = bool((canID_EXT & 0x80000000) >> 31)
            can_data = struct.unpack("BBBBBBBB", rxmessage[can_message_index + CAN_DATA_OFFSET:can_message_index + CAN_DATA_OFFSET + 8])
            timestamp += microseconds_per_second * 0.000001
            #can_message = "{:d} {:12.6f} {:08X} {} {:d} {}".format(channel,timestamp,canID,extended,dlc," ".join(["{:02X}".format(b) for b in can_data]))
            self.can_dict["{:08X}".format(canID)]={'channel': channel,
                                    'timestamp':'{:12.6f}'.format(timestamp),
                                    'dlc':"{:d}".format(dlc),
                                    'bytes': " ".join(["{:02X}".format(b) for b in can_data])}
            can_message="CH Timestamp CANID DLC Data\n"
            for k,v in sorted(self.can_dict.items()):
                can_message += "{} {} {} [{}] {}\n".format(v['channel'],v['timestamp'],k,v['dlc'],v['bytes'])
            self.CAN_RX_text_box.setPlainText(can_message)
            #print(can_message)

    def show_no_usb(self):
        self.statusBar().showMessage("Missing - SSS2 not detected over USB.")
        self.ignition_key_button.setCheckState(Qt.PartiallyChecked)
        self.ignition_key_button.setEnabled(False)
       
        sm = self.settings_model["Potentiometers"]
        # Iterate though all the bytes in the incomming message
        for group,pair,pot in zip(ALL_GROUPS,ALL_PAIRS,ALL_POTS):
            sm[group]["Pairs"][pair]["Pots"][pot]["Wiper Position"].setFlags(Qt.NoItemFlags)
            sm[group]["Pairs"][pair]["Pots"][pot]["Term. A Connect"].setFlags(Qt.NoItemFlags)
            sm[group]["Pairs"][pair]["Pots"][pot]["Wiper Connect"].setFlags(Qt.NoItemFlags)
            sm[group]["Pairs"][pair]["Pots"][pot]["Term. B Connect"].setFlags(Qt.NoItemFlags)
            sm[group]["Pairs"][pair]["Terminal A Voltage"].setFlags(Qt.NoItemFlags)

        for group in GROUP_NAMES:
            sm[group]["Terminal A Connection"].setFlags(Qt.NoItemFlags)

        sm = self.settings_model["DACs"]    
        for dac in VOUT_NAMES:
            sm[dac]["Average Voltage"].setFlags(Qt.NoItemFlags)
        
        self.settings_model["HVAdjOut"]["Average Voltage"].setFlags(Qt.NoItemFlags)

        sm = self.settings_model["Switches"]
        for name in SWITCH_NAMES:
            sm[name]["State"].setFlags(Qt.NoItemFlags)
        
        sm = self.settings_model["PWMs"]
        for name in PWM_NAMES:
            sm[name]["Duty Cycle"].setFlags(Qt.NoItemFlags)
            sm[name]["Frequency"].setFlags(Qt.NoItemFlags )
        
        self.can0_stream_box.setCheckState(Qt.PartiallyChecked)
        self.can0_stream_box.setEnabled(False)
        
        self.can1_stream_box.setCheckState(Qt.PartiallyChecked)
        self.can1_stream_box.setEnabled(False)
        
        # self.can2_stream_box.setCheckState(Qt.PartiallyChecked)
        # self.can2_stream_box.setEnabled(False)
        
        self.J1708_stream_box.setCheckState(Qt.PartiallyChecked) 
        self.J1708_stream_box.setEnabled(False)
        
        self.LIN_stream_box.setCheckState(Qt.PartiallyChecked) 
        self.LIN_stream_box.setEnabled(False)
        
        self.LIN_suppress_box.setCheckState(Qt.PartiallyChecked)
        self.LIN_suppress_box.setEnabled(False)
        


    def parse_status_message_one(self, rxmessage):
        """
        """
        s = self.settings_dict["Potentiometers"]
        s["Group A"]["Pairs"]["U1U2"]["Pots"]["U1"]["Wiper Position"]    = rxmessage[1]
        s["Group A"]["Pairs"]["U1U2"]["Pots"]["U2"]["Wiper Position"]    = rxmessage[2]
        s["Group A"]["Pairs"]["U3U4"]["Pots"]["U3"]["Wiper Position"]    = rxmessage[3]
        s["Group A"]["Pairs"]["U3U4"]["Pots"]["U4"]["Wiper Position"]    = rxmessage[4]
        s["Group A"]["Pairs"]["U5U6"]["Pots"]["U5"]["Wiper Position"]    = rxmessage[5]
        s["Group A"]["Pairs"]["U5U6"]["Pots"]["U6"]["Wiper Position"]    = rxmessage[6]
        s["Group A"]["Pairs"]["U7U8"]["Pots"]["U7"]["Wiper Position"]    = rxmessage[7]
        s["Group A"]["Pairs"]["U7U8"]["Pots"]["U8"]["Wiper Position"]    = rxmessage[8]
        s["Group B"]["Pairs"]["U09U10"]["Pots"]["U09"]["Wiper Position"] = rxmessage[9]
        s["Group B"]["Pairs"]["U09U10"]["Pots"]["U10"]["Wiper Position"] = rxmessage[10]
        s["Group B"]["Pairs"]["U11U12"]["Pots"]["U11"]["Wiper Position"] = rxmessage[11]
        s["Group B"]["Pairs"]["U11U12"]["Pots"]["U12"]["Wiper Position"] = rxmessage[12]
        s["Group B"]["Pairs"]["U13U14"]["Pots"]["U13"]["Wiper Position"] = rxmessage[13]
        s["Group B"]["Pairs"]["U13U14"]["Pots"]["U14"]["Wiper Position"] = rxmessage[14]
        s["Group B"]["Pairs"]["U15U16"]["Pots"]["U15"]["Wiper Position"] = rxmessage[15]
        s["Group B"]["Pairs"]["U15U16"]["Pots"]["U16"]["Wiper Position"] = rxmessage[16]
        
        sm = self.settings_model["Potentiometers"]
        sm["Group A"]["Pairs"]["U1U2"]["Pots"]["U1"]["Wiper Position"].setText("{:d}".format(rxmessage[1]))
        sm["Group A"]["Pairs"]["U1U2"]["Pots"]["U2"]["Wiper Position"].setText("{:d}".format(rxmessage[2]))
        sm["Group A"]["Pairs"]["U3U4"]["Pots"]["U3"]["Wiper Position"].setText("{:d}".format(rxmessage[3]))
        sm["Group A"]["Pairs"]["U3U4"]["Pots"]["U4"]["Wiper Position"].setText("{:d}".format(rxmessage[4]))
        sm["Group A"]["Pairs"]["U5U6"]["Pots"]["U5"]["Wiper Position"].setText("{:d}".format(rxmessage[5]))
        sm["Group A"]["Pairs"]["U5U6"]["Pots"]["U6"]["Wiper Position"].setText("{:d}".format(rxmessage[6]))
        sm["Group A"]["Pairs"]["U7U8"]["Pots"]["U7"]["Wiper Position"].setText("{:d}".format(rxmessage[7]))
        sm["Group A"]["Pairs"]["U7U8"]["Pots"]["U8"]["Wiper Position"].setText("{:d}".format(rxmessage[8]))
        sm["Group B"]["Pairs"]["U09U10"]["Pots"]["U09"]["Wiper Position"].setText("{:d}".format(rxmessage[9]))
        sm["Group B"]["Pairs"]["U09U10"]["Pots"]["U10"]["Wiper Position"].setText("{:d}".format(rxmessage[10]))
        sm["Group B"]["Pairs"]["U11U12"]["Pots"]["U11"]["Wiper Position"].setText("{:d}".format(rxmessage[11]))
        sm["Group B"]["Pairs"]["U11U12"]["Pots"]["U12"]["Wiper Position"].setText("{:d}".format(rxmessage[12]))
        sm["Group B"]["Pairs"]["U13U14"]["Pots"]["U13"]["Wiper Position"].setText("{:d}".format(rxmessage[13]))
        sm["Group B"]["Pairs"]["U13U14"]["Pots"]["U14"]["Wiper Position"].setText("{:d}".format(rxmessage[14]))
        sm["Group B"]["Pairs"]["U15U16"]["Pots"]["U15"]["Wiper Position"].setText("{:d}".format(rxmessage[15]))
        sm["Group B"]["Pairs"]["U15U16"]["Pots"]["U16"]["Wiper Position"].setText("{:d}".format(rxmessage[16]))
        
        s["Group A"]["Pairs"]["U1U2"]["Terminal A Voltage"]   = bool(rxmessage[CONFIGSWITCH_1_LOC] & U1U2P0ASWITCH_MASK)
        s["Group A"]["Pairs"]["U3U4"]["Terminal A Voltage"]   = bool(rxmessage[CONFIGSWITCH_1_LOC] & U3U4P0ASWITCH_MASK)
        s["Group A"]["Pairs"]["U5U6"]["Terminal A Voltage"]   = bool(rxmessage[CONFIGSWITCH_1_LOC] & U5U6P0ASWITCH_MASK)
        s["Group A"]["Pairs"]["U7U8"]["Terminal A Voltage"]   = bool(rxmessage[CONFIGSWITCH_1_LOC] & U7U8P0ASWITCH_MASK)
        s["Group B"]["Pairs"]["U09U10"]["Terminal A Voltage"] = bool(rxmessage[CONFIGSWITCH_1_LOC] & U9U10P0ASWITCH_MASK)
        s["Group B"]["Pairs"]["U11U12"]["Terminal A Voltage"] = bool(rxmessage[CONFIGSWITCH_1_LOC] & U11U12P0ASWITCH_MASK)
        s["Group B"]["Pairs"]["U13U14"]["Terminal A Voltage"] = bool(rxmessage[CONFIGSWITCH_1_LOC] & U13U14P0ASWITCH_MASK)
        s["Group B"]["Pairs"]["U15U16"]["Terminal A Voltage"] = bool(rxmessage[CONFIGSWITCH_1_LOC] & U15U16P0ASWITCH_MASK)

        for name, group in zip(PAIR_NAMES, GROUP_NAMES):
            state = s[group]["Pairs"][name]["Terminal A Voltage"]
            if state:
                sm[group]["Pairs"][name]["Terminal A Voltage"].setText("+12V")
                sm[group]["Pairs"][name]["Terminal A Voltage"].setCheckState(Qt.Checked)
            else:
                sm[group]["Pairs"][name]["Terminal A Voltage"].setText("+5V")
                sm[group]["Pairs"][name]["Terminal A Voltage"].setCheckState(Qt.Unchecked)
        
        s["Group A"]["Terminal A Connection"] = not (bool(rxmessage[CONFIGSWITCH_2_LOC] & U28P0AENABLE_MASK))
        s["Group B"]["Terminal A Connection"] = not (bool(rxmessage[CONFIGSWITCH_2_LOC] & U31P0AENABLE_MASK))
        for group in ["Group A", "Group B"]:
            state = s[group]["Terminal A Connection"]
            if state:
                sm[group]["Terminal A Connection"].setText("True")
                sm[group]["Terminal A Connection"].setCheckState(Qt.Checked)
            else:
                sm[group]["Terminal A Connection"].setText("Open")
                sm[group]["Terminal A Connection"].setCheckState(Qt.Unchecked)
        
        self.settings_dict["Potentiometers"]["Others"]["Pairs"]["I2CPots"]["Pots"]["U34"]["Wiper Position"] = rxmessage[U34_WIPER_LOC]
        self.settings_dict["Potentiometers"]["Others"]["Pairs"]["I2CPots"]["Pots"]["U36"]["Wiper Position"] = rxmessage[U36_WIPER_LOC]
        self.settings_dict["Potentiometers"]["Others"]["Pairs"]["I2CPots"]["Pots"]["U37"]["Wiper Position"] = rxmessage[U37_WIPER_LOC]
        self.settings_model["Potentiometers"]["Others"]["Pairs"]["I2CPots"]["Pots"]["U34"]["Wiper Position"].setText("{:d}".format(rxmessage[U34_WIPER_LOC]))
        self.settings_model["Potentiometers"]["Others"]["Pairs"]["I2CPots"]["Pots"]["U36"]["Wiper Position"].setText("{:d}".format(rxmessage[U36_WIPER_LOC]))
        self.settings_model["Potentiometers"]["Others"]["Pairs"]["I2CPots"]["Pots"]["U37"]["Wiper Position"].setText("{:d}".format(rxmessage[U37_WIPER_LOC]))


        self.settings_dict["DACs"]["Vout1"]["Average Voltage"] = struct.unpack('<H',rxmessage[17:19])[0]
        self.settings_dict["DACs"]["Vout2"]["Average Voltage"] = struct.unpack('<H',rxmessage[19:21])[0]
        self.settings_dict["DACs"]["Vout3"]["Average Voltage"] = struct.unpack('<H',rxmessage[21:23])[0]
        self.settings_dict["DACs"]["Vout4"]["Average Voltage"] = struct.unpack('<H',rxmessage[23:25])[0]
        self.settings_dict["DACs"]["Vout5"]["Average Voltage"] = struct.unpack('<H',rxmessage[25:27])[0]
        self.settings_dict["DACs"]["Vout6"]["Average Voltage"] = struct.unpack('<H',rxmessage[27:29])[0]
        self.settings_dict["DACs"]["Vout7"]["Average Voltage"] = struct.unpack('<H',rxmessage[29:31])[0]
        self.settings_dict["DACs"]["Vout8"]["Average Voltage"] = struct.unpack('<H',rxmessage[31:33])[0]
        
        for name in VOUT_NAMES:
            self.settings_model["DACs"][name]["Average Voltage"].setText(
                "{:0.2f}".format(self.settings_dict["DACs"][name]["Average Voltage"]/1000))
         
        self.settings_dict["HVAdjOut"]["Average Voltage"] =  rxmessage[HVADJOUT_LOC]
        self.settings_model["HVAdjOut"]["Average Voltage"].setText(
            "{:0.2f}".format(self.getHVOUT_voltage(rxmessage[HVADJOUT_LOC])))

        s = self.settings_dict["Switches"]
        s["Port 10 or 19"]["State"]              = bool(rxmessage[CONFIGSWITCH_2_LOC] & P10OR19SWITCH_MASK)
        s["Port 15 or 18"]["State"]              = bool(rxmessage[CONFIGSWITCH_2_LOC] & P15OR18SWITCH_MASK)
        s["CAN2 or J1708"]["State"]              = bool(rxmessage[CONFIGSWITCH_2_LOC] & J1708ORCAN1_MASK)
        s["PWMs or CAN2"]["State"]               = bool(rxmessage[CONFIGSWITCH_2_LOC] & CAN2CONNECT_MASK)
        s["CAN0 Resistor 1"]["State"]            = bool(rxmessage[PWMSWITCHES_LOC] & CAN0TERM1_MASK)
        s["CAN1 Resistor 1"]["State"]            = bool(rxmessage[PWMSWITCHES_LOC] & CAN1TERM1_MASK)
        s["CAN2 Resistor 1"]["State"]            = bool(rxmessage[PWMSWITCHES_LOC] & CAN2TERM1_MASK)
        s["LIN Master Pullup Resistor"]["State"] = bool(rxmessage[PWMSWITCHES_LOC] & LIN_PULLUP_MASK)
        s["PWM3 or 12V"]["State"]                = bool(rxmessage[HBRIDGE_LOC] & TWELVE_OUT_1_MASK)
        s["12V Out 2"]["State"]                  = bool(rxmessage[HBRIDGE_LOC] & TWELVE_OUT_2_MASK)
        s["PWM4 or Ground"]["State"]             = bool(rxmessage[HBRIDGE_LOC] & GROUND_OUT_1_MASK)
        s["Ground Out 2"]["State"]               = bool(rxmessage[HBRIDGE_LOC] & GROUND_OUT_2_MASK)
        s["PWM1 Connect"]["State"]               = bool(rxmessage[PWMSWITCHES_LOC] & PWM1_CONNECT_MASK)
        s["PWM2 Connect"]["State"]               = bool(rxmessage[PWMSWITCHES_LOC] & PWM2_CONNECT_MASK)
        s["PWM3 Connect"]["State"]               = bool(rxmessage[PWMSWITCHES_LOC] & PWM3_CONNECT_MASK)
        s["PWM4 Connect"]["State"]               = bool(rxmessage[PWMSWITCHES_LOC] & PWM4_CONNECT_MASK)
        s["LIN to SHLD"]["State"]                = bool(rxmessage[CONFIGSWITCH_2_LOC] & LINTOSHIELD_MASK)
        s["LIN to Port 16"]["State"]             = bool(rxmessage[CONFIGSWITCH_2_LOC] & LINTO16_MASK)
        s["Ignition"]["State"]                   = bool(rxmessage[HBRIDGE_LOC] & IGNITION_RELAY_MASK)

        sm = self.settings_model["Switches"]
        for name in SWITCH_NAMES:
            sm[name]["State"].setText("{}".format(s[name]["State"]))
            if s[name]["State"]:
                sm[name]["State"].setCheckState(Qt.Checked)
            else:
                sm[name]["State"].setCheckState(Qt.Unchecked)

        # Parse the incoming message for PWM signal related information
        self.settings_dict["PWMs"]["PWM1"]["Duty Cycle"] = struct.unpack('<H',rxmessage[35:37])[0]
        self.settings_dict["PWMs"]["PWM2"]["Duty Cycle"] = struct.unpack('<H',rxmessage[37:39])[0]
        self.settings_dict["PWMs"]["PWM3"]["Duty Cycle"] = struct.unpack('<H',rxmessage[39:41])[0]
        self.settings_dict["PWMs"]["PWM4"]["Duty Cycle"] = struct.unpack('<H',rxmessage[41:43])[0]
        self.settings_dict["PWMs"]["PWM5"]["Duty Cycle"] = struct.unpack('<H',rxmessage[43:45])[0]
        self.settings_dict["PWMs"]["PWM6"]["Duty Cycle"] = struct.unpack('<H',rxmessage[45:47])[0]

        self.settings_dict["PWMs"]["PWM1"]["Frequency"] = struct.unpack('<H',rxmessage[54:56])[0]
        self.settings_dict["PWMs"]["PWM2"]["Frequency"] = struct.unpack('<H',rxmessage[54:56])[0]
        self.settings_dict["PWMs"]["PWM3"]["Frequency"] = struct.unpack('<H',rxmessage[56:58])[0]
        self.settings_dict["PWMs"]["PWM4"]["Frequency"] = struct.unpack('<H',rxmessage[56:58])[0]
        self.settings_dict["PWMs"]["PWM5"]["Frequency"] = struct.unpack('<H',rxmessage[58:60])[0]
        self.settings_dict["PWMs"]["PWM6"]["Frequency"] = struct.unpack('<H',rxmessage[58:60])[0]

        # Set the display model in the tree.
        for name in PWM_NAMES:
            self.settings_model["PWMs"][name]["Duty Cycle"].setText(
                "{:0.2f}%".format(self.settings_dict["PWMs"][name]["Duty Cycle"]/4096*100))
            self.settings_model["PWMs"][name]["Frequency"].setText(
                "{:d}".format(self.settings_dict["PWMs"][name]["Frequency"]))   

        # Check the ignition state
        self.settings_dict["Switches"]
        if self.settings_dict["Switches"]["Ignition"]["State"]:
            self.ignition_key_button.setCheckState(Qt.Checked)
        else:
            self.ignition_key_button.setCheckState(Qt.Unchecked)

        s = self.settings_dict["Switches"]
        s["PWM4_28 Connect"]["State"]            = bool(rxmessage[TERMSWITCHES_LOC] & PWM4_P28_MASK)
        s["PWM5 Connect"]["State"]               = bool(rxmessage[TERMSWITCHES_LOC] & PWM5_CONNECT_MASK)
        s["PWM6 Connect"]["State"]               = bool(rxmessage[TERMSWITCHES_LOC] & PWM6_CONNECT_MASK)
        s["CAN1 Connect"]["State"]               = bool(rxmessage[TERMSWITCHES_LOC] & CAN1_CONNECT_MASK)
        s["CAN0 Resistor 2"]["State"]            = bool(rxmessage[TERMSWITCHES_LOC] & CAN0TERM2_MASK)
        s["CAN2 Resistor 2"]["State"]            = bool(rxmessage[TERMSWITCHES_LOC] & CAN2TERM2_MASK)
        s["CAN1 Resistor 2"]["State"]            = bool(rxmessage[TERMSWITCHES_LOC] & CAN1TERM2_MASK)
        
    def getHVOUT_voltage(self, reading):
        return reading*0.049441804 + 1.94

    def setHVOUT_voltage(self, voltage):
        return "{:d}".format(int((float(voltage)-1.94)*20.22579915))
        
    def parse_status_message_two(self, rxmessage):
        s  = self.settings_dict["Potentiometers"]
        sm = self.settings_model["Potentiometers"]
        # Iterate though all the bytes in the incomming message
        for i,group,pair,pot in zip(range(1,20),ALL_GROUPS,ALL_PAIRS,ALL_POTS):
           
            state = bool(rxmessage[i] & WIPER_TCON_MASK)
            s[group]["Pairs"][pair]["Pots"][pot]["Wiper Connect"]   = state
            if state:
                sm[group]["Pairs"][pair]["Pots"][pot]["Wiper Connect"].setText("True")
                sm[group]["Pairs"][pair]["Pots"][pot]["Wiper Connect"].setCheckState(Qt.Checked)
            else:
                sm[group]["Pairs"][pair]["Pots"][pot]["Wiper Connect"].setText("Open")
                sm[group]["Pairs"][pair]["Pots"][pot]["Wiper Connect"].setCheckState(Qt.Unchecked)
            
            state = bool(rxmessage[i] & TERMA_TCON_MASK)
            s[group]["Pairs"][pair]["Pots"][pot]["Term. A Connect"] 
            if state:
                sm[group]["Pairs"][pair]["Pots"][pot]["Term. A Connect"].setText("True")
                sm[group]["Pairs"][pair]["Pots"][pot]["Term. A Connect"].setCheckState(Qt.Checked)
            else:
                sm[group]["Pairs"][pair]["Pots"][pot]["Term. A Connect"].setText("Open")
                sm[group]["Pairs"][pair]["Pots"][pot]["Term. A Connect"].setCheckState(Qt.Unchecked)

            state = bool(rxmessage[i] & TERMB_TCON_MASK)
            s[group]["Pairs"][pair]["Pots"][pot]["Term. B Connect"] = state
            if state:
                sm[group]["Pairs"][pair]["Pots"][pot]["Term. B Connect"].setText("True")
                sm[group]["Pairs"][pair]["Pots"][pot]["Term. B Connect"].setCheckState(Qt.Checked)
            else:
                sm[group]["Pairs"][pair]["Pots"][pot]["Term. B Connect"].setText("Open")
                sm[group]["Pairs"][pair]["Pots"][pot]["Term. B Connect"].setCheckState(Qt.Unchecked)

       
        self.status_message_2 = rxmessage

        if (bool(rxmessage[NET_STATUS_LOC] & STREAM_CAN0_MASK)):
            self.can0_stream_box.setCheckState(Qt.Checked)
        else:
            self.can0_stream_box.setCheckState(Qt.Unchecked)

        if (bool(rxmessage[NET_STATUS_LOC] & STREAM_CAN1_MASK)):
            self.can1_stream_box.setCheckState(Qt.Checked)
        else:
            self.can1_stream_box.setCheckState(Qt.Unchecked)

        # if (bool(rxmessage[NET_STATUS_LOC] & STREAM_CAN2_MASK)):
        #     self.can2_stream_box.setCheckState(Qt.Checked)
        # else:
        #     self.can2_stream_box.setCheckState(Qt.Unchecked)

        if (bool(rxmessage[NET_STATUS_LOC] & STREAM_J1708_MASK)):
            self.J1708_stream_box.setCheckState(Qt.Checked)
        else:
            self.J1708_stream_box.setCheckState(Qt.Unchecked)

        if (bool(rxmessage[NET_STATUS_LOC] & SEND_LIN_MASK)):
            self.LIN_stream_box.setCheckState(Qt.Checked)
        else:
            self.LIN_stream_box.setCheckState(Qt.Unchecked)

        if (bool(rxmessage[NET_STATUS_LOC] & SUPPRESS_LIN_MASK )):
            self.LIN_suppress_box.setCheckState(Qt.Checked)
        else:
            self.LIN_suppress_box.setCheckState(Qt.Unchecked)

        self.can0_baud = CAN_SPEEDS[rxmessage[CAN0_BAUD_LOC]]
        baud_string = "{}".format(self.can0_baud)
        baud_index = self.can0_baud_box.findText(baud_string)
        self.can0_baud_box.setCurrentIndex(baud_index)

        self.can1_baud = CAN_SPEEDS[rxmessage[CAN1_BAUD_LOC]]
        baud_string = "{}".format(self.can1_baud)
        baud_index = self.can1_baud_box.findText(baud_string)
        self.can1_baud_box.setCurrentIndex(baud_index)
        
        self.can2_baud = CAN_SPEEDS[rxmessage[CAN2_BAUD_LOC]]
        baud_string = "{}".format(self.can2_baud)
        baud_index = self.can2_baud_box.findText(baud_string)
        self.can2_baud_box.setCurrentIndex(baud_index)

        self.can0_rx_count.setText("{}".format(struct.unpack("<L",
            rxmessage[CAN0_RX_COUNT_LOC:CAN0_RX_COUNT_LOC+4])[0]))

        self.can1_rx_count.setText("{}".format(struct.unpack("<L",
            rxmessage[CAN1_RX_COUNT_LOC:CAN1_RX_COUNT_LOC+4])[0]))

        self.can2_rx_count.setText("{}".format(struct.unpack("<L",
            rxmessage[CAN2_RX_COUNT_LOC:CAN2_RX_COUNT_LOC+4])[0]))

        self.can0_tx_count.setText("{}".format(struct.unpack("<L",
            rxmessage[CAN0_TX_COUNT_LOC:CAN0_TX_COUNT_LOC+4])[0]))

        self.can1_tx_count.setText("{}".format(struct.unpack("<L",
            rxmessage[CAN1_TX_COUNT_LOC:CAN1_TX_COUNT_LOC+4])[0]))

        self.can2_tx_count.setText("{}".format(struct.unpack("<L",
            rxmessage[CAN2_TX_COUNT_LOC:CAN2_TX_COUNT_LOC+4])[0]))

        self.j1708_rx_count.setText("{}".format(struct.unpack("<H",
            rxmessage[J1708_RX_COUNT_LOC:J1708_RX_COUNT_LOC+2])[0]))

        self.lin_rx_count.setText("{}".format(struct.unpack("<H",
            rxmessage[LIN_RX_COUNT_LOC:LIN_RX_COUNT_LOC+2])[0]))

        self.lin_tx_count.setText("{}".format(struct.unpack("<H",
            rxmessage[LIN_TX_COUNT_LOC:LIN_TX_COUNT_LOC+2])[0]))


    def parse_status_message_three(self, rxmessage):
        pass

    def clicked_setting(self, index):
        parent = index.parent()
        model = parent.model()
        try:
            if model.itemFromIndex(index).isCheckable():
                setting_index = index.siblingAtColumn(2)
                setting_number = int(model.itemFromIndex(setting_index).text())
                #logger.debug("Checkable Setting Index: {}".format(setting_number))
                if model.itemFromIndex(index).checkState() == Qt.Checked:
                   setting_value = 1
                else:
                   setting_value = 0
                #logger.debug("Setting Value: {}".format(setting_value))
                if (setting_number >= 51 and setting_number <= 66) or (setting_number >= 78 and setting_number <= 80):
                    description_index = index.siblingAtColumn(1)
                    description = model.itemFromIndex(description_index).text()
                    logger.debug(description)
                    if (setting_number >= 51 and setting_number <= 66):
                        current_value = (self.status_message_2[setting_number-50])
                    else:
                        current_value = (self.status_message_2[setting_number-61])
                    if "A" in description:
                        value = TERMA_TCON_MASK
                    elif "W" in description:
                        value = WIPER_TCON_MASK
                    else:
                        value = TERMB_TCON_MASK

                    if setting_value == 1:
                        current_value |=  value
                    else:
                        current_value &=  ~value
                    setting_value = current_value
                elif setting_number == 73 or setting_number == 74:
                    setting_value = not setting_value
                command_string = "{:d},{:d}".format(setting_number,setting_value)
                self.send_command(command_string) 
        except AttributeError:
            #Do nothing if there is no itemFromIndex
            pass
        except:
            logger.debug(traceback.format_exc())
        self.edit_settings = False

    def change_setting(self, item):
        
        if self.edit_settings or self.load_settings:
            # See if an item was passed in, or is it an index.
            try:
                index = item.index()
            except:
                index = item
            # The parent is the row index
            parent = index.parent()
            # the model has the data in the row
            model = parent.model()
            try:
                setting_index = index.siblingAtColumn(2)
                setting_number = int(model.itemFromIndex(setting_index).text())
                if setting_number > 16 and setting_number < 25: #Voltage out
                    setting_value = int(float(model.itemFromIndex(index).text())*1000)  
                elif setting_number == 49:
                    setting_value = int(self.setHVOUT_voltage(model.itemFromIndex(index).text()))
                elif (setting_number >= 33 and setting_number <= 36) or (setting_number >= 87 and setting_number <= 88):
                    setting_value = int(float(model.itemFromIndex(index).text())/100*4096)
                else:
                    setting_value = int(model.itemFromIndex(index).text())
                #logger.debug("Setting Value: {}".format(setting_value))
                command_string = "{:d},{:d}".format(setting_number,setting_value)
                self.send_command(command_string)            
            except (AttributeError,TypeError):
                #Some of the items do not have siblings.
                logger.debug(traceback.format_exc())
            except (ValueError):
                #Clicking on a thing that doesn't have a check box
                logger.debug(traceback.format_exc())
            
            # The edit_settings flag is to ensure the user is the one editing the settings
            # Setting this flag is done with a mouse click. With out this check, the SSS2 can
            # call this function and it goes into a loop.
            self.edit_settings = False
         
    
    def fill_tree(self):
        
        for key0,item0 in self.settings_dict.items():
            if "CAN" not in key0:
                thing = QStandardItem(key0)
                thing.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
            else:
                continue
            if not isinstance(item0, dict):
                continue

            self.settings_model[key0]={}
            if key0 == "HVAdjOut":
                vout = QStandardItem(key0)
                vout_label = QStandardItem("Voltage for pins J24:19 and J18:11")
                vout_setting = QStandardItem("{:2d}".format(item0["SSS2 setting"]))
                vout_value = QStandardItem("{}".format(item0["Average Voltage"]))  
                
                vout.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                vout_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                vout_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                vout_value.setFlags(Qt.NoItemFlags)
                
                self.settings_model[key0]["Average Voltage"]=vout_value
                thing.appendRow([vout,vout_label,vout_setting,vout_value])
                
            for key1, item1 in item0.items():
                if not isinstance(item1, dict):
                    continue 
                self.settings_model[key0][key1]={}
                if key0 == "Potentiometers":
                    group = QStandardItem(key1)
                    group_label = QStandardItem("All Terminal A's are connected to voltage for {}.".format(item1["Label"]))
                    try:
                        group_setting = QStandardItem("{:2d}".format(item1["SSS2 Setting"]))
                    except TypeError:
                        group_setting = QStandardItem("")
                    if "Others" == key1:
                        group_value = QStandardItem("")
                    else:
                        group_value = QStandardItem(str(item1["Terminal A Connection"]))
                        group_value.setCheckable(True)
                
                    group.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    group_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    group_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    group_value.setFlags(Qt.NoItemFlags)  
                    self.settings_model[key0][key1]["Terminal A Connection"] = group_value

                    group.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    group_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    group_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    self.settings_model[key0][key1]["Pairs"] = {}
                    for p,pots in item1["Pairs"].items():
                        self.settings_model[key0][key1]["Pairs"][p]={}
                        pair = QStandardItem(p)
                        if "I2CPots" not in p:
                            pair_value = QStandardItem("{}".format(pots["Terminal A Voltage"]))
                            pair_value.setCheckable(True)
                        else:
                            pair_value = QStandardItem("")
                        self.settings_model[key0][key1]["Pairs"][p]["Terminal A Voltage"] = pair_value
                        try:
                            pair_setting = QStandardItem("{:2d}".format(pots["SSS Setting"]))
                        except TypeError:
                            pair_setting = QStandardItem("")
                        pair_label = QStandardItem(pots["Name"])
                        pair.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                        pair_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                        pair_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                        pair_value.setFlags(Qt.NoItemFlags)

                        self.settings_model[key0][key1]["Pairs"][p]["Pots"]={}
                        for pot_key,vals in pots["Pots"].items():
                            self.settings_model[key0][key1]["Pairs"][p]["Pots"][pot_key]={}
                            pot =  QStandardItem(pot_key)
                            pot_setting = QStandardItem("{:2d}".format(vals["SSS2 Wiper Setting"]))
                            pot_value = QStandardItem(str(vals["Wiper Position"]))
                            pot_label = QStandardItem(vals["Name"] + " ({}) Wiper Position ({})".format(vals["Resistance"],vals["Pin"]))
                            pot.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            pot_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            pot_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            pot_value.setFlags(Qt.NoItemFlags)
                            
                            terminalA = QStandardItem("")
                            terminalA_label = QStandardItem("Connect Terminal A")
                            terminalA_setting = QStandardItem("{:2d}".format(vals["SSS2 TCON Setting"]))
                            terminalA_value = QStandardItem("{}".format(vals["Term. A Connect"]))
                            
                            wiper = QStandardItem("")
                            wiper_label = QStandardItem("Connect Potentiometer Wiper")
                            wiper_setting = QStandardItem("{:2d}".format(vals["SSS2 TCON Setting"]))
                            wiper_value = QStandardItem("{}".format(vals["Wiper Connect"]))
                            
                            terminalB = QStandardItem("")
                            terminalB_label = QStandardItem("Connect Terminal B")
                            terminalB_setting = QStandardItem("{:2d}".format(vals["SSS2 TCON Setting"]))
                            terminalB_value = QStandardItem("{}".format(vals["Term. B Connect"]))
                            
                            terminalA.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            terminalA_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            terminalA_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            terminalA_value.setFlags(Qt.NoItemFlags)
                            terminalA_value.setCheckable(True)

                            wiper.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            wiper_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            wiper_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            wiper_value.setFlags(Qt.NoItemFlags)
                            wiper_value.setCheckable(True)
                            
                            terminalB.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            terminalB_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            terminalB_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                            terminalB_value.setFlags(Qt.NoItemFlags)
                            terminalB_value.setCheckable(True)
                            
                            pot.appendRow([terminalA, terminalA_label, terminalA_setting, terminalA_value])
                            pot.appendRow([wiper, wiper_label, wiper_setting, wiper_value])
                            pot.appendRow([terminalB, terminalB_label, terminalB_setting, terminalB_value])
                            self.settings_model[key0][key1]["Pairs"][p]["Pots"][pot_key]["Wiper Position"] = pot_value
                            self.settings_model[key0][key1]["Pairs"][p]["Pots"][pot_key]["Term. A Connect"] = terminalA_value
                            self.settings_model[key0][key1]["Pairs"][p]["Pots"][pot_key]["Wiper Connect"] = wiper_value
                            self.settings_model[key0][key1]["Pairs"][p]["Pots"][pot_key]["Term. B Connect"] = terminalB_value
                            pair.appendRow([pot,pot_label,pot_setting,pot_value])
                            
                        group.appendRow([pair,pair_label,pair_setting,pair_value])
                    thing.appendRow([group,group_label,group_setting,group_value])        
                elif key0 == "DACs":
                        vout = QStandardItem(key1)
                        vout_label = QStandardItem("Voltage for {} ({})".format(item1["Name"],item1["Pin"]))
                        vout_setting = QStandardItem("{:2d}".format(item1["SSS2 setting"]))
                        vout_value = QStandardItem("{}".format(item1["Average Voltage"]))  
                        
                        vout.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                        vout_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                        vout_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                        vout_value.setFlags(Qt.NoItemFlags)
                        
                        self.settings_model[key0][key1] = {}
                        self.settings_model[key0][key1]["Average Voltage"]=vout_value
                        thing.appendRow([vout,vout_label,vout_setting,vout_value])                                   
                elif key0 == "PWMs":
                    pwm = QStandardItem(key1)
                    pwm_label = QStandardItem("Pulse Width Modulated Signal {} Duty Cycle ({})".format(item1["Name"],item1["Pin"]))
                    pwm_setting = QStandardItem("{:2d}".format(item1["SSS2 setting"]))
                    pwm_value = QStandardItem("{}".format(item1["Duty Cycle"]))
                    pwm.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    pwm_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    pwm_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    pwm_value.setFlags(Qt.NoItemFlags)
                    
                    freq = QStandardItem("Freq.")
                    freq_label = QStandardItem("Frequency of PWM Signal (Hz)")
                    freq_setting = QStandardItem("{:2d}".format(item1["SSS2 freq setting"]))
                    freq_value = QStandardItem("{:d}".format(item1["Frequency"]))
                    
                    freq.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    freq_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    freq_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    freq_value.setFlags(Qt.NoItemFlags)

                    self.settings_model[key0][key1] = {}
                    self.settings_model[key0][key1]["Duty Cycle"]=pwm_value
                    self.settings_model[key0][key1]["Frequency"]=freq_value
                    thing.appendRow([pwm,pwm_label,pwm_setting,pwm_value])
                    pwm.appendRow([freq,freq_label,freq_setting,freq_value])
                    

                elif key0 == "Switches":
                    switch = QStandardItem(key1)
                    try:
                        switch_label = QStandardItem("{}".format(item1["Label"]))
                    except KeyError:
                        switch_label = QStandardItem("{} (True) or {} (False)".format(item1["Label A"], item1["Label B"]))
                    switch_setting = QStandardItem("{:2d}".format(item1["SSS2 setting"]))
                    switch_value = QStandardItem("{}".format(item1["State"]))
                    switch.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    switch_label.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    switch_setting.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
                    switch_value.setCheckable(True)
                    switch_value.setFlags(Qt.NoItemFlags)
                    self.settings_model[key0][key1] = {}
                    self.settings_model[key0][key1]["State"] = switch_value
                    
                    thing.appendRow([switch,switch_label,switch_setting,switch_value])
            
            self.settings_tree.model().appendRow(thing)

        self.settings_tree.expandAll()
    
    def enable_edit(self):
        self.edit_settings = True
    
    def load_file(self):
        
        filters = "Smart Sensor Simulator Settings Files (*.SSS2);;All Files (*.*)"
        selected_filter = "Smart Sensor Simulator Settings Files (*.SSS2)"
        fname = QFileDialog.getOpenFileName(self, 
                                            'Open File',
                                            self.export_path,
                                            filters,
                                            selected_filter)
        if fname[0]:
            self.export_path, self.filename = os.path.split(fname[0])
            self.setWindowTitle('{} {} - {}'.format(release_title,
                                                        release_version,
                                                        self.filename))
            self.reload(fname[0])

    def reload(self, filename=False):
        logger.debug("Trying to load {}".format(filename))
        if not filename:
            filename = os.path.join(self.export_path, self.filename)
        
        if not self.usb_signal:
            QMessageBox.warning(self,"Connection Needed",
                "Smart Sensor Simulator 2 must be connectected and communicating for settings to be loaded.")
            return False


        try:
            with open(filename,'r') as fp:
                new_settings = json.load(fp)
        except:
            message =traceback.format_exc()
            logger.debug(message)
            QMessageBox.warning(self,"Not a valid file","There was an issue opening the file.\n{}".format(message))
            return False
        
        digest = calculate_sha256(filename)
        logger.info("Opened {} with the following SHA256 digest:\n{}".format(self.filename,digest))
        
        for k,v in self.settings_dict.items():
            try:                    
                self.settings_dict[k].update(new_settings[k])
            except AttributeError:
                self.settings_dict[k] = new_settings[k]
            except KeyError:
                pass
        
        command_string = "" 
        s = self.settings_dict["DACs"]    
        for dac in VOUT_NAMES:
            setting_number = s[dac]["SSS2 setting"] #Watch capitalization. 
            setting_value  = int(float(s[dac]["Average Voltage"])*1000)
            command_string += "{:d},{:d},".format(setting_number, setting_value)
            if len(command_string) > MAX_COMMAND_STRING_LENGTH:
                self.send_command(command_string)
                command_string = ""    
        self.send_command(command_string)  # Send combined commands  command_string = "" 
        
        command_string = "" 
        
        s = self.settings_dict["Potentiometers"]
        for group,pair,pot in zip(ALL_GROUPS,ALL_PAIRS,ALL_POTS):
            setting_number = s[group]["Pairs"][pair]["Pots"][pot]["SSS2 Wiper Setting"]
            setting_value = s[group]["Pairs"][pair]["Pots"][pot]["Wiper Position"]
            tcon_setting_number = s[group]["Pairs"][pair]["Pots"][pot]["SSS2 TCON Setting"]
            tcon_setting_value = (WIPER_TCON_MASK * int(s[group]["Pairs"][pair]["Pots"][pot]["Wiper Connect"])
                                + TERMB_TCON_MASK * int(s[group]["Pairs"][pair]["Pots"][pot]["Term. B Connect"])
                                + TERMA_TCON_MASK * int(s[group]["Pairs"][pair]["Pots"][pot]["Term. A Connect"])
                                )
            command_string = "{:d},{:d},{:d},{:d},".format(setting_number, 
                                                           setting_value,
                                                           tcon_setting_number,
                                                           tcon_setting_value)
            self.send_command(command_string)
            
        command_string = ""    
        for group in set(GROUP_NAMES): # Use a set since GROUP_NAMES contains duplicates
            setting_number = s[group]["SSS2 Setting"]
            setting_value = int(s[group]["Terminal A Connection"])
            command_string += "{:d},{:d},".format(setting_number, setting_value)
        self.send_command(command_string)  # Send combined commands   
        
        
        
        command_string = "" 
        setting_number = self.settings_dict["HVAdjOut"]["SSS2 setting"]
        setting_value  = self.setHVOUT_voltage(self.settings_dict["HVAdjOut"]["Average Voltage"])
        command_string += "{:d},{},".format(setting_number, setting_value)
        self.send_command(command_string) 

        command_string = "" 
        s = self.settings_dict["Switches"]
        for name in SWITCH_NAMES:
            setting_number = s[name]["SSS2 setting"] #Watch capitalization. 
            setting_value  = int((s[name]["State"]))
            command_string += "{:d},{:d},".format(setting_number, setting_value)
            if len(command_string) > MAX_COMMAND_STRING_LENGTH:
                self.send_command(command_string)
                command_string = ""    
        self.send_command(command_string)  # Send combined commands  
        
        command_string = "" 
        s = self.settings_dict["PWMs"]
        for name in PWM_NAMES:
            setting_number = s[name]["SSS2 setting"] #Watch capitalization. 
            setting_value  = int((s[name]["Duty Cycle"])*4096/100)
            command_string += "{:d},{:d},".format(setting_number, setting_value)
            setting_number = s[name]["SSS2 freq setting"] #Watch capitalization. 
            setting_value  = int((s[name]["Frequency"]))
            command_string += "{:d},{:d},".format(setting_number, setting_value)
            self.send_command(command_string)
            command_string = ""    
        #self.send_command("LS")
        return True

    def save_file(self):
        filters = "Smart Sensor Simulator Settings Files (*.SSS2);;All Files (*.*)"
        selected_filter = "Smart Sensor Simulator Settings Files (*.SSS2)"
        fname = QFileDialog.getSaveFileName(self, 
                                            'Save File As',
                                            os.path.join(self.export_path,self.filename),
                                            filters,
                                            selected_filter)
        if fname[0]:
            if fname[0][-5:] ==".SSS2":
                self.filename = fname[0]
            else:
                self.filename = fname[0]+".SSS2"
            
            self.settings_dict["SSS2 Interface Release Date"] = release_date
            self.settings_dict["SSS2 Interface Version"] = release_version
             
            with open(self.filename,'w') as outfile:
                json.dump(self.settings_dict,outfile,indent=4,sort_keys=True)
            
            digest = calculate_sha256(self.filename)
            logger.info("Saved {} with the following SHA256 digest:\n{}".format(self.filename,digest))
            with open(self.filename+".SHA256",'w') as outfile:
                outfile.write(digest)
            self.export_path, self.filename = os.path.split(fname[0])
            self.setWindowTitle('{} {} - {}'.format(release_title,
                                                    release_version,
                                                    self.filename))
    
    def build_can_generator_tab(self):
        # Setup the Model Viewer and Controller for the table for th CAN generator status messages
        self.can_table = QTableView()
        self.can_data_model = CANTableModel()
        self.can_table_proxy = Proxy()
        self.can_data_model.setDataDict(self.can_generator_dict)
        self.can_table_columns = ["Thread","Count","Index","Send","Channel","Period",
                                    "Restart","Total","TX Count","CAN HEX ID","DLC",
                                    "B1","B2","B3","B4","B5","B6","B7","B8","Label"]
        self.can_data_model.setDataHeader(self.can_table_columns)
        self.can_table_proxy.setSourceModel(self.can_data_model)
        self.can_table.setModel(self.can_table_proxy)
        self.can_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.can_table.setSortingEnabled(True)
        self.can_table.setWordWrap(False)
        self.can_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.can_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.can_table.setAlternatingRowColors(True)
        self.can_tab_layout.addWidget(self.can_table,0,0,1,3)
        
        # self.add_row_button = QPushButton("Add Row to Table", self)
        # self.add_row_button.clicked.connect(self.add_can_table_row)
        # self.can_tab_layout.addWidget(self.add_row_button,1,1,1,1)

        clear_button = QPushButton("Clear Table")
        clear_button.clicked.connect(self.clear_can_table)
        self.can_tab_layout.addWidget(clear_button,1,2,1,1)
    
    def clear_can_table(self):
        self.can_generator_dict = {}
        self.can_data_model.aboutToUpdate()
        self.can_data_model.setDataDict(self.can_generator_dict)
        self.can_data_model.signalUpdate()
        self.can_table.resizeRowsToContents()     
        self.can_table.scrollToBottom()
        self.can_table.resizeColumnsToContents()

    
    # def add_can_table_row(self):
    #     current_row = self.can_table.currentRow()
    #     if current_row < 0:
    #         current_row = self.can_table.rowCount()
    #     self.can_table.insertRow(current_row)

    def fill_can_table(self,rxmessage):
        """ Arduino code generating message
          status_buffer_4[1] = can_messages[buffer4_index]->channel;
          memcpy(&status_buffer_4[2],&buffer4_index,2);
          memcpy(&status_buffer_4[4],&buffer4_message_index,2);
          status_buffer_4[6] = can_messages[buffer4_index]->txmsg.len;
          memcpy(&status_buffer_4[7],&can_messages[buffer4_index]->tx_period,4);
          memcpy(&status_buffer_4[11],&can_messages[buffer4_index]->loop_cycles,4);
          status_buffer_4[15] = can_messages[buffer4_index]->num_messages;
          memcpy(&status_buffer_4[16],&can_messages[buffer4_index]->stop_after_count,4);
          memcpy(&status_buffer_4[20],&can_messages[buffer4_index]->id_list[buffer4_message_index],4);   
          memcpy(&status_buffer_4[24],&can_messages[buffer4_index]->message_list[buffer4_message_index],8);   
          status_buffer_4[32] = can_messages[buffer4_index]->ok_to_send;
          memcpy(&status_buffer_4[33],&can_messages[buffer4_index]->transmit_number,4);   
          memset(&status_buffer_4[37],0x00,24); //Clear string
          memcpy(&status_buffer_4[37],&can_messages[buffer4_index]->ThreadName[0],24);   
          buffer4_message_index++;
          if (buffer4_message_index >= can_messages[buffer4_index]->num_messages ) {
            buffer4_message_index = 0;
            buffer4_index++;
            if (buffer4_index > can_thread_controller.size(false)) buffer4_index = 0; 
          }
        """
        needs_updating = False
        entry = struct.unpack(">L",rxmessage[2:6])[0]
        print(entry) 
        if entry not in self.can_generator_dict:
            self.can_generator_dict[entry] = {'previous':[None for i in rxmessage]}
               
        #    return
        # else:
        #     if ( self.can_generator_dict[entry]['previous'][6:33] == rxmessage[6:33] and
        #            self.can_generator_dict[entry]['previous'][37:61] == rxmessage[37:61]):
        #         needs_updating = False
        #     else:
        #         needs_updating = True
                
        row = list(self.can_generator_dict.keys()).index(entry)
        
        if self.can_generator_dict[entry]['previous'][33:37] != rxmessage[33:37]:
            col = self.can_table_columns.index("TX Count")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["TX Count"] = "{:10d}".format(struct.unpack("<L",rxmessage[33:37])[0])
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["TX Count"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][1] != rxmessage[1]:
            col = self.can_table_columns.index("Channel")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["Channel"] = rxmessage[1]
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["Channel"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][2:4] != rxmessage[2:4]:
            col = self.can_table_columns.index("Thread")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["Thread"] = "{:4d}".format(struct.unpack("<H",rxmessage[2:4])[0])
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["Thread"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][4:6] != rxmessage[4:6]:
            col = self.can_table_columns.index("Index")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["Index"] = "{:4d}".format(struct.unpack("<H",rxmessage[4:6])[0])
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["Index"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][6] != rxmessage[6]:
            col = self.can_table_columns.index("DLC")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["DLC"] = rxmessage[6]
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["DLC"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][32] != rxmessage[32]:
            send = rxmessage[32]
            col = self.can_table_columns.index("Send")
            idx = self.can_data_model.index(row, col)
            if send == 0:
                self.can_generator_dict[entry]["Send"] = "No"
            else:
                self.can_generator_dict[entry]["Send"] = "Yes"
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["Send"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][7:11] != rxmessage[7:11]:
            col = self.can_table_columns.index("Period")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["Period"] = "{:6d}".format(struct.unpack("<L",rxmessage[7:11])[0])
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["Period"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][11:15] != rxmessage[11:15]:
            col = self.can_table_columns.index("Restart")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["Restart"] = "{:6d}".format(struct.unpack("<L",rxmessage[11:15])[0])
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["Restart"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][15] != rxmessage[15]:
            col = self.can_table_columns.index("Count")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["Count"] =  rxmessage[15]
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["Count"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][16:20] != rxmessage[16:20]:
            col = self.can_table_columns.index("Total")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["Total"] = struct.unpack("<L",rxmessage[16:20])[0]
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["Total"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][20:24] != rxmessage[20:24]:
            can_id = struct.unpack("<L",rxmessage[20:24])[0]
            col = self.can_table_columns.index("CAN HEX ID")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["CAN HEX ID"] = "{:08X}".format(can_id)
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["CAN HEX ID"])
            needs_updating = True
        
        if self.can_generator_dict[entry]['previous'][24:32] != rxmessage[24:32]:
            data_bytes = struct.unpack("BBBBBBBB",rxmessage[24:32])
            col = self.can_table_columns.index("B1")
            for b,c,d in zip(data_bytes,range(col,col+8),range(8)):
                idx = self.can_data_model.index(row, c)
                self.can_generator_dict[entry]["B{}".format(d+1)] = "{:02X}".format(b)
                self.can_data_model.setData(idx, self.can_generator_dict[entry]["B{}".format(d+1)])
            needs_updating = True

        if self.can_generator_dict[entry]['previous'][37:61] != rxmessage[37:61]:
            name = rxmessage[37:61].decode('ascii','ignore')
            col = self.can_table_columns.index("Label")
            idx = self.can_data_model.index(row, col)
            self.can_generator_dict[entry]["Label"] = "{}".format(name)
            self.can_data_model.setData(idx, self.can_generator_dict[entry]["Label"])
            needs_updating = True

        self.can_generator_dict[entry]['previous'] = rxmessage
        
        if needs_updating:
            self.can_data_model.aboutToUpdate()
            self.can_data_model.setDataDict(self.can_generator_dict)
            self.can_data_model.signalUpdate()
            self.can_table.resizeRowsToContents()     
            self.can_table.scrollToBottom()
            self.can_table.resizeColumnsToContents()
            



    def write_file(self):
        self.send_command("SAVE")

    def build_network_tab(self):
        self.can0_stream_box =  QCheckBox("Stream CAN0/J1939")
        self.can0_stream_box.clicked.connect(self.send_stream_can0)
        self.network_tab_layout.addWidget(self.can0_stream_box,0,0,1,1)

        self.can1_stream_box =  QCheckBox("Stream CAN1/(PT CAN)")
        self.can1_stream_box.clicked.connect(self.send_stream_can1)
        self.network_tab_layout.addWidget(self.can1_stream_box,0,2,1,1)

        #The CAN2 seems to be broken
        self.can2_stream_box =  QCheckBox("Stream CAN2 (MCP CAN)")
        self.can2_stream_box.clicked.connect(self.send_stream_can2)
        #self.network_tab_layout.addWidget(self.can2_stream_box,0,4,1,1)

        self.J1708_stream_box =  QCheckBox("Stream J1708/J1587")
        self.J1708_stream_box.clicked.connect(self.send_stream_j1708)
        self.network_tab_layout.addWidget(self.J1708_stream_box,0,6,1,1)

        self.LIN_stream_box =  QCheckBox("Stream LIN")
        self.LIN_stream_box.clicked.connect(self.send_stream_lin)
        self.network_tab_layout.addWidget(self.LIN_stream_box,1,6,1,1)

        self.LIN_suppress_box =  QCheckBox("Suppress LIN")
        self.LIN_suppress_box.clicked.connect(self.send_supress_lin)
        self.network_tab_layout.addWidget(self.LIN_suppress_box,2,6,1,1)



        baud_label = QLabel("CAN0/J1939 Baudrate:")
        self.network_tab_layout.addWidget(baud_label,1,0,1,1)
        self.can0_baud_box = QComboBox()
        self.can0_baud_box.addItem("Auto")
        for speed in CAN_SPEEDS:
            self.can0_baud_box.addItem("{}".format(speed))
        self.can0_baud_box.activated.connect(self.change_can0_baud)
        self.network_tab_layout.addWidget(self.can0_baud_box,1,1,1,1)

        baud_label = QLabel("CAN1/PT-CAN Baudrate:")
        self.network_tab_layout.addWidget(baud_label,1,2,1,1)
        self.can1_baud_box = QComboBox()
        self.can1_baud_box.addItem("Auto")
        for speed in CAN_SPEEDS:
            self.can1_baud_box.addItem("{}".format(speed))
        self.can1_baud_box.activated.connect(self.change_can1_baud)
        self.network_tab_layout.addWidget(self.can1_baud_box,1,3,1,1)

        baud_label = QLabel("CAN2/MCP-CAN Baudrate:")
        #self.network_tab_layout.addWidget(baud_label,1,4,1,1)
        self.can2_baud_box = QComboBox()
        self.can2_baud_box.addItem("Auto")
        for speed in CAN_SPEEDS:
            self.can2_baud_box.addItem("{}".format(speed))
        self.can2_baud_box.activated.connect(self.change_can2_baud)
        #self.network_tab_layout.addWidget(self.can2_baud_box,1,5,1,1)

        rx_label = QLabel("CAN0/J1939 Receive Count:")
        self.network_tab_layout.addWidget(rx_label,2,0,1,1)
        self.can0_rx_count = QLineEdit()
        self.network_tab_layout.addWidget(self.can0_rx_count,2,1,1,1)

        tx_label = QLabel("CAN0/J1939 Transmit Count:")
        self.network_tab_layout.addWidget(tx_label,3,0,1,1)
        self.can0_tx_count = QLineEdit()
        self.network_tab_layout.addWidget(self.can0_tx_count,3,1,1,1)

        rx_label = QLabel("CAN1/PT-CAN Receive Count:")
        self.network_tab_layout.addWidget(rx_label,2,2,1,1)
        self.can1_rx_count = QLineEdit()
        self.network_tab_layout.addWidget(self.can1_rx_count,2,3,1,1)
        
        tx_label = QLabel("CAN1/PT-CAN Transmit Count:")
        self.network_tab_layout.addWidget(tx_label,3,2,1,1)
        self.can1_tx_count = QLineEdit()
        self.network_tab_layout.addWidget(self.can1_tx_count,3,3,1,1)

        rx_label = QLabel("CAN2/MCP-CAN Receive Count:")
        #self.network_tab_layout.addWidget(rx_label,3,4,1,1)
        self.can2_rx_count = QLineEdit()
        #self.network_tab_layout.addWidget(self.can2_rx_count,3,5,1,1)
        
        rx_label = QLabel("CAN2/MCP-CAN Transmit Count:")
        #self.network_tab_layout.addWidget(rx_label,3,4,1,1)
        self.can2_tx_count = QLineEdit()
        #self.network_tab_layout.addWidget(self.can2_tx_count,3,5,1,1)

        self.CAN_RX_text_box =  QPlainTextEdit(self)
        self.network_tab_layout.addWidget(self.CAN_RX_text_box,4,0,1,4)
        
        rx_label = QLabel("J1708/J1587 Receive Count:")
        self.network_tab_layout.addWidget(rx_label,0,4,1,1)
        self.j1708_rx_count = QLineEdit()
        self.network_tab_layout.addWidget(self.j1708_rx_count,0,5,1,1)

        rx_label = QLabel("LIN Receive Count:")
        self.network_tab_layout.addWidget(rx_label,1,4,1,1)
        self.lin_rx_count = QLineEdit()
        self.network_tab_layout.addWidget(self.lin_rx_count,1,5,1,1)

        tx_label = QLabel("LIN Transmit Count:")
        self.network_tab_layout.addWidget(tx_label,2,4,1,1)
        self.lin_tx_count = QLineEdit()
        self.network_tab_layout.addWidget(self.lin_tx_count,2,5,1,1)
        

       

    def change_can0_baud(self):
        selection = self.can0_baud_box.currentText()
        if "Auto" in selection:
            commandString = "B0,"
        else:
            commandString = "B0,{}".format(selection)
        self.send_command(commandString) 

    def change_can1_baud(self):
        selection = self.can1_baud_box.currentText()
        if "Auto" in selection:
            commandString = "B1,"
        else:
            commandString = "B1,{}".format(selection)
        self.send_command(commandString) 

    def change_can2_baud(self):
        selection = self.can2_baud_box.currentText()
        if "Auto" in selection:
            commandString = "BMCP,"
        else:
            commandString = "BMCP,{}".format(selection)
        self.send_command(commandString) 

    def send_stream_lin(self):
        if self.LIN_stream_box.isChecked():
            commandString = "LIN,1"
        else:
            commandString = "LIN,0"
        self.send_command(commandString)  

    def send_supress_lin(self):
        if self.LIN_suppress_box.isChecked():
            commandString = "SENDLIN,1"
        else:
            commandString = "SENDLIN,0"
        self.send_command(commandString)       

    def send_stream_j1708(self):
        if self.J1708_stream_box.isChecked():
            commandString = "J1708,1"
        else:
            commandString = "J1708,0"
        self.send_command(commandString)  

    def send_stream_can0(self):
        if self.can0_stream_box.isChecked():
            commandString = "C0,1"
        else:
            commandString = "C0,0"
        self.send_command(commandString)

    def send_stream_can1(self):
        if self.can1_stream_box.isChecked():
            commandString = "C1,1"
        else:
            commandString = "C1,0"
        self.send_command(commandString)

    def send_stream_can2(self):
        if self.can2_stream_box.isChecked():
            commandString = "C2,1"
        else:
            commandString = "C2,0"
        self.send_command(commandString)

    def send_ignition_key_command(self):
        commandString = "50,0"    
        if self.ignition_key_button.isChecked():
            print('\007') #Bell sound
            response =  QMessageBox.question(self,"Turn Key Switch On","Have you loaded or configured the desired settings?\n Would you like to turn on the key switch?")
            if response == QMessageBox.Yes:
                commandString = "50,1"
            else:
                self.ignition_key_button.setChecked()
        self.send_command(commandString)


    def init_gui(self):
        """Builds GUI."""
        self.grid_layout = QGridLayout()
        
        # Build common menu options
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_toolbar = self.addToolBar("File")
        
        load_file = QAction(QIcon(r'icons\icons8_Open_48px_1.png'), '&Load to SSS2', self)
        load_file.setShortcut('Ctrl+L')
        load_file.setToolTip('Load settings file to a Smart Sensor Simulator 2')
        load_file.triggered.connect(self.load_file)
        file_menu.addAction(load_file)
        file_toolbar.addAction(load_file)

        save_file = QAction(QIcon(r'icons\icons8_Save_as_48px.png'), '&Save to File', self)
        save_file.setShortcut('Ctrl+S')
        save_file.setToolTip('Save the current SSS2 settings to a file')
        save_file.triggered.connect(self.save_file)
        file_menu.addAction(save_file)
        file_toolbar.addAction(save_file)

        write_file = QAction(QIcon(r'icons\icons8_Fingerprint_Scan_48px.png'), '&Write to SSS2', self)
        write_file.setShortcut('Ctrl+W')
        write_file.setToolTip('Write the current SSS2 settings to the device memory.')
        write_file.triggered.connect(self.write_file)
        file_menu.addAction(write_file)
        file_toolbar.addAction(write_file)

        reload_file = QAction(QIcon(r'icons\Replay_48px.png'), '&Reload Settings', self)
        reload_file.setShortcut('Ctrl+R')
        reload_file.setToolTip('Reload the SSS2 settings from the current file.')
        reload_file.triggered.connect(self.reload)
        file_menu.addAction(reload_file)
        file_toolbar.addAction(reload_file)

        self.tabs = QTabWidget()
        self.tabs.setTabShape(QTabWidget.Triangular)

        # Button to do something on the right
        self.ignition_key_button =  QCheckBox("Ignition Key Switch")
        self.ignition_key_button.setTristate(True)
        self.ignition_key_button.clicked.connect(self.send_ignition_key_command)
        
        self.tree_tab = QWidget()
        self.tabs.addTab(self.tree_tab,"Settings Tree")
        tree_tab_layout = QVBoxLayout()
        
        #Set up the Table Model/View/Proxy
        self.settings_tree = QTreeView(self)
        self.tree_model = QStandardItemModel()
        self.settings_tree.setModel(self.tree_model)
        self.settings_tree.setAlternatingRowColors(True)
        #self.settings_tree.setSortingEnabled(True)
        self.settings_tree.setHeaderHidden(False)
        self.settings_tree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.settings_tree.doubleClicked.connect(self.enable_edit)
        self.settings_tree.clicked.connect(self.clicked_setting)

        self.settings_tree.model().setHorizontalHeaderLabels(['Item', 'Description', "Setting", 'Value'])
        self.settings_tree.model().dataChanged.connect(self.change_setting)
        self.settings_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.settings_model={}
        self.fill_tree();

        #setup the layout to be displayed in the box
        tree_tab_layout.addWidget(self.settings_tree)
        self.tree_tab.setLayout(tree_tab_layout)

        #Add a networking tab
        self.network_tab = QWidget()
        self.tabs.addTab(self.network_tab,"Networking")
        self.network_tab_layout = QGridLayout()

        self.build_network_tab()
        #setup the layout to be displayed in the box
        self.network_tab.setLayout(self.network_tab_layout)

        self.can_tab = QWidget()
        self.tabs.addTab(self.can_tab,"Message Generator")
        self.can_tab_layout = QGridLayout()

        self.build_can_generator_tab()
        #setup the layout to be displayed in the box
        self.can_tab.setLayout(self.can_tab_layout)
        

        self.grid_layout.addWidget(self.ignition_key_button,0,0,1,1)
        self.grid_layout.addWidget(self.tabs,1,0,1,1)

        main_widget = QWidget()
        #main_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_widget.setLayout(self.grid_layout)
        self.setCentralWidget(main_widget)
        self.resize(950, 700)
        
        return
        
class CANTableModel(QAbstractTableModel):
    ''' data model for a J1939 Data class '''
    def __init__(self):
        super(CANTableModel, self).__init__()
        self.data_dict = {}
        self.header = []
        self.table_rows = []

    def setDataHeader(self, header):
        self.header = header
        self.first = self.header[0]
        self.header_len = len(self.header)
        
    def setDataDict(self, new_dict):
        self.data_dict = new_dict
        self.table_rows = list(sorted(new_dict.keys()))
        
    def aboutToUpdate(self):
        self.layoutAboutToBeChanged.emit()

    def signalUpdate(self):
        ''' tell viewers to update their data (this is full update, not
        efficient)'''
        self.layoutChanged.emit()

    def headerData(self, section, orientation = Qt.Horizontal, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section + 1
        else:
            return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            key = self.table_rows[index.row()]
            col_name = self.header[index.column()]
            return str(self.data_dict[key][col_name])
        else:
            return QVariant()

    def flags(self, index):
            flags = super(CANTableModel, self).flags(index)
            flags |= ~Qt.ItemIsEditable
            return flags

    def setData(self, index, value, role = Qt.DisplayRole):
        if role == Qt.DisplayRole and index.isValid():
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def rowCount(self, index=QVariant()):
        return len(self.data_dict)

    def columnCount(self, index=QVariant()):
        return len(self.header)

class Proxy(QSortFilterProxyModel):
    def __init__(self):
        super(Proxy, self).__init__()

    def headerData(self, section, orientation, role):
        return self.sourceModel().headerData(section, orientation, role)







































































        
        
        
#         self.tabs = ttk.Notebook(self, name='tabs')
#         self.tabs.grid(row=1,column=0,columnspan=3,sticky=tk.W)

#         self.file_status_string = tk.StringVar(value="Default Settings Loaded")
#         tk.Label(self, textvariable=self.file_status_string, name="file_status_label").grid(row=2,column=0,sticky=tk.W)

#         #self.connection_status_string = tk.StringVar(name='status_string',value="Not Connected.")
#         tk.Label(self, textvariable=self.connection_status_string,name="connection_label").grid(row=2,column=2,sticky="E")

#         self.modified_entry_string = tk.StringVar(name='modified_string',value="")
#         self.modified_entry = tk.Entry(self, textvariable=self.modified_entry_string)
#         self.modified_entry.grid(row=2,column=1)
#         self.modified_entry['justify']=tk.CENTER
        

        
#         # create each Notebook tab in a Frame
#         #Create a Settings Tab to amake the adjustments for sensors
#         self.profile_tab = tk.Frame(self.tabs, name='profile_tab')
#         self.tabs.add(self.profile_tab, text="ECU Profile Settings") # add tab to Notebook

#         #Create a Potentiometers Tab to amake the adjustments for sensors
#         self.settings_tab = tk.Frame(self.tabs, name='potentiometer_tab')
#         self.tabs.add(self.settings_tab, text="Digital Potentiometers") # add tab to Notebook
         
#         #Create an additional Tab to interface with the SSS
#         self.extra_tab = tk.Frame(self.tabs, name='extra_tab')
#         self.tabs.add(self.extra_tab, text="Extra Outputs") # add tab to Notebook
        
#         #Create a Voltage out make the adjustments for PWM, DAC, and Regulators
#         self.voltage_out_tab = tk.Frame(self.tabs, name='voltage_out_tab')
#         self.tabs.add(self.voltage_out_tab, text="Voltage Output") # add tab to Notebook
        
#         #Create a Networks Tab to make the adjustments for J1939, CAN and J1708
#         self.truck_networks_tab = tk.Frame(self.tabs, name='truck_network_tab')
#         self.tabs.add(self.truck_networks_tab, text="Network Message Generator") # add tab to Notebook

#         #Create a Connections Tab to interface with the SSS
#         self.data_logger_tab = tk.Frame(self.tabs, name='data_logger')
#         self.tabs.add(self.data_logger_tab, text="Data Logger") # add tab to Notebook

#         #Create a Monitor Tab to interface with the SSS
#         self.monitor_tab = tk.Frame(self.tabs, name='monitor tab')
#         self.tabs.add(self.monitor_tab, text="SSS2 Command Interface") # add tab to Notebook

        

#         self.tabs.enable_traversal()
        
          
#         self.root.option_add('*tearOff', 'FALSE')
#         self.menubar = tk.Menu(self.root,name='main_menus')
 
#         self.menu_file = tk.Menu(self.menubar)
#         self.menu_connection = tk.Menu(self.menubar)
#         self.menu_tools = tk.Menu(self.menubar)
        
#         self.menu_file.add_command(label='Open...', command=self.open_settings_file, accelerator="Ctrl+O")
#         self.menu_file.add_command(label='Save', command=self.save_settings_file, accelerator="Ctrl+S")
#         self.menu_file.add_command(label='Save As...', command=self.saveas_settings_file, accelerator="Ctrl+A")
#         self.menu_file.add_command(label='Save Serial Log', command=self.save_log_file, accelerator="Ctrl+L")
#         self.menu_file.add_command(label='Print as Text', command=self.print_settings_file, accelerator="Ctrl+P")
#         self.menu_file.add_separator()
#         self.menu_file.add_command(label='Refresh', command=self.init_tabs, accelerator="Ctrl+R")
#         self.menu_file.add_separator()
#         self.menu_file.add_command(label='Exit', command=self.on_quit, accelerator="Ctrl+Q")
#         self.menu_connection.add_command(label='Select COM Port',
#                                          command=self.connect_to_serial)
#         self.menu_connection.add_separator()
#         self.menu_connection.add_command(label='Get Unique ID',
#                                          command=self.get_sss2_unique_id)
#         self.menu_tools.add_command(label='Export Wiring Table',
#                                          command=self.export_wiring)
#         self.menu_tools.add_separator()
#         self.menu_tools.add_command(label='Version Information',
#                                          command=self.current_version)
        
#         self.menubar.add_cascade(menu=self.menu_file, label='File')
#         self.menubar.add_cascade(menu=self.menu_connection, label='Connection')
#         self.menubar.add_cascade(menu=self.menu_tools, label='Tools')

#         self.bind_all("<Control-o>",self.open_settings_file)
#         self.bind_all("<Control-s>",self.save_settings_file)
#         self.bind_all("<Control-a>",self.saveas_settings_file)
#         self.bind_all("<Control-r>",self.init_tabs)
#         self.bind_all("<Control-q>",self.on_quit)
#         self.bind_all("<Control-k>",self.send_ignition_key_command)
#         self.bind_all("<Control-l>",self.save_log_file)
#         self.bind_all("<Control-p>",self.print_settings_file)
        
#         self.root.config(menu=self.menubar)
        
        
#         self.serial_connected = False
#         self.serial_rx_byte_list = []
#         self.received_can0_messages=[]
#         self.received_can1_messages=[]
#         self.received_can2_messages=[]
#         self.received_j1708_messages=[]
#         self.received_lin_messages=[]
#         self.received_analog_messages=[]
#         self.data_logger()
#         self.settings_monitor_setup()
#         self.connect_to_serial(auto=True)
#         self.process_serial()
#         self.tx_queue.put_nowait("Time,{:d}".format( int( time.time() - time.timezone + time.daylight*3600 )))
#         #self.init_tabs()
        
#     def current_version(self):
#         messagebox.showinfo("Current Version",
#                            "The SSS2 Interface App is on release version {}.\nThe release date is {}\nSee http://www.synercontechnologies.com/sss2/ for more information.".format(release_version,release_date))
        
#     def init_tabs(self,event=None):
        
        
#         self.tx_queue.put("50,0")
#         #time.sleep(.25)
        
#         if self.autosave_job is not None:
#             self.after_cancel(self.autosave_job)
#             self.autosave_job = None
#         if self.update_job is not None:
#             self.after_cancel(self.update_job)
#             self.update_job = None

#         for child in self.settings_tab.winfo_children():
#             child.destroy()        
#         for child in self.voltage_out_tab.winfo_children():
#             child.destroy()
#         for child in self.truck_networks_tab.winfo_children():
#             child.destroy()
#         for child in self.extra_tab.winfo_children():
#             child.destroy()

        
#         self.data_logger()
        
#         self.potentiometer_settings() #put this after the serial connections

#         self.voltage_out_settings()

#         self.vehicle_networks_settings()

#         self.profile_settings()
        
#         self.tabs.select(self.extra_tab)
#         self.tabs.select(self.data_logger_tab)
#         self.tabs.select(self.truck_networks_tab)
#         self.tabs.select(self.voltage_out_tab)
#         self.tabs.select(self.settings_tab)
#         self.tabs.select(self.profile_tab)

#         self.send_stream_A21()
#         self.send_stream_can0()
#         self.send_stream_can1()
#         self.send_stream_j1708()

#         self.clear_j1939_buffer()
#         self.clear_can2_buffer()
#         self.clear_j1708_buffer()
#         self.clear_analog_buffer()

#         self.get_sss2_component_id()
#         time.sleep(.05)
#         self.get_sss2_software_id()

#         time.sleep(.1)
#         self.update_sha()
#         if self.filename is not None:
#             self.autosave()
            
        
#        #Use these messages to determine window size during development.  
#        # logger.debug("Window Height: {}".format(self.root.winfo_height()))
#        # logger.debug("Window Width: {}".format(self.root.winfo_width()))
       
    
                
#     def export_wiring(self):
#         for group_key in self.settings_dict["Potentiometers"]:
#             for pair_key in self.settings_dict["Potentiometers"][group_key]["Pairs"]:
#                 for pot_key in self.settings_dict["Potentiometers"][group_key]["Pairs"][pair_key]["Pots"]:
#                     pot = self.settings_dict["Potentiometers"][group_key]["Pairs"][pair_key]["Pots"][pot_key]
#                     if len(pot["Application"]) > 1:
#                         self.wiring_dict[pot["Pin"]]={"Wire Color":pot["Wire Color"],"Application":pot["Application"],"ECU Pins":pot["ECU Pins"]}
#         for dac_key in self.settings_dict["DACs"]:
#             dac = self.settings_dict["DACs"][dac_key]
#             if len(dac["Application"]) > 1:
#                 self.wiring_dict[dac["Pin"]]={"Wire Color":dac["Wire Color"],"Application":dac["Application"],"ECU Pins":dac["ECU Pins"]}
#         for pwm_key in self.settings_dict["PWMs"]:
#             pwm = self.settings_dict["PWMs"][pwm_key]
#             if len(pwm["Application"]) > 1:
#                 self.wiring_dict[pwm["Pin"]]={"Wire Color":pwm["Wire Color"],"Application":pwm["Application"],"ECU Pins":pwm["ECU Pins"]}
#         pwm = self.settings_dict["HVAdjOut"]
#         if len(pwm["Application"]) > 1:
#             self.wiring_dict[pwm["Pin"]]={"Wire Color":pwm["Wire Color"],"Application":pwm["Application"],"ECU Pins":pwm["ECU Pins"]}
        
#         types = [('Tab delimited file', '*.txt')]
#         idir = self.home_directory
#         ifile = "SSS2 Partial Wiring Table"
#         title='SSS2 Wiring Table'
#         wiring_filename = filedialog.asksaveasfilename( filetypes=types,
#                                            initialdir=idir,
#                                            initialfile=ifile,
#                                            title=title,
#                                            defaultextension=".txt")
#         w=self.wiring_dict
#         formatted_keys={}
#         for key in w:
#             cavity=key.split(":")
#             formatted_keys[key]="{}:{:02d}".format(cavity[0],int(cavity[1]))
#         sorted_keys = sorted(formatted_keys.items(), key=itemgetter(1))    
#         with open(wiring_filename,'w') as f:
#             f.write("Molex Pins\tColor\tApplication\tECU Pins\n")
#             for key,label in sorted_keys:
#                 f.write("\t".join([formatted_keys[key],w[key]["Wire Color"],w[key]["Application"],w[key]["ECU Pins"]])+"\n")
#         logger.debug("Saved "+wiring_filename)
#         self.file_status_string.set("Saved "+wiring_filename)
            
#     def print_settings_file(self,event=None):
#         try:
#             original_file = self.filename
#             self.filename += ".txt"
#             self.save_settings_file()
#             os.startfile(self.filename, "open")
#             logger.debug("Saved and opened "+self.filename)
            
#         except Exception as e:
#             logger.debug(e)
#             messagebox.showerror("Print File Error",
#                            "There is not a default application to print text (.txt) files. Please configure your system environment to print text files.")
                        
            
#     def open_settings_file(self,event=None):
          
#         types = [('Smart Sensor Simulator 2 Settings Files', '*.SSS2'),('All Files', '*')]
#         idir = self.home_directory
#         ifile = self.filename
#         title='SSS2 Settings File'
#         self.filename = filedialog.askopenfilename(filetypes=types,
#                                                      initialdir=idir,
#                                                      initialfile=ifile,
#                                                      title=title,
#                                                      defaultextension=".SSS2")
      
#         try:
#             with open(self.filename,'r') as infile:
#                 new_settings_dict=json.load(infile)

#             if (len(new_settings_dict["Analog Calibration"]) < len(self.settings_dict["Analog Calibration"])):
#                 new_settings_dict["Analog Calibration"] = self.settings_dict["Analog Calibration"]

#             self.settings_dict["CAN"]={}

#             self.settings_dict = update_dict(self.settings_dict,new_settings_dict)
            
#         except Exception as e:
#             logger.debug(e)
#             messagebox.showerror("Loading File Error",
#                            "The file selected is not the appropriate type for this program. This file may have been corrupted. The file must be a correctly formatted JSON file. Please select a different file.")
                        
#             return

#         digest_from_file=self.settings_dict["SHA256 Digest"]
#         logger.debug("digest_from_file: ",end='')
#         logger.debug(digest_from_file)
        
#         newhash=self.get_settings_hash()

#         logger.debug("newhash:          ",end='')
#         logger.debug(newhash)
        
#         ok_to_open = False
   
#         if newhash==digest_from_file or UNIVERSAL:
#             logger.debug("Hash system OK.")
#             sss2_id = self.settings_dict["SSS2 Product Code"].strip()
#             if  sss2_id == "UNIVERSAL":
#                 ok_to_open = True
#             else:
#                 try:
#                     if self.serial.isOpen():
                        
#                         command_string = "OK,{}".format(sss2_id)
#                         self.tx_queue.put_nowait(command_string)
#                         self.wait_variable(self.file_OK_received)       
#                         self.file_OK_received.set(False)
#                         if not self.file_authenticated:
#                             self.settings_dict = get_default_settings()
#                             messagebox.showwarning("Incompatible SSS2",
#                                 "The Unique ID for the SSS2 does not match the file. Files are save for specific SSS2 units only and cannot be transfered from one to another. Please enter or get the correct Unique ID")
#                             self.tabs.select(self.profile_tab)
#                             self.sss2_product_code.focus()
#                             self.sss2_product_code['bg']='yellow'
#                         else:
#                             ok_to_open = True
#                             self.sss2_product_code['bg']='white'
#                     else:
#                         messagebox.showerror("SSS2 Needed to Open File",
#                            "Please connect the Smart Sensor Simulator 2 with USB to open a file. User saved files are specific to each SSS2 unit.")
#                         self.connect_to_serial()


#                 except Exception as e:
#                     logger.debug(e)
#                     messagebox.showerror("Connect SSS2",
#                            "Please connect to the Smart Sensor Simulator 2 unit with serial number {} to open a file. Be sure the SSS2 product code under the\n USB/Serial Interface tab is correct. The current code that is entered is {}.".format(self.settings_dict["Serial Number"],self.settings_dict["SSS2 Product Code"]) )
#                     self.connect_to_serial()
                  
#         else:
#             logger.debug("Hash values different, Reloading defaults.")
#             self.settings_dict = get_default_settings()
#             messagebox.showerror("File Integrity Error",
#                     "The hash value from the file\n {}\n does not match the new calculated hash.\n The file may have been altered. \nReloading defaults.".format(self.filename) )
#             self.file_status_string.set("Error Opening "+self.filename)
#         if ok_to_open:
#             self.file_status_string.set("Opened "+self.filename)
#             self.settings_file_status_string.set(os.path.basename(self.filename))
#             logger.debug("Opened "+self.filename)
#             self.settings_dict["SHA256 Digest"]=self.get_settings_hash()

#         else:
#             self.settings_dict = get_default_settings()    

#         self.send_clear_can()
#         self.init_tabs()
        
        
    
#     def saveas_settings_file(self,event=None):
#         types = [('Smart Sensor Simulator 2 Settings Files', '*.SSS2')]
#         idir = self.home_directory
#         ifile = self.filename
#         title='SSS2 Settings File'
#         self.filename = filedialog.asksaveasfilename( filetypes=types,
#                                            initialdir=idir,
#                                            initialfile=ifile,
#                                            title=title,
#                                            defaultextension=".SSS2")
#         self.save_settings_file()

#     def save_settings_file(self,event=None):

#         if self.filename is None:
#             self.saveas_settings_file()

#         if self.filename is '':
#             self.file_status_string.set("File not saved.")
#             logger.debug("File not saved.") 
#             return
        
#         ok_to_save = False
#         sss2_id = self.sss2_product_code_text.get().strip()
#         if not sss2_id == "UNIVERSAL":
#                 if self.serial is not None:
#                     command_string = "OK,{}".format(sss2_id.strip())
#                     self.tx_queue.put_nowait(command_string)
#                     self.wait_variable(self.file_OK_received)       
#                     self.file_OK_received.set(False)
#                     if self.file_authenticated: 
#                         ok_to_save = True
#                     logger.debug("Authenticated. OK to Save")
#         else:
#             if UNIVERSAL:
#                 ok_to_save = True 
#             else:
#                 ok_to_save = False 
#         if ok_to_save:
#             self.settings_dict["SSS2 Interface Release Date"] = self.release_date
#             self.settings_dict["SSS2 Interface Version"] = self.release_version

#             self.interface_date.set(self.release_date)
#             self.interface_release.set(self.release_version)
            
#             self.file_status_string.set("Saved "+self.filename)
#             self.settings_file_status_string.set(os.path.basename(self.filename))
            
#             logger.debug("Saved "+self.filename)
#             self.sss2_product_code['bg']='white'

#             self.saved_date_text.set(time.strftime("%A, %d %B %Y %H:%M:%S %Z", time.localtime()))
#             self.update_dict()
#             self.settings_dict["SHA256 Digest"]=self.get_settings_hash()
#             self.settings_dict["Original File SHA"]=self.settings_dict["SHA256 Digest"]
            

             
#             with open(self.filename,'w') as outfile:
#                 json.dump(self.settings_dict,outfile,indent=4,sort_keys=True)

            
        

#         else:
#             self.file_status_string.set("")
#             self.file_status_string.set("File not saved.")
#             logger.debug("File not saved.") 
#             messagebox.showerror("Incompatible SSS2 for Saving",
#                             "The unique ID entered for the SSS2 does not match the unit. Please select Get ID from the Connection menu to get the SSS2 Unique ID to populate the form.")
#             self.tabs.select(self.profile_tab)
#             self.sss2_product_code.focus()
#             self.sss2_product_code['bg']='yellow'
        
#     def save_log_file(self,event=None):
#         ifile = "SSS2_Log_{}.log".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         if os.path.exists(self.home_directory):
#             log_filename = self.home_directory + ifile
#         else:
#             log_filename = os.path.expanduser('~') + os.sep + ifile
#         with open(log_filename,'w') as log_file:
#             for byte_entry in self.serial_rx_byte_list:
#                 log_file.write(byte_entry.decode('ascii',"ignore"))
#         logger.debug("Saved {}".format(log_filename))
#         self.file_status_string.set("Saved log data to "+log_filename)
                       
#     def get_settings_hash(self):
#         digest_from_file=self.settings_dict["Original File SHA"]
#         load_date = self.settings_dict["Original Creation Date"]
#         save_date = self.settings_dict["Saved Date"]
        
         
        
#         new_hash               = self.settings_dict.pop("SHA256 Digest",None)
#         digest_from_file       = self.settings_dict.pop("Original File SHA",None)
#         load_date              = self.settings_dict.pop("Original Creation Date",None)
#         save_date              = self.settings_dict.pop("Saved Date",None)
#         sss_software_ID        = self.settings_dict.pop("Software ID",None)
#         sss_component_ID       = self.settings_dict.pop("Component ID",None)
#         sss_serial_ID          = self.settings_dict.pop("Serial Number",None)
#         sss_interface_version  = self.settings_dict.pop("SSS2 Interface Version",None)
#         sss_interface_date     = self.settings_dict.pop("SSS2 Interface Release Date",None)
        
#         temp_settings_dict = pformat(self.settings_dict)
#         new_hash = str(hashlib.sha256(bytes(temp_settings_dict,'utf-8')).hexdigest())
        
#         self.settings_dict["SHA256 Digest"]               = new_hash
#         self.settings_dict["Original File SHA"]           = digest_from_file
#         self.settings_dict["Original Creation Date"]      = load_date
#         self.settings_dict["Saved Date"]                  = save_date
#         self.settings_dict["Component ID"]                = sss_component_ID
#         self.settings_dict["Software ID"]                 = sss_software_ID
#         self.settings_dict["Serial Number"]               = sss_serial_ID
#         self.settings_dict["SSS2 Interface Version"]      = sss_interface_version
#         self.settings_dict["SSS2 Interface Release Date"] = sss_interface_date

#         if self.settings_dict["Original File SHA"] ==  "Current Settings Not Saved.":
#             self.modified_entry_string.set("Default Settings")
#             self.modified_entry['bg']='yellow'
#         else:
#             if digest_from_file == new_hash:
#                 self.modified_entry_string.set("Settings Unchanged")
#                 self.modified_entry['bg']='light green'
#             else:
#                 self.modified_entry_string.set("Settings Altered")
#                 self.modified_entry['bg']='red'
        
#         return new_hash

#     def autosave(self):
#         if self.lasthash != self.current_hash:
#             original_file = self.filename
#             try:
#                 if self.filename[-14:] == ".SSS2.AUTOSAVE":
#                     original_file = self.filename[:-14]
#                 else:
#                     self.filename += ".AUTOSAVE"
#             except Exception as e:
#                 logger.debug(e)
#                 self.filename += ".AUTOSAVE"
#             with open(self.filename,'w') as outfile:
#                 json.dump(self.settings_dict,outfile,indent=4,sort_keys=True)
#             self.filename = original_file
#             #logger.debug('Autosaving')
            
#         self.lasthash = self.current_hash 
        
#         self.autosave_job = self.after(5000,self.autosave)

#     def update_sha(self):
#         self.update_dict()
#         self.file_sha_string.set(self.settings_dict["Original File SHA"])
#         self.current_hash = self.get_settings_hash()
#         self.settings_sha_string.set(self.current_hash)

#         self.update_job = self.after(500,self.update_sha)
        
#     def enable_can_component_id(self):
#         commandString = "CANCOMP,{}".format(self.can_component_id_text.get())
#         self.tx_queue.put_nowait(commandString)

#     def profile_settings(self):
#         self.ecu_frame = tk.LabelFrame(self.profile_tab, name="ecu_frame",
#                                                   text="Electronic Control Unit (ECU) Settings")
#         self.ecu_frame.grid(row=0,column=0,sticky=tk.E+tk.W,columnspan=1)
#         #User Changable values
#         tk.Label(self.ecu_frame,text="ECU Year:").grid(row=0,column=0,sticky=tk.W)
#         self.ecu_year_text = tk.StringVar(value = self.settings_dict["ECU Year"])
#         self.ecu_year = tk.Entry(self.ecu_frame,textvariable= self.ecu_year_text, width=5)
#         self.ecu_year.grid(row=0,column=1,sticky=tk.W,padx=5,pady=5)

#         tk.Label(self.ecu_frame,text="ECU Make:").grid(row=0,column=3,sticky=tk.E)
#         self.ecu_make_text = tk.StringVar(value = self.settings_dict["ECU Make"])
#         self.ecu_make = tk.Entry(self.ecu_frame,textvariable= self.ecu_make_text, width=16)
#         self.ecu_make.grid(row=0,column=4,sticky=tk.W,padx=5,pady=5)

#         tk.Label(self.ecu_frame,text="ECU Model:").grid(row=0,column=5,sticky=tk.E)
#         self.ecu_model_text = tk.StringVar(value = self.settings_dict["ECU Model"])
#         self.ecu_model = tk.Entry(self.ecu_frame,textvariable= self.ecu_model_text, width=24)
#         self.ecu_model.grid(row=0,column=6,sticky=tk.W,padx=5,pady=5)

#         tk.Label(self.ecu_frame,text="ECU Software Version:").grid(row=2,column=0,sticky=tk.W,columnspan=2)
#         self.sss_ecu_id_text = tk.StringVar(value = self.settings_dict["ECU Software Version"])
#         self.sss_ecu_id = tk.Entry(self.ecu_frame, textvariable= self.sss_ecu_id_text, width=74)
#         self.sss_ecu_id.grid(row=2,column=2,sticky=tk.W,padx=5,pady=5,columnspan=6)
#         #tk.Button(self.ecu_frame,text="Get SW",command=self.get_ecu_software_id).grid(row=2,column=8,sticky=tk.W,padx=5)

#         tk.Label(self.ecu_frame,text="Engine Serial Number:").grid(row=1,column=0,sticky=tk.W,columnspan=2)
#         self.engine_serial_text = tk.StringVar(value = self.settings_dict["Engine Serial Number"])
#         self.engine_serial = tk.Entry(self.ecu_frame, textvariable= self.engine_serial_text, width=74)
#         self.engine_serial.grid(row=1,column=2,sticky=tk.W,padx=5,pady=5,columnspan=6)
        
#         tk.Label(self.ecu_frame,text="Veh. Year:").grid(row=3,column=0,sticky=tk.W)
#         self.vehicle_year_text = tk.StringVar(value = self.settings_dict["Vehicle Year"])
#         self.vehicle_year = tk.Entry(self.ecu_frame,textvariable= self.vehicle_year_text, width=5)
#         self.vehicle_year.grid(row=3,column=1,sticky=tk.W,padx=5,pady=5)

#         tk.Label(self.ecu_frame,text="Vehicle Make:").grid(row=3,column=3,sticky=tk.E)
#         self.vehicle_make_text = tk.StringVar(value = self.settings_dict["Vehicle Make"])
#         self.vehicle_make = tk.Entry(self.ecu_frame,textvariable= self.vehicle_make_text, width=20)
#         self.vehicle_make.grid(row=3,column=4,sticky=tk.W,padx=5,pady=5)

#         tk.Label(self.ecu_frame,text="Vehicle Model:").grid(row=3,column=5,sticky=tk.E)
#         self.vehicle_model_text = tk.StringVar(value = self.settings_dict["Vehicle Model"])
#         self.vehicle_model = tk.Entry(self.ecu_frame,textvariable= self.vehicle_model_text, width=24)
#         self.vehicle_model.grid(row=3,column=6,sticky=tk.W,padx=5,pady=5)

#         tk.Label(self.ecu_frame,text="Vehicle ID (VIN):").grid(row=4,column=0,sticky=tk.W,columnspan=2)
#         self.vehicle_vin_text = tk.StringVar(value = self.settings_dict["Vehicle VIN"])
#         self.vehicle_vin = tk.Entry(self.ecu_frame, textvariable= self.vehicle_vin_text, width=74)
#         self.vehicle_vin.grid(row=4,column=2,sticky=tk.W,padx=5,pady=5,columnspan=6)

#         tk.Label(self.ecu_frame,text="ECU Component ID:").grid(row=5,column=0,sticky=tk.W,columnspan=2)
#         self.ecu_component_id_text = tk.StringVar(value = self.settings_dict["ECU Component ID"])
#         self.ecu_component_id = tk.Entry(self.ecu_frame, textvariable= self.ecu_component_id_text, width=74)
#         self.ecu_component_id.grid(row=5,column=2,sticky=tk.W,padx=5,pady=5,columnspan=6)
#         #tk.Button(self.ecu_frame,text="Get ID",command=self.get_ecu_software_id).grid(row=5,column=8,sticky=tk.W,padx=5)

#         tk.Label(self.ecu_frame,text="ECU Configuration:").grid(row=6,column=0,sticky=tk.W,columnspan=2)
#         self.ecu_configuration_text = tk.StringVar(value = self.settings_dict["Engine Configuration"])
#         self.ecu_configuration = tk.Entry(self.ecu_frame, textvariable= self.ecu_configuration_text, width=74)
#         self.ecu_configuration.grid(row=6,column=2,sticky=tk.W,padx=5,pady=5,columnspan=6)
        
        
#         self.sss2_frame = tk.LabelFrame(self.profile_tab, name="sss2_frame",
#                                                   text="Smart Sensor Simulator 2 (QWidget) Settings")
#         self.sss2_frame.grid(row=1,column=0,sticky=tk.E+tk.W,columnspan=1)

#         tk.Label(self.sss2_frame,text="SSS2 Component ID:").grid(row=0,column=0,sticky=tk.W)
        
#         self.sss2_serial_number = tk.Entry(self.sss2_frame, name="sss2_serial",textvariable=self.sss_component_id_text,width=75)
#         self.sss2_serial_number.grid(row=0,column=1,sticky=tk.W,padx=5,pady=5,columnspan=2)
#         self.sss2_serial_number.configure(state='readonly')
        
#         #self.sss2_serial_number.insert(0,self.settings_dict["Component ID"])
#         self.can_component_id_text = tk.StringVar(value = self.settings_dict["Send SSS2 Component ID"])
#         self.can_component_id = ttk.Checkbutton(self.sss2_frame,
#                                                 text="Send SSS2 Component Information over J1939",
#                                                 command=self.enable_can_component_id,
#                                                 variable = self.can_component_id_text,
#                                                 onvalue="1",
#                                                 offvalue="0")
#         self.can_component_id.grid(row=1,column=1,sticky=tk.W,columnspan=2)
#         self.can_component_id.state(['!alternate']) #Clears Check Box
        

#         #Uncomment for commissioning
#         #tk.Button(self.sss2_frame,text="Set ID",command=self.set_sss2_component_id).grid(row=0,column=8,sticky=tk.W,padx=5)


#         tk.Label(self.sss2_frame,text="SSS2 Unique ID:").grid(row=2,column=0,sticky=tk.W)
#         self.sss2_product_code_text = tk.StringVar(value = self.settings_dict["SSS2 Product Code"])
#         self.sss2_product_code = tk.Entry(self.sss2_frame,textvariable= self.sss2_product_code_text,width=75)
#         self.sss2_product_code.grid(row=2,column=1,sticky=tk.W,padx=5,pady=5,columnspan=2)
#         #tk.Button(self.sss2_frame,text="Get ID",command=self.get_sss2_unique_id).grid(row=1,column=7,sticky=tk.W)


#         tk.Label(self.sss2_frame,text="SSS2 Software ID:").grid(row=3,column=0,sticky=tk.W)
#         self.sss_software_id = tk.Entry(self.sss2_frame, textvariable= self.sss_software_id_text,width=75)
#         self.sss_software_id.grid(row=3,column=1,sticky=tk.W,padx=5,pady=5,columnspan=2)
#         self.sss_software_id.configure(state='readonly')
#         #tk.Button(self.sss2_frame,text="Get ID",command=self.get_sss2_software_id).grid(row=2,column=7,sticky=tk.W)

#         cable_models = ["SSS2-ADEM2",
#                         "SSS2-ADEM3",
#                         "SSS2-ADEM4",
#                         "SSS2-CM500",
#                         "SSS2-CM800",
#                         "SSS2-CM2150",
#                         "SSS2-CM2250",
#                         "SSS2-CM2350",
#                         "SSS2-DDEC4",
#                         "SSS2-DDEC5",
#                         "SSS2-DDEC6",
#                         "SSS2-DDEC10",
#                         "SSS2-ACM",
#                         "SS2-MCM",
#                         "SSS2-TCM",
#                         "SSS2-MBE",
#                         "SSS2-VCU/PLD",
#                         "SSS2-MX",
#                         "SSS2-MaxxForce",
#                         "SSS2-Bendix",
#                         "SSS2-BDX-Chassis",
#                         "SSS2-Wabco",
#                         "SSS2-CUSTOM"]
#         tk.Label(self.sss2_frame,text="SSS2 Cable Model:").grid(row=4,column=0,sticky=tk.W)
#         self.sss2_cable_text = tk.StringVar(value = self.settings_dict["SSS2 Cable"])
#         self.sss2_cable = ttk.Combobox(self.sss2_frame, textvariable= self.sss2_cable_text, values=cable_models)
#         self.sss2_cable.grid(row=4,column=1,sticky=tk.W,padx=5,pady=5,columnspan=1)

#         self.resisor_box_button_text = tk.StringVar(value = self.settings_dict["Resistor Box Used"])
#         self.resisor_box_button = ttk.Checkbutton(self.sss2_frame,text="Supplemental Resistor Box Used",
#                                                   offvalue="No",onvalue="Yes",variable=self.resisor_box_button_text)
#         self.resisor_box_button.grid(row=4,column=2, padx=5, pady =5,sticky="E")
#         self.resisor_box_button.state(['!alternate']) #Clears Check Box
        
#         self.file_frame = tk.LabelFrame(self.profile_tab, name="file_frame",
#                                                   text="Current Settings Information")
#         self.file_frame.grid(row=2,column=0,sticky=tk.N+tk.E+tk.W,columnspan=1)

#         tk.Label(self.file_frame,text="Settings File:").grid(row=0,column=0,sticky=tk.E)
        
#         self.file_status_label = tk.Label(self.file_frame, textvariable=self.settings_file_status_string,name="file_status_label")
#         self.file_status_label.grid(row=0,column=1,sticky=tk.W)
          
#         tk.Label(self.file_frame,text="Current SHA-256 Digest:").grid(row=1,column=0,sticky=tk.E)
#         self.settings_sha_string = tk.StringVar(name='settings-SHA')
#         self.settings_sha_string.set(self.get_settings_hash())
#         self.settings_sha_label = tk.Label(self.file_frame, textvariable=self.settings_sha_string,name="settings_sha_label")
#         self.settings_sha_label.grid(row=1,column=1,sticky=tk.W,columnspan=3)

#         tk.Label(self.file_frame,text="Saved SHA-256 Digest:").grid(row=2,column=0,sticky=tk.E)
#         self.file_sha_string = tk.StringVar(name='file-SHA')
#         self.file_sha_string.set(self.settings_dict["Original File SHA"])
#         self.file_sha_label = tk.Label(self.file_frame, textvariable=self.file_sha_string,name="file_sha_label")
#         self.file_sha_label.grid(row=2,column=1,sticky=tk.W,columnspan=3)

#         self.version_frame = tk.LabelFrame(self.profile_tab, name="version_frame",
#                                                   text="Smart Sensor Simulator Interface Information")
#         self.version_frame.grid(row=3,column=0,sticky=tk.S+tk.E+tk.W,columnspan=1)
#         self.interface_release = tk.StringVar(value=self.settings_dict["SSS2 Interface Version"])
#         tk.Label(self.version_frame,text="File Saved with Smart Sensor Simulator Interface Version:").grid(row=0,column=0,sticky=tk.E)
#         tk.Label(self.version_frame, textvariable=self.interface_release).grid(row=0,column=1,sticky=tk.W,columnspan=3)
#         self.interface_date = tk.StringVar(value=self.settings_dict["SSS2 Interface Release Date"])
#         tk.Label(self.version_frame,text="File Saved with Smart Sensor Simulator Interface Release:").grid(row=1,column=0,sticky=tk.E)
#         tk.Label(self.version_frame, textvariable=self.interface_date).grid(row=1,column=1,sticky=tk.W,columnspan=3)
#         tk.Label(self.version_frame,text="Current Smart Sensor Simulator Interface Version:").grid(row=2,column=0,sticky=tk.E)
#         tk.Label(self.version_frame, text=self.release_version).grid(row=2,column=1,sticky=tk.W,columnspan=3)
#         tk.Label(self.version_frame,text="Current Smart Sensor Simulator Interface Release:").grid(row=3,column=0,sticky=tk.E)
#         tk.Label(self.version_frame, text=self.release_date).grid(row=3,column=1,sticky=tk.W,columnspan=3)
        

#         self.user_frame = tk.LabelFrame(self.profile_tab, name="user_frame",
#                                                   text="User Information")
#         self.user_frame.grid(row=0,column=1,sticky=tk.N+tk.E+tk.W+tk.S,columnspan=1,rowspan=4)

#         tk.Label(self.user_frame,text="Date Loaded:").grid(row=0,column=0,sticky=tk.W,pady=5)
#         self.current_date_text = tk.StringVar(value = time.strftime("%A, %d %B %Y %H:%M:%S %Z", time.localtime()))
#         self.current_date = tk.Label(self.user_frame, textvariable = self.current_date_text)
#         self.current_date.grid(row=0,column=1,sticky=tk.W,padx=5,pady=5)
        
#         tk.Label(self.user_frame,text="Date Saved:").grid(row=1,column=0,sticky=tk.W,pady=5)
#         self.saved_date_text = tk.StringVar(value = self.settings_dict["Saved Date"])
#         self.saved_date = tk.Label(self.user_frame, textvariable = self.saved_date_text)
#         self.saved_date.grid(row=1,column=1,sticky=tk.W,padx=5,pady=5)
        
#         tk.Label(self.user_frame,text="User Name:").grid(row=2,column=0,sticky=tk.W,pady=5)
#         self.user_name_text = tk.StringVar(value = self.settings_dict["Programmed By"])
#         self.user_name = tk.Entry(self.user_frame, textvariable=self.user_name_text ,width=60)
#         self.user_name.grid(row=2,column=1,sticky=tk.W,padx=5,pady=5)
        
#         tk.Label(self.user_frame,text="Company:").grid(row=3,column=0,sticky=tk.W,pady=5)
#         self.company_name_text = tk.StringVar(value = self.settings_dict["Company"])
#         self.company_name = tk.Entry(self.user_frame, textvariable=self.company_name_text ,width=60)
#         self.company_name.grid(row=3,column=1,sticky=tk.W,padx=5,pady=5)

#         tk.Label(self.user_frame,text="Location:").grid(row=4,column=0,sticky=tk.W,pady=5)
#         self.location_name_text = tk.StringVar(value = self.settings_dict["Location"])
#         self.location_name = tk.Entry(self.user_frame, textvariable=self.location_name_text ,width=60)
#         self.location_name.grid(row=4,column=1,sticky=tk.W,padx=5,pady=5)
        
#         tk.Label(self.user_frame,text="Case Number:").grid(row=5,column=0,sticky=tk.W,pady=5)
#         self.case_number_text = tk.StringVar(value = self.settings_dict["Case Number"])
#         self.case_number = tk.Entry(self.user_frame, textvariable=self.case_number_text ,width=60)
#         self.case_number.grid(row=5,column=1,sticky=tk.W,padx=5,pady=5)
        
#         tk.Label(self.user_frame,text="Date:").grid(row=6,column=0,sticky=tk.W,pady=5)
#         self.date_of_loss_text = tk.StringVar(value = self.settings_dict["Date of Loss"])
#         self.date_of_loss = tk.Entry(self.user_frame, textvariable=self.date_of_loss_text ,width=60)
#         self.date_of_loss.grid(row=6,column=1,sticky=tk.W,padx=5)
       
#         tk.Label(self.user_frame,text="User Notes:").grid(row=7,column=0,sticky=tk.W)
#         self.case_notes = tkst.ScrolledText(self.user_frame, height=18,width=53,padx=5,pady=4,wrap=tk.WORD)
#         self.case_notes.grid(row=8,column=0,sticky=tk.W,padx=5,pady=5,columnspan=2)
#         self.case_notes.focus_set()
#         self.case_notes.insert(1.0,self.settings_dict["User Notes"].strip())
        
#         self.warning_frame = tk.LabelFrame(self.profile_tab, name="warning_frame",
#                                                   text="Warnings and Cautions")
#         self.warning_frame.grid(row=4,column=0,sticky=tk.N+tk.E+tk.W,columnspan=2,rowspan=1)
#         self.warning_text = tk.Text(self.warning_frame,height=3,wrap=tk.WORD,width=130)
#         self.warning_text.grid(row=0,column=0,sticky=tk.E+tk.W,padx=5,pady=5)
#         self.warning_text.insert(tk.END,self.settings_dict["Warnings"])
#         self.warning_text.configure(state='disabled')
        
#         logo_file = tk.PhotoImage(file="SynerconLogoWithName.gif")
#         logo = tk.Label(self.profile_tab,image=logo_file)
#         logo.image= logo_file
#         logo.grid(row=0,column=2,sticky=tk.W)
#         logo.bind("<Button-1>", self.open_link)
        
#         link = tk.Label(self.profile_tab, text="Visit: http://www.synercontechnologies.com/SSS2/", fg="blue", cursor="hand2")
#         link.grid(row=4,column=2,sticky=tk.S)
#         link.bind("<Button-1>", self.open_link)

#         angled_photo = tk.PhotoImage(file="sss2angle.gif")
#         new_photo = angled_photo.subsample(2,2)
        
#         image_label = Label(self.profile_tab,image=new_photo)
#         image_label.image = new_photo
#         image_label.grid(row=1,column=2,sticky="NE",rowspan=2)       
        
#         button_frame = tk.Frame(self.profile_tab)
#         button_frame.grid(row=3,column=2,rowspan=2)
#         tk.Button(button_frame,text="Open Settings File",command=self.open_settings_file,width = 50).grid(row=0,column=0,pady=2)
#         tk.Button(button_frame,text="Save Settings File",command=self.save_settings_file,width = 50).grid(row=1,column=0,pady=2)
#         tk.Button(button_frame,text="Save Settings File As...",command=self.saveas_settings_file,width = 50).grid(row=2,column=0,pady=2)
#         tk.Button(button_frame,text="Get SSS2 Unique ID",command=self.get_sss2_unique_id,width = 50).grid(row=3,column=0,pady=2)
        
#     def open_link(self,event=None):
#         webbrowser.open_new(r"http://www.synercontechnologies.com/SSS2/")
        
#     def get_ecu_software_id(self):
#         pass

#     def get_sss2_unique_id(self):
#         commandString = "ID,"
        
#         self.tx_queue.put_nowait(commandString)
        
#     def get_sss2_software_id(self):
#         commandString = "SOFT,"
#         self.tx_queue.put_nowait(commandString)

#     def get_sss2_component_id(self):
#         commandString = "CI,"
#         self.tx_queue.put_nowait(commandString)

#     def set_sss2_component_id(self):
#         commandString = "CI,{}".format(self.sss2_serial_number.get())
#         self.tx_queue.put_nowait(commandString)

#     def update_dict(self):
#         for bank_key in self.pot_bank.keys():
#             group=self.settings_dict["Potentiometers"][bank_key]
            
#             if group["Terminal A Connection"]:
#                 group["Terminal A Connection"] = self.pot_bank[bank_key].bank_button.instate(['selected'])
#             for pair_key in self.pot_bank[bank_key].pot_pairs.keys():
#                 pair=group["Pairs"][pair_key]
#                 if self.pot_bank[bank_key].pot_pairs[pair_key].twelve_volt_switch is not None:
#                     if self.pot_bank[bank_key].pot_pairs[pair_key].twelve_volt_switch.instate(['selected']):
#                         pair["Terminal A Voltage"] = "+12V"
#                     else:
#                         pair["Terminal A Voltage"] = "+5V"
#                 for pot_key in self.pot_bank[bank_key].pot_pairs[pair_key].pots.keys():
#                     pot=pair["Pots"][pot_key]
#                     pot_object = self.pot_bank[bank_key].pot_pairs[pair_key].pots[pot_key]
#                     pot["Term. A Connect"] =    pot_object.terminal_A_connect_button.instate(['selected']) 
#                     pot["Term. B Connect"] =    pot_object.terminal_B_connect_button.instate(['selected']) 
#                     pot["Wiper Connect"]   =    pot_object.wiper_connect_button.instate(['selected']) 
#                     pot["Wiper Position"] = int(pot_object.wiper_position_slider.get())
#                     pot["ECU Pins"] =           pot_object.ecu_app.ecu_pins.get()
#                     pot["Wire Color"] =         pot_object.ecu_app.ecu_color.get()
#                     pot["Application"] =        pot_object.ecu_app.ecu_app.get()

#         for dac_key in self.dac_objects.keys():
#             dac_dict=self.settings_dict["DACs"][dac_key]
#             dac_dict["Average Voltage"] = self.dac_objects[dac_key].dac_mean_slider.get()/100
#             dac_dict["ECU Pins"] =        self.dac_objects[dac_key].ecu_app.ecu_pins.get()
#             dac_dict["Wire Color"] =        self.dac_objects[dac_key].ecu_app.ecu_color.get()
#             dac_dict["Application"] =     self.dac_objects[dac_key].ecu_app.ecu_app.get()

#         for pwm_key in self.pwm_objects.keys():
#             pwm_dict=self.settings_dict["PWMs"][pwm_key]
#             pwm_dict["Duty Cycle"] = self.pwm_objects[pwm_key].pwm_duty_cycle_slider.get()
#             pwm_dict["Frequency"] = self.pwm_objects[pwm_key].pwm_frequency_slider.get()
#             pwm_dict["ECU Pins"] =        self.pwm_objects[pwm_key].ecu_app.ecu_pins.get()
#             pwm_dict["Wire Color"] =        self.pwm_objects[pwm_key].ecu_app.ecu_color.get()
#             pwm_dict["Application"] =     self.pwm_objects[pwm_key].ecu_app.ecu_app.get()

#         hv_dict=self.settings_dict["HVAdjOut"]
#         hv_dict["Average Voltage"] = self.hvadjout.dac_mean_slider.get()/100
#         hv_dict["ECU Pins"] =        self.hvadjout.ecu_app.ecu_pins.get()
#         hv_dict["Wire Color"] =        self.hvadjout.ecu_app.ecu_color.get()
#         hv_dict["Application"] =     self.hvadjout.ecu_app.ecu_app.get()

#         s=self.settings_dict["Switches"]        
#         s["Port 10 or 19"]["State"]=self.vout2a_switch.switch_buttonA.instate(['selected'])
#         s["Port 15 or 18"]["State"]=self.vout2b_switch.switch_buttonA.instate(['selected'])
#         s["CAN1 or J1708"]["State"]=self.j1708_switch.switch_buttonA.instate(['selected'])
#         s["PWMs or CAN2"]["State"]=self.pwm12_switch.switch_buttonA.instate(['selected'])
#         s["CAN0"]["State"]=self.can0_term.switch_button.instate(['selected'])
#         s["CAN1"]["State"]=self.can1_term.switch_button.instate(['selected'])
#         s["CAN2"]["State"]=self.can2_term.switch_button.instate(['selected'])
#         s["LIN Master Pullup Resistor"]["State"]=self.lin_to_master.switch_button.instate(['selected'])
#         s["12V Out 2"]["State"]=self.twelve2_switch.switch_button.instate(['selected'])
#         s["12V Out 1"]["State"]=self.pwm3_switch.switch_buttonB.instate(['selected'])
#         s["Ground Out 1"]["State"]=self.pwm4_switch.switch_buttonB.instate(['selected'])
#         s["Ground Out 2"]["State"]=self.ground2_switch.switch_button.instate(['selected'])
#         s["LIN to SHLD"]["State"]=self.lin_to_shield_switch.switch_button.instate(['selected'])
#         s["LIN to Port 16"]["State"]=self.lin_to_port_16.switch_button.instate(['selected'])
#         s["PWM1 Connect"]["State"]=self.pwm1_switch.switch_button.instate(['selected'])
#         s["PWM2 Connect"]["State"]=self.pwm2_switch.switch_button.instate(['selected'])
#         s["PWM3 or 12V"]["State"]=self.pwm3_switch.switch_buttonA.instate(['selected'])
#         s["PWM4 or Ground"]["State"]=self.pwm4_switch.switch_buttonA.instate(['selected'])
#         s["CAN1 Connect"]["State"]=self.can1_switch.switch_button.instate(['selected'])
#         s["PWM5 Connect"]["State"]=self.pwm5_switch.switch_button.instate(['selected'])
#         s["PWM6 Connect"]["State"]=self.pwm6_switch.switch_button.instate(['selected'])
#         s["PWM4_28 Connect"]["State"]=self.pwm4_28_switch.switch_button.instate(['selected'])

#         self.settings_dict["ECU Year"] = self.ecu_year_text.get()
#         self.settings_dict["ECU Make"] = self.ecu_make_text.get()
#         self.settings_dict["ECU Model"] = self.ecu_model_text.get()
#         self.settings_dict["ECU Software Version"] = self.sss_ecu_id_text.get()
#         self.settings_dict["Engine Serial Number"] = self.engine_serial_text.get()
#         self.settings_dict["Vehicle Year"] = self.vehicle_year_text.get()
#         self.settings_dict["Vehicle Make"] = self.vehicle_make_text.get()
#         self.settings_dict["Vehicle Model"] = self.vehicle_model_text.get()
#         self.settings_dict["Engine Configuration"] = self.ecu_configuration_text.get()
#         self.settings_dict["Component ID"] = self.sss_component_id_text.get()
#         self.settings_dict["Send SSS2 Component ID"] = self.can_component_id_text.get()
#         self.settings_dict["SSS2 Product Code"] = self.sss2_product_code_text.get()
#         self.settings_dict["Software ID"] = self.sss_software_id_text.get()
#         self.settings_dict["SSS2 Cable"] = self.sss2_cable_text.get()
#         self.settings_dict["Resistor Box Used"] = self.resisor_box_button_text.get()
#         self.settings_dict["Saved Date"] = self.saved_date_text.get()
#         self.settings_dict["Serial Number"] = self.sss2_serial_number.get() 
#         self.settings_dict["Vehicle VIN"] = self.vehicle_vin_text.get().strip()
#         self.settings_dict["ECU Component ID"] = self.ecu_component_id_text.get()
#         self.settings_dict["Original Creation Date"]=self.current_date_text.get()
#         self.settings_dict["Programmed By"] = self.user_name_text.get()
#         self.settings_dict["Company"] = self.company_name_text.get()
#         self.settings_dict["Location"] = self.location_name_text.get()
#         self.settings_dict["Case Number"] = self.case_number_text.get()
#         self.settings_dict["Date of Loss"] = self.date_of_loss_text.get()
#         self.settings_dict["User Notes"] = self.case_notes.get(1.0,tk.END).strip()
#         try:
#             self.settings_dict["File Name"] = os.path.basename(self.filename)
#         except:
#             pass

#         self.settings_dict["CAN Config"]["CAN0 Baudrate"] = self.j1939_baud.get()
#         self.settings_dict["CAN Config"]["CAN1 Baudrate"] = self.can2_baud.get()
#         self.settings_dict["CAN Config"]["MCPCAN Baudrate"] = self.can1_baud.get()

#         self.settings_dict["SSS2 Interface Release Date"] = self.release_date
#         self.settings_dict["SSS2 Interface Version"] = self.release_version

        
        
#     def get_all_children(self,tree, item=""):
#         children = tree.get_children(item)
#         for child in children:
#             children += self.get_all_children(tree, child)
#         return children
#     def send_transmit_can(self):
#         commandString = "STARTCAN,"
#         for tree_item in self.get_all_children(self.can_tree):
#             self.can_tree.set(tree_item,"Send","Yes")
            
#         self.tx_queue.put_nowait(commandString)
        
#     def send_stop_can(self):
#         commandString = "STOPCAN,"
#         for tree_item in self.get_all_children(self.can_tree):
#             self.can_tree.set(tree_item,"Send","No")
#             self.can_tree.selection_set(tree_item)
#         self.tx_queue.put_nowait(commandString)         

#     def send_clear_can(self):
        
#         for tree_item in self.can_tree.get_children():
#             self.can_tree.delete(tree_item)   
#         self.tx_queue.put_nowait("CLEARCAN,")

#     def send_reload_can(self):
#         msg_index=0
#         for msgKey in self.settings_dict["CAN"]:
#             self.load_can_frame(self.settings_dict["CAN"][msgKey])
#             time.sleep(0.002)
#             msg_index+=1
#         self.tx_queue.put_nowait("RELOAD,")

#     def send_j1939_baud(self):
#         commandString = "B0,{}".format(self.j1939_baud_value.get())
#         self.tx_queue.put_nowait(commandString)
        
#     def send_can2_baud(self):
#         self.tx_queue.put_nowait("B1,{}".format(self.can2_baud_value.get()))

#     def send_can1_baud(self):
#         self.tx_queue.put_nowait("BMCP,{}".format(self.can1_baud_value.get()))
        
#     def vehicle_networks_settings(self):

#         self.truck_networks_tab.grid_rowconfigure(5,weight=2) #Expands blank space under radio buttons.
#         self.truck_networks_tab.grid_columnconfigure(3,weight=1) #Expands blank space 
#         self.truck_networks_tab.grid_columnconfigure(4,weight=2) #Expands blank space 


#         ttk.Button(self.truck_networks_tab,
#                                     text="Transmit all CAN messages", width = 35,
#                                     command=self.send_transmit_can).grid(row=0,
#                                                                          column=1,
#                                                                          sticky="W",columnspan=3,
#                                                                          pady=5,padx=5)
        
#         ttk.Button(self.truck_networks_tab, width = 35,
#                                     text="Stop Sending all CAN messages",
#                                     command=self.send_stop_can).grid(row=1,
#                                                                      column=1,
#                                                                      sticky="W",columnspan=3,
#                                                                      pady=5,padx=5)
        
#         tk.Label(self.truck_networks_tab,text="J1939 Bit Rate:").grid(row=2,column=1,sticky="E")
        
#         self.j1939_baud = ttk.Combobox(self.truck_networks_tab,
#                                    textvariable=self.j1939_baud_value,
#                                    width=8,
#                                    values=self.baudrates)
#         self.j1939_baud.set(self.settings_dict["CAN Config"]["CAN0 Baudrate"])
#         self.j1939_baud.grid(row=2,column=2,sticky="W",pady=5,columnspan=1)
#         ttk.Button(self.truck_networks_tab, width = 9,
#                                     text="Set",command=self.send_j1939_baud).grid(row=2,
#                                                                      column=3,
#                                                                      sticky="W",columnspan=1,
#                                                                      pady=5,padx=5)
#         self.send_j1939_baud()
        

#         tk.Label(self.truck_networks_tab,text="CAN1 Bit Rate:").grid(row=3,column=1,sticky="E")
        
#         self.can1_baud = ttk.Combobox(self.truck_networks_tab,
#                                    textvariable=self.can1_baud_value,
#                                    width=8,
#                                    values=self.baudrates)
#         self.can1_baud.set(self.settings_dict["CAN Config"]["MCPCAN Baudrate"])
#         self.can1_baud.grid(row=3,column=2,sticky="W",pady=5,columnspan=1)
#         ttk.Button(self.truck_networks_tab, width = 9,
#                                     text="Set",command=self.send_can1_baud).grid(row=3,
#                                                                      column=3,
#                                                                      sticky="W",columnspan=1,
#                                                                      pady=5,padx=5)
#         self.send_can1_baud()

#         tk.Label(self.truck_networks_tab,text="CAN2 Bit Rate:").grid(row=4,column=1,sticky="E")
        
#         self.can2_baud = ttk.Combobox(self.truck_networks_tab,
#                                    textvariable=self.can2_baud_value,
#                                    width=8,
#                                    values=self.baudrates)
#         self.can2_baud.set(self.settings_dict["CAN Config"]["CAN1 Baudrate"])
#         self.can2_baud.grid(row=4,column=2,sticky="W",pady=5,columnspan=1)
#         ttk.Button(self.truck_networks_tab, width = 9,
#                                     text="Set",command=self.send_can2_baud).grid(row=4,
#                                                                      column=3,
#                                                                      sticky="W",columnspan=1,
#                                                                      pady=5,padx=5)
#         self.send_can2_baud()
        
#         logo_file = tk.PhotoImage(file="SynerconLogoWithName300.gif")
#         logo = tk.Label(self.truck_networks_tab,image=logo_file)
#         logo.image= logo_file
#         logo.grid(row=0,column=4,sticky=tk.E,rowspan=5)
        
#         self.can_edit_frame = tk.LabelFrame(self.truck_networks_tab, name="edit_can",text="CAN Message Editor")
#         self.can_edit_frame.grid(row=5,column=1,sticky="EW",columnspan=4,rowspan=1)
        
#         tk.Label(self.can_edit_frame,text="Description:").grid(row=0,column=0,sticky="E")
#         self.can_name_value = tk.StringVar()
#         self.can_name = ttk.Entry(self.can_edit_frame,textvariable=self.can_name_value,width=65)
#         self.can_name.grid(row=0,column=1,sticky="W",columnspan=6,pady=5)
#         self.can_name.configure(state = 'disabled')
        

#         tk.Label(self.can_edit_frame,text="Thread:").grid(row=1,column=0,sticky="E")
#         self.can_thread_value=tk.StringVar()
#         self.can_thread = ttk.Label(self.can_edit_frame,textvariable=self.can_thread_value,width=10)
#         self.can_thread.grid(row=1,column=1,sticky="W",pady=5,columnspan=1)

#         tk.Label(self.can_edit_frame,text="Sequence Count:").grid(row=1,column=2,sticky="E")
#         self.can_count_value=tk.StringVar(value="1")
#         self.can_count = ttk.Label(self.can_edit_frame,textvariable=self.can_count_value,width=10)
#         self.can_count.grid(row=1,column=3,sticky="W",pady=5,columnspan=1)

#         tk.Label(self.can_edit_frame,text="Sequence Index:").grid(row=1,column=4,sticky="E")
#         self.can_sub_value=tk.StringVar(value = "0")
#         self.can_sub = tk.Label(self.can_edit_frame,textvariable=self.can_sub_value,width=10)
#         self.can_sub.grid(row=1,column=5,sticky="W",pady=5,columnspan=1)

        
#         tk.Label(self.can_edit_frame,text="Hex CAN ID:").grid(row=2,column=0,sticky="E")
#         self.can_id_value=tk.StringVar()
#         self.can_id = tk.Entry(self.can_edit_frame,textvariable=self.can_id_value,width=12)
#         self.can_id.grid(row=2,column=1,sticky="W",pady=5,columnspan=2)
#         self.can_id.bind('<Return>',self.modify_can_message)
#         self.can_id.bind('<Tab>',self.modify_can_message)
        


#         tk.Label(self.can_edit_frame,text="DLC:").grid(row=2,column=2,sticky="E")
#         self.can_dlc_value=tk.StringVar(value="8")
#         spinbox_values = ["1","2","3","4","5","6","7","8"]
#         self.can_dlc = ttk.Combobox(self.can_edit_frame,textvariable=self.can_dlc_value,width=2,values=spinbox_values)
#         self.can_dlc.grid(row=2,column=3,sticky="W",pady=5,columnspan=1)
#         self.can_dlc.bind('<<ComboboxSelected>>',self.modify_can_message)
#         self.can_dlc.bind('<Return>',self.modify_can_message)
#         self.can_dlc.bind('<Tab>',self.modify_can_message)
        

        
#         self.can_ext_id_state = tk.IntVar(value=1)
#         self.can_ext_id = ttk.Checkbutton(self.can_edit_frame,text="Use Extended (29-bit) ID",
#                                           variable=self.can_ext_id_state,
#                                           command=self.modify_can_message)
#         self.can_ext_id.grid(row=2,column=4,sticky="W",padx=10,columnspan=3)
        
#         tk.Label(self.can_edit_frame,text="Channel:").grid(row=3,column=0,sticky="E")
#         self.can_radio_frame = tk.Frame(self.can_edit_frame)
#         self.can_radio_frame.grid(row=3,column=1,sticky="W",columnspan=2,pady=5)
#         self.can_channel_value = tk.StringVar(value="0")
#         self.can_channel_0 = ttk.Radiobutton(self.can_radio_frame,value="0",text="J1939",variable=self.can_channel_value,
#                                         command=self.modify_can_message)
#         self.can_channel_0.grid(row=0,column=0,sticky="E")
#         self.can_channel_0 = ttk.Radiobutton(self.can_radio_frame,value="2",text="CAN1",variable=self.can_channel_value,
#                                         command=self.modify_can_message)
#         self.can_channel_0.grid(row=0,column=1,sticky="W")
#         self.can_channel_0 = ttk.Radiobutton(self.can_radio_frame,value="1",text="CAN2",variable=self.can_channel_value,
#                                         command=self.modify_can_message)
#         self.can_channel_0.grid(row=0,column=2,sticky="W")
        
#         self.can_send_state = tk.IntVar(value=1)
#         self.can_send = ttk.Checkbutton(self.can_edit_frame,
#                                         text="Enable Transmission (Send)",
#                                         variable=self.can_send_state,
#                                         command=self.modify_can_message)
#         self.can_send.grid(row=3,column=4,sticky="W",padx=10,columnspan=3)
        
#         tk.Label(self.can_edit_frame,text="Period (msec):").grid(row=4,column=0,sticky="E")
#         self.can_period_value = tk.StringVar(value="100")
#         self.can_period = tk.Entry(self.can_edit_frame,textvariable=self.can_period_value,width=10)
#         self.can_period.grid(row=4,column=1,sticky="W",pady=5)
#         self.can_period.bind('<Return>',self.modify_can_message)
#         self.can_period.bind('<Tab>',self.modify_can_message)
        


#         tk.Label(self.can_edit_frame,text="  Restart (msec):").grid(row=4,column=2,sticky="E")
#         self.can_restart_value = tk.StringVar(value="0")
#         self.can_restart = tk.Entry(self.can_edit_frame,textvariable=self.can_restart_value,width=10)
#         self.can_restart.grid(row=4,column=3,sticky="W",pady=5)
#         self.can_restart.bind('<Return>',self.modify_can_message)
#         self.can_restart.bind('<Tab>',self.modify_can_message)
        

#         tk.Label(self.can_edit_frame,text="Total to Send:").grid(row=4,column=4,sticky="E")
#         self.can_total_value = tk.StringVar(value="0")
#         self.can_total = tk.Entry(self.can_edit_frame,textvariable=self.can_total_value,width=10)
#         self.can_total.grid(row=4,column=5,sticky="W")
#         self.can_total.bind('<Return>',self.modify_can_message)
#         self.can_total.bind('<Tab>',self.modify_can_message)
        
#         self.can_data_frame = tk.Frame(self.can_edit_frame)
#         self.can_byte_value=[]
#         self.can_byte=[]
#         for byteLabel in range(8):
#             tk.Label(self.can_data_frame,text=" B{}:".format(byteLabel+1)).grid(row=0,column=2*byteLabel)
#             self.can_byte_value.append(tk.StringVar(value="00"))
#             self.can_byte.append(tk.Entry(self.can_data_frame,textvariable=self.can_byte_value[byteLabel],width=3))
#             self.can_byte[byteLabel].grid(row=0,column=2*byteLabel+1,pady=5)
#             self.can_byte[-1].bind('<Return>',self.modify_can_message)
#             self.can_byte[-1].bind('<Tab>',self.modify_can_message)
#         self.can_data_frame.grid(row=5,column=1,columnspan=6,sticky="W")
#         tk.Label(self.can_edit_frame,text="Data Bytes (Hex):").grid(row=5,column=0,sticky="W")

#         self.modify_can_button = ttk.Button(self.can_edit_frame, width = 35,
#                                     text="Modify Selected Message",
#                                     command=self.modify_can_message)
#         self.modify_can_button.grid(row=6,columnspan=3,column=0,sticky="W",
#                                                                      pady=5,padx=5)
#         ttk.Button(self.can_edit_frame, width = 35,
#                                     text="Create New CAN Message",
#                                     command=self.create_new_message).grid(row=6,columnspan=3,
#                                                                      column=3,
#                                                                      sticky="E",
#                                                                      pady=5,padx=5)

#         self.send_can_button = ttk.Button(self.can_edit_frame, width = 35,
#                                     text="Send Selected Message",
#                                     command=self.send_single_frame)
#         self.send_can_button.grid(row=7,columnspan=3,column=0,sticky="W",pady=5,padx=5)

#         self.delete_can_button = ttk.Button(self.can_edit_frame, width = 35,
#                                     text="Delete Selected Message",
#                                     command=self.delete_can_message)
#         self.delete_can_button.grid(row=7,columnspan=3,column=3,sticky="E",pady=5,padx=5)

#         self.add_sequence_button = ttk.Button(self.can_edit_frame, width = 35,
#                                     text="Add Sequential Message",
#                                     command=self.add_sequential_message)
#         self.add_sequence_button.grid(row=8,columnspan=3,column=0,sticky="W",pady=5,padx=5)

    
#         self.can0_frame = tk.LabelFrame(self.truck_networks_tab, name="can0 Messages",text="CAN Messages to Transmit")
#         ttk.Sizegrip(self.can0_frame)
                                                  
#         self.can0_frame.grid(row=0,column=0,sticky="NW",columnspan=1,rowspan=7)

#         colWidths = [50,50,50,50,55,50,50,50,30,75,35,24,24,24,24,24,24,24,24]
#         self.colNames = ["Thread","Count","Index","Send","Channel","Period","Restart","Total","Ext","CAN HEX ID","DLC","B1","B2","B3","B4","B5","B6","B7","B8"]
#         colPos = ['center','center','center','center','center',tk.E,tk.E,tk.E,'center',tk.E,'center','center','center','center',
#                   'center','center','center','center','center','center']
#         self.display_cols = ["Send","Channel","Period","Restart","Total","Ext","CAN HEX ID","DLC","B1","B2","B3","B4","B5","B6","B7","B8"]
#         self.can_tree = ttk.Treeview(self.can0_frame, selectmode = "browse",
#                                      displaycolumns="#all",columns = self.colNames,height=31)
        
#         self.can_tree.grid(row=0,column=0)

#         self.can_tree.heading("#0", anchor = tk.W, text = "Label")
#         for c,w,p in zip(self.colNames,colWidths,colPos):
#             self.can_tree.column(c, anchor = p, stretch = False, width = w)
#             self.can_tree.heading(c, anchor = p, text = c)
#         self.item_identifier={}

#         for i in self.can_tree.get_children():
#             self.can_tree.delete(i)
#         self.new_message = True
#         for msg_index in sorted(self.settings_dict["CAN"].keys()):
#             self.load_can_frame(self.settings_dict["CAN"][msg_index])
#             time.sleep(0.005)

            
        
#         self.can_tree.bind('<<TreeviewSelect>>',self.fill_can_box)

            
#         self.message_config_frame = tk.LabelFrame(self.truck_networks_tab, name="network Configurations",
#                                                   text="Network Configurations")
#         self.message_config_frame.grid(row=6,column=1,sticky="EW",columnspan=4)

#         self.lin_to_shield_switch = config_switches(self.message_config_frame,self.tx_queue,
#                             self.settings_dict["Switches"],"LIN to SHLD",row=1,col=0)
#         self.lin_to_port_16 = config_switches(self.message_config_frame,self.tx_queue,
#                             self.settings_dict["Switches"],"LIN to Port 16",row=2,col=0)
#         self.lin_to_master = config_switches(self.message_config_frame,self.tx_queue,
#                             self.settings_dict["Switches"],"LIN Master Pullup Resistor",row=3,col=0)
#         self.can0_term = config_switches(self.message_config_frame,self.tx_queue,
#                             self.settings_dict["Switches"],"CAN0",row=4,col=0)
#         self.can1_term = config_switches(self.message_config_frame,self.tx_queue,
#                             self.settings_dict["Switches"],"CAN1",row=6,col=0)
#         self.can2_term = config_switches(self.message_config_frame,self.tx_queue,
#                             self.settings_dict["Switches"],"CAN2",row=5,col=0)
#         self.j1708_switch = config_radio_switches(self.message_config_frame,self.tx_queue,
#                             self.settings_dict["Switches"],"CAN1 or J1708",rowA=7,colA=0,rowB=8,colB=0)

#     def modify_can_message(self,event=None):
#         self.new_message=False
#         can_thread = self.can_thread_value.get()
#         selection = self.can_tree.selection()
#         self.common_can_message(can_thread)
#         self.sync_tables()
        
#     def delete_can_message(self):
#         selection = self.can_tree.selection()
#         can_msg = self.can_tree.item(selection)
#         index = self.can_thread_value.get()
#         sub = self.can_sub_value.get()
#         commandString = "GO,{},0".format(index) 
#         self.tx_queue.put_nowait(commandString)
#         del self.settings_dict["CAN"]["{:>3d}.{:03d}".format(int(index),int(sub))] 
#         for tree_item in self.can_tree.get_children(selection):
#             self.can_tree.delete(tree_item)
#         prev_selection = self.can_tree.prev(selection)
#         self.can_tree.delete(selection)
#         self.can_tree.selection_set(prev_selection)

#     def add_sequential_message(self):
#         self.new_message = True
#         selection = self.can_tree.selection()
#         if self.can_tree.parent(selection) is not "":
#             while self.can_tree.next(selection) is not "":
#                 selection = self.can_tree.next(selection)
#         self.can_tree.selection_set(selection)
#         self.can_count_value.set("{}".format( self.get_max_count(selection) + 1 ))
#         self.can_sub_value.set("{}".format( self.get_max_count(selection) ))
#         can_thread = int(self.can_thread_value.get())
#         self.common_can_message(str(can_thread))
#         self.sync_tables()
        
#     def sync_tables(self):
#         selection = self.can_tree.selection()
#         while self.can_tree.parent(selection) is not "":
#             selection = self.can_tree.parent(selection)
#         tree_item = selection
        
#         self.can_tree.set(tree_item,"Count",str(self.can_count_value.get()))
#         if self.can_send_state.get() == 1:
#             state = "Yes"
#         else:
#             state = "No"
#         self.can_tree.set(tree_item,"Send",state)
#         if self.can_channel_value.get() == "0":
#             chan = "J1939"
#         elif self.can_channel_value.get() == "2":
#             chan = "CAN1"
#         elif self.can_channel_value.get() == "1":
#             chan = "CAN2"
        
#         self.can_tree.set(tree_item,"Channel",chan)
#         self.can_tree.set(tree_item,"Period",self.can_period_value.get())
#         self.can_tree.set(tree_item,"Restart",self.can_restart_value.get())
#         self.can_tree.set(tree_item,"Total",self.can_total_value.get())
#         for tree_item in self.can_tree.get_children(selection):
#             self.can_tree.set(tree_item,"Count",str(self.can_count_value.get()))
#             if self.can_send_state.get() == 1:
#                 state = "Yes"
#             else:
#                 state = "No"
#             self.can_tree.set(tree_item,"Send",state)
#             if self.can_channel_value.get() == "0":
#                 chan = "J1939"
#             elif self.can_channel_value.get() == "2":
#                 chan = "CAN1"
#             elif self.can_channel_value.get() == "1":
#                 chan = "CAN2"
#             self.can_tree.set(tree_item,"Channel",chan)
#             self.can_tree.set(tree_item,"Period",self.can_period_value.get())
#             self.can_tree.set(tree_item,"Restart",self.can_restart_value.get())
#             self.can_tree.set(tree_item,"Total",self.can_total_value.get())
#             self.can_tree.set(tree_item,"DLC",self.can_dlc_value.get())
            
                     
#     def create_new_message(self):
#         new_name = simpledialog.askstring("Input", "New CAN Message Name:",parent=self, initialvalue="CAN Message")
#         if new_name is None:
#             return
#         self.new_message = True
#         self.can_name.configure(state = 'normal')
#         self.can_name_value.set(new_name)
#         self.can_name.configure(state = 'disabled')
#         selection = self.can_tree.selection()
#         can_thread_list=[]
#         for selection in self.can_tree.get_children(""):
#             can_msg = self.can_tree.item(selection)
#             vals = can_msg['values']
#             can_thread_list.append(vals[0])
#         can_thread = self.get_max_threads() + 1
#         self.can_sub_value.set("0")
#         self.can_count_value.set("1")
#         if can_thread < 1024:
#             #self.create_can_message = False
#             self.common_can_message(str(can_thread))
            
       
#         else:
#             logger.debug("Too many CAN threads for SSS2. Please redo the CAN messages.")

#     def get_max_threads(self):
#         can_thread_list=[]
#         for selection in self.get_all_children(self.can_tree):
#             can_msg = self.can_tree.item(selection)
#             vals = can_msg['values']
#             can_thread_list.append(vals[0])
#         return  max(can_thread_list)

#     def get_max_count(self,item):
#         can_thread_list=[]
#         can_msg = self.can_tree.item(item)
#         vals = can_msg['values']
#         can_thread_list.append(vals[1])
#         for selection in self.can_tree.get_children(item):
#             can_msg = self.can_tree.item(selection)
#             vals = can_msg['values']
#             can_thread_list.append(vals[1])
#         return max(can_thread_list)
        
#     def common_can_message(self,can_thread):
#         #new_thread = from serial len(self.settings_dict["CAN"]["Load Preprogrammed"])
#         selection = self.can_tree.selection()
#         can_msg = self.can_tree.item(selection)
#         m = ""
#         m += self.can_name_value.get()
#         m += ","
#         m += can_thread 
#         m += ","
#         m += self.can_count_value.get()
#         m += ","
#         m += self.can_sub_value.get()
#         m += ","
#         m += self.can_channel_value.get()
#         try:
#             m += ",{},".format(abs(int(self.can_period_value.get())))
#             self.can_period['bg']='white'
#         except Exception as e:
#             logger.debug(e)
#             self.root.bell()
#             self.can_period.focus()
#             self.can_period['bg']='yellow'
#             return
        
#         try:
#             m += "{},".format(abs(int(self.can_restart_value.get())))
#             self.can_restart['bg']='white'
#         except Exception as e:
#             logger.debug(e)
#             self.root.bell()
#             self.can_restart.focus()
#             self.can_restart['bg']='yellow'
#             return

#         try:
#             m += "{},".format(abs(int(self.can_total_value.get())))
#             self.can_total['bg']='white'
#         except Exception as e:
#             logger.debug(e)
#             self.root.bell()
#             self.can_total.focus()
#             self.can_total['bg']='yellow'
#             return
        
#         m += str(self.can_ext_id_state.get())
#         m += ","
#         try:
#             if self.can_ext_id_state.get() == 1:
#                 m += "{:>8X},".format(int(self.can_id_value.get(),16) & 0x1FFFFFFF)
#             else:
#                 m += "{:>3X},".format(int(self.can_id_value.get(),16) & 0x7FF)
#             self.can_id['bg']='white'
#         except Exception as e:
#             logger.debug(e)
#             self.root.bell()
#             self.can_id.focus()
#             self.can_id['bg']='yellow'
#             return
        
#         try:
#             m += "{},".format(abs(int(self.can_dlc_value.get()) & 0x0F))
#             self.can_dlc['background']='white'
#         except Exception as e:
#             logger.debug(e)
#             self.root.bell()
#             self.can_dlc.focus()
#             self.can_dlc['background']='yellow'
#             return

#         for i in range(8):
#             try:
#                 byte_char = "{:02X},".format(abs(int(self.can_byte_value[i].get(),16) & 0xFF))
#                 m += byte_char
#                 self.can_byte_value[i].set(byte_char)
#                 self.can_byte[i]['bg']='white'
#             except Exception as e:
#                 logger.debug(e)
#                 self.root.bell()
#                 self.can_byte[i].focus()
#                 self.can_byte[i]['bg']='yellow'
#                 return
        
#         if self.can_send_state.get() == 1:
#             m += "Yes"
#         else:
#             m += "No"
        
#         self.load_can_frame(m)
        
#     def send_single_frame(self,event=None):
#         commandString = "GO,{},{}".format(self.can_thread_value.get(),self.can_send_state.get()) 
#         self.tx_queue.put_nowait(commandString)

#     def fill_can_box(self,event=None):
#         selection = self.can_tree.selection()
#         can_msg = self.can_tree.item(selection)
#         vals = can_msg['values']
#         if len(vals)==19:
#             self.can_thread_value.set(vals[0])
#             self.can_count_value.set(vals[1])
#             self.can_sub_value.set(vals[2])
#             self.can_name.configure(state = 'normal')
#             self.can_name_value.set(can_msg['text'])
#             self.can_name.configure(state = 'disabled')
#             self.can_id_value.set(vals[9])
#             self.can_dlc_value.set(vals[10])
#             self.can_ext_id_state.set(vals[8])
#             if vals[3]=="Yes":
#                 self.can_send_state.set(1)
#             else:
#                 self.can_send_state.set(0)
#             if vals[4] == "CAN1":
#                 self.can_channel_value.set("2")
#             elif vals[4] == "CAN2":
#                 self.can_channel_value.set("1")
#             else:
#                 self.can_channel_value.set("0")
#             self.can_period_value.set(vals[5])
#             self.can_restart_value.set(vals[6])
#             self.can_total_value.set(vals[7])
#             for i in range(8):
#                 self.can_byte_value[i].set(vals[11+i])
#             self.modify_can_button.configure(state=tk.NORMAL)
#         else:
#             self.modify_can_button.configure(state=tk.DISABLED)

#     def load_can_frame(self,message_string):
        
#         msg = message_string.split(',')
#         msgKey = msg[0].strip()
#         index = msg[1].strip()
        
#         num = msg[2].strip()
#         sub = msg[3].strip()

#         #Switch CAN 1 and 2 becuse they are switched on the Arduino
#         if msg[4] == "0":
#             channel = "J1939"
#         elif msg[4] == "2":
#             channel = "CAN1"
#         elif msg[4] == "1": 
#             channel = "CAN2"
#         else:
#             channel = msg[4].strip()
#         period = msg[5].strip()
#         restart = msg[6].strip()
#         total = msg[7].strip()
#         extID = msg[8].strip()
#         IDhex = msg[9].strip()
#         dlc = msg[10].strip()
#         B=[]
        
#         for b in msg[11:19]:
#             B.append ("{:02X}".format(int(b,16)))
#         send = msg[19].strip()

#         if self.new_message:
#             msg_iid = self.find_next_iid()
#             if sub == "0":
#                 selection = self.can_tree.insert("",int(index),iid=msg_iid,text=msgKey,open=True,
#                                                     values=[index,num,"0",send,channel,period, restart,total,extID,IDhex,dlc]+B)    
                
#             else:
#                 self.trunk = self.can_tree.selection()
#                 while self.can_tree.parent(self.trunk) is not "":
#                     self.trunk = self.can_tree.parent(self.trunk)
#                 selection = self.can_tree.insert(self.trunk,int(sub),iid=msg_iid,text=msgKey,open=True,
#                                                 values=[index,num,sub,send,channel,period, restart,total,extID,IDhex,dlc]+B)
#         else:
                
#             selection = self.can_tree.selection()    
#             if self.can_tree.item(selection) is not "":
#                 self.can_tree.set(selection,"Send",send)
#                 self.can_tree.set(selection,"Channel",channel)
#                 self.can_tree.set(selection,"Period",period)
#                 self.can_tree.set(selection,"Restart",restart)
#                 self.can_tree.set(selection,"Total",total)
#                 self.can_tree.set(selection,"Ext",extID)
#                 self.can_tree.set(selection,"CAN HEX ID",IDhex)
#                 self.can_tree.set(selection,"DLC",dlc)
#                 for i in range(8):
#                     self.can_tree.set(selection,"B{}".format(i+1),B[i])
#             try:
#                 selection = int(selection[0])
#             except:
#                 pass

#         self.can_tree.selection_set(selection)
         
         

#         self.can_thread_value.set(index)
#         if send == "Yes":
#             self.can_send_state.set(1)
#         else:
#             self.can_send_state.set(0)
#         self.fill_can_box()

#         self.settings_dict["CAN"]["{:>3d}.{:03d}".format(int(index),int(sub))] = message_string 
#         commandString = "SM,"+message_string
#         self.tx_queue.put_nowait(commandString)   
#         self.send_single_frame()
        
#     def find_next_iid(self):
#         iid_list=[0]
#         for tree_item in self.get_all_children(self.can_tree):
#             #logger.debug(tree_item)
#             try:
#                 iid_list.append(int(tree_item))
#             except:
#                 iid_list.append(0)
        
#         return max(iid_list) + 1
        
#     def voltage_out_settings(self):
       
#         self.DAC_bank = tk.LabelFrame(self.voltage_out_tab, name="dac_bank",
#                                                   text="Voltage Outputs")
#         self.DAC_bank.grid(row=2,column=0,sticky="NW",columnspan=1)
#         self.DAC_bank.grid_rowconfigure(4,weight=2) #Expands blank space under radio buttons.

#         dac_dict=self.settings_dict["DACs"]
#         self.dac_objects={}
#         for key,c,r in zip(sorted(dac_dict.keys()),[0,1,2,3,0,1,2,3],[0,0,0,0,1,1,1,1]):
#             self.dac_objects[key] = DAC7678(self.DAC_bank,self.tx_queue, dac_dict[key], row=r, col=c)
        
#         self.vout2a_switch = config_radio_switches(self.DAC_bank,self.tx_queue,
#                             self.settings_dict["Switches"],"Port 10 or 19",rowA=2,colA=1,rowB=3,colB=1)
#         self.vout2b_switch = config_radio_switches(self.DAC_bank,self.tx_queue,
#                             self.settings_dict["Switches"],"Port 15 or 18",rowA=2,colA=0,rowB=3,colB=0)
        
#         self.hvadjout_bank = tk.LabelFrame(self.extra_tab, name="hvadjout_bank",
#                                                   text="High Current Adjustable Regulator")
#         self.hvadjout_bank.grid(row=2,column=2,sticky="SW",columnspan=1,rowspan=1)
#         self.hvadjout = DAC7678(self.hvadjout_bank,self.tx_queue,
#                                 self.settings_dict["HVAdjOut"],
#                                 row=0,
#                                 col=0,
#                                 software_ID = self.sss_software_id_text)

#         self.extra_tab.grid_rowconfigure(3,weight=2)                                         
#         logo_file = tk.PhotoImage(file="SSS2Pins.gif")
#         logo = tk.Label(self.extra_tab,image=logo_file)
#         logo.image= logo_file
#         logo.grid(row=3,column=2,sticky="SW",columnspan=3,rowspan=1)

#         logo_file = tk.PhotoImage(file="SynerconLogoWithName300.gif")
#         logo = tk.Label(self.extra_tab,image=logo_file)
#         logo.image= logo_file
#         logo.grid(row=0,column=3,sticky=tk.W,columnspan=2,rowspan=2)
        

#         tk.Label(self.voltage_out_tab,text="The following share a common frequency: PWM1 and PWM2,  PWM3 and PWM4, PWM5 and PWM6. Adjusting one in the group will affect the other.").grid(row=1,column=0)
#         self.pwm_bank=tk.LabelFrame(self.voltage_out_tab, name="pwm_bank",
#                                                   text="Pulse Width Modulated (PWM) Outputs")
#         self.pwm_bank.grid(row=0,column=0,sticky="SE",columnspan=1)

#         self.pwm1_switch = config_switches(self.pwm_bank,self.tx_queue,
#                             self.settings_dict["Switches"],"PWM1 Connect",row=1,col=0)
#         self.pwm2_switch = config_switches(self.pwm_bank,self.tx_queue,
#                             self.settings_dict["Switches"],"PWM2 Connect",row=1,col=1)
#         self.pwm3_switch = config_radio_switches(self.pwm_bank,self.tx_queue,
#                             self.settings_dict["Switches"],"PWM3 or 12V",rowA=1,colA=2,rowB=2,colB=2)
        
#         self.pwm4_switch = config_radio_switches(self.pwm_bank,self.tx_queue,
#                             self.settings_dict["Switches"],"PWM4 or Ground",rowA=1,colA=3,rowB=2,colB=3)
#         self.pwm4_28_switch = config_switches(self.pwm_bank,self.tx_queue,
#                             self.settings_dict["Switches"],"PWM4_28 Connect",row=3,col=3)
#         self.pwm5_switch = config_switches(self.pwm_bank,self.tx_queue,
#                             self.settings_dict["Switches"],"PWM5 Connect",row=1,col=4)
#         self.pwm6_switch = config_switches(self.pwm_bank,self.tx_queue,
#                             self.settings_dict["Switches"],"PWM6 Connect",row=1,col=5)
                
#         self.pwm12_switch = config_radio_switches(self.pwm_bank,self.tx_queue,
#                             self.settings_dict["Switches"],"PWMs or CAN2",rowA=2,colA=0,rowB=3,colB=0)
#         self.pwm_objects={}
#         pwm_dict=self.settings_dict["PWMs"]
#         col_index=0
#         for key in sorted(pwm_dict.keys()):
#             self.pwm_objects[key] = pwm_out(self.pwm_bank,self.tx_queue, pwm_dict[key], row=0, col=col_index)
#             col_index+=1
        
        
#     def data_logger(self):


#         self.can1_switch = config_switches(self.data_logger_tab,self.tx_queue,
#                             self.settings_dict["Switches"],"CAN1 Connect",row=2,col=1)
        
#         self.data_logger_tab.grid_columnconfigure(3,weight=2) #Expands blank space 

#         buffer_size_frame = tk.Frame(self.data_logger_tab)
#         tk.Label(buffer_size_frame,text="Buffer Size:").grid(row=0,column=0,sticky=tk.E)
#         self.j1939_size_value = tk.StringVar(value = 1000000)
#         self.j1939_size = tk.Entry(buffer_size_frame,textvariable= self.j1939_size_value, width=10)
#         self.j1939_size.grid(row=0,column=1,sticky=tk.W,padx=5,pady=2)
#         buffer_size_frame.grid(row=0,column=0,sticky=tk.W)
#         warning= tk.Label(self.data_logger_tab,
#                           text= "Caution: Using the datalogger features can set fault codes. CAN messages may be faster than USB and messages may be dropped. ",
#                           background = "yellow",justify=tk.CENTER,relief=tk.RAISED)
#         warning.grid(row=0,column=1,columnspan=2,sticky="EW")
        
#         self.j1939_frame = tk.LabelFrame(self.data_logger_tab, text="J1939 Messages")
#         self.j1939_frame.grid(row=1,column=0,sticky='NSEW')

#         tk.Label(self.j1939_frame,text="J1939 Bit Rate:").grid(row=1,column=0,sticky="E")
#         self.j1939_baud = ttk.Combobox(self.j1939_frame,
#                                    textvariable=self.j1939_baud_value,
#                                    width=8,
#                                    values=self.baudrates)
#         self.j1939_baud.grid(row=1,column=1,sticky="W",pady=5,columnspan=1)
#         ttk.Button(self.j1939_frame, width = 9,
#                                     text="Set",command=self.send_j1939_baud).grid(row=1,
#                                                                      column=2,
#                                                                      sticky="W",columnspan=1,
#                                                                      pady=5,padx=5)
        

#         self.stream_can0_box =  ttk.Checkbutton(self.j1939_frame,
#                                     text="Stream CAN0 (J1939)",
#                                     command=self.send_stream_can0)
#         self.stream_can0_box.grid(row=0,column=0,sticky="W")
#         self.stream_can0_box.state(['!alternate']) #Clears Check Box

#         tk.Button(self.j1939_frame,text="Clear Buffer", command=self.clear_j1939_buffer).grid(row=0,column=1,pady=5,sticky=tk.N+tk.W)
#         tk.Button(self.j1939_frame,text="Save Buffer", command=self.save_j1939_buffer).grid(row=0,column=2,pady=5,sticky=tk.N+tk.W)
#         tk.Button(self.j1939_frame,text="Save Buffer As...", command=self.save_j1939_buffer_as).grid(row=0,column=3,pady=5,sticky=tk.N+tk.W)
    
        
#         colWidths = [60,30,24,24,24,24,24,24,24,24,50]
#         colNames = ["Period","DLC","B0","B1","B2","B3","B4","B5","B6","B7","Count"]
#         colPos = ['center','center','center','center','center','center','center','center','center','center','center']
        
#         self.j1939_tree = ttk.Treeview(self.j1939_frame, selectmode = "browse",columns=colNames, displaycolumns="#all", height=25)
#         self.j1939_tree.heading("#0", anchor = tk.E, text = "CAN ID")
#         self.j1939_tree.column("#0",width=75)
#         for c,w,p in zip(colNames,colWidths,colPos):
#             self.j1939_tree.column(c, anchor = p, stretch = False, width = w)
#             self.j1939_tree.heading(c, anchor = p, text = c)
#         self.j1939_tree.grid(row=2,column=0,columnspan=4)
#         self.j1939_frame.columnconfigure(3, weight=1)
#         self.j1939_frame.rowconfigure(2, weight=1)
        
#         self.j1939_unique_messages = {}
#         self.j1939_prior_messages = {}

#         self.can1_frame = tk.LabelFrame(self.data_logger_tab, text="CAN1 Messages")
#         self.can1_frame.grid(row=1,column=1,sticky='NSEW')

#         tk.Label(self.can1_frame,text="CAN1 Bit Rate:").grid(row=1,column=0,sticky="E")
#         self.can1_baud = ttk.Combobox(self.can1_frame,
#                                    textvariable=self.can1_baud_value,
#                                    width=8,
#                                    values=self.baudrates)
#         self.can1_baud.grid(row=1,column=1,sticky="W",pady=5,columnspan=1)
#         ttk.Button(self.can1_frame, width = 9,
#                                     text="Set",command=self.send_can1_baud).grid(row=1,
#                                                                      column=2,
#                                                                      sticky="W",columnspan=1,
#                                                                      pady=5,padx=5)

#         self.stream_can1_box =  ttk.Checkbutton(self.can1_frame,
#                                     name="stream CAN1 (MCPCAN)",
#                                     text="Stream CAN1 (MCPCAN)",
#                                     command=self.send_stream_can1)
#         self.stream_can1_box.grid(row=0,column=0,sticky="W")
#         self.stream_can1_box.state(['!alternate']) #Clears Check Box

#         tk.Button(self.can1_frame,text="Clear Buffer", command=self.clear_can1_buffer).grid(row=0,column=1,pady=5,sticky=tk.N+tk.W)
#         tk.Button(self.can1_frame,text="Save Buffer", command=self.save_can1_buffer).grid(row=0,column=2,pady=5,sticky=tk.N+tk.W)
#         tk.Button(self.can1_frame,text="Save Buffer As...", command=self.save_can1_buffer_as).grid(row=0,column=3,pady=5,sticky=tk.N+tk.W)
    
#         self.can1_tree = ttk.Treeview(self.can1_frame, selectmode = "browse",columns=colNames, displaycolumns="#all", height=25)
#         self.can1_tree.heading("#0", anchor = tk.E, text = "CAN ID")
#         self.can1_tree.column("#0",width=75)
#         for c,w,p in zip(colNames,colWidths,colPos):
#             self.can1_tree.column(c, anchor = p, stretch = False, width = w)
#             self.can1_tree.heading(c, anchor = p, text = c)
#         self.can1_tree.grid(row=2,column=0,columnspan=4,sticky=tk.S+tk.W)
#         self.can1_frame.columnconfigure(3, weight=1)
#         self.can1_frame.rowconfigure(2, weight=1)
#         self.can1_unique_messages = {}
#         self.can1_prior_messages = {}


#         self.can2_frame = tk.LabelFrame(self.data_logger_tab, text="CAN2 Messages")
#         self.can2_frame.grid(row=1,column=2,sticky='NSEW')

#         tk.Label(self.can2_frame,text="CAN2 Bit Rate:").grid(row=1,column=0,sticky="E")
#         self.can2_baud = ttk.Combobox(self.can2_frame,
#                                    textvariable=self.can2_baud_value,
#                                    width=8,
#                                    values=self.baudrates)
#         self.can2_baud.grid(row=1,column=1,sticky="W",pady=5,columnspan=1)
#         ttk.Button(self.can2_frame, width = 9,
#                                     text="Set",command=self.send_can2_baud).grid(row=1,
#                                                                      column=2,
#                                                                      sticky="W",columnspan=1,
#                                                                      pady=5,padx=5)

#         self.stream_can2_box =  ttk.Checkbutton(self.can2_frame,
#                                     name="stream CAN2 (E-CAN)",
#                                     text="Stream CAN2 (PTCAN)",
#                                     command=self.send_stream_can2)
#         self.stream_can2_box.grid(row=0,column=0,sticky="W")
#         self.stream_can2_box.state(['!alternate']) #Clears Check Box

#         tk.Button(self.can2_frame,text="Clear Buffer", command=self.clear_can2_buffer).grid(row=0,column=1,pady=5,sticky=tk.N+tk.W)
#         tk.Button(self.can2_frame,text="Save Buffer", command=self.save_can2_buffer).grid(row=0,column=2,pady=5,sticky=tk.N+tk.W)
#         tk.Button(self.can2_frame,text="Save Buffer As...", command=self.save_can2_buffer_as).grid(row=0,column=3,pady=5,sticky=tk.N+tk.W)
    
#         self.can2_tree = ttk.Treeview(self.can2_frame, selectmode = "browse",columns=colNames, displaycolumns="#all", height=25)
#         self.can2_tree.heading("#0", anchor = tk.E, text = "CAN ID")
#         self.can2_tree.column("#0",width=75)
#         for c,w,p in zip(colNames,colWidths,colPos):
#             self.can2_tree.column(c, anchor = p, stretch = False, width = w)
#             self.can2_tree.heading(c, anchor = p, text = c)
#         self.can2_tree.grid(row=2,column=0,columnspan=4,sticky=tk.S+tk.W)
#         self.can2_frame.columnconfigure(3, weight=1)
#         self.can2_frame.rowconfigure(2, weight=1)
#         self.can2_unique_messages = {}
#         self.can2_prior_messages = {}

#         self.j1708_frame = tk.LabelFrame(self.extra_tab, text="J1708 Messages")
#         self.j1708_frame.grid(row=0,column=0,sticky='NSEW',rowspan=4)


#         self.stream_j1708_box =  ttk.Checkbutton(self.j1708_frame,
#                                     name='stream_j1708',
#                                     text="Stream J1708",
#                                     command=self.send_stream_j1708)
#         self.stream_j1708_box.grid(row=0,column=0,padx=5,sticky=tk.W,columnspan=2)
#         self.stream_j1708_box.state(['!alternate']) #Clears Check Box

#         tk.Button(self.j1708_frame,text="Clear Buffer", command=self.clear_j1708_buffer).grid(row=1,column=0,pady=5,padx=1,sticky=tk.N+tk.W)
#         tk.Button(self.j1708_frame,text="Save Buffer ", command=self.save_j1708_buffer).grid(row=1,column=1,pady=5,padx=1,sticky=tk.N+tk.W)
#         tk.Button(self.j1708_frame,text="Save Buffer As...", command=self.save_j1708_buffer_as).grid(row=1,column=2,pady=5,padx=1,sticky=tk.N+tk.W)
    

#         self.j1708_tree = ttk.Treeview(self.j1708_frame,  height=27)
#         self.j1708_tree.grid(row=3,column=0,sticky=tk.S+tk.W,columnspan=4)
#         self.j1708_frame.columnconfigure(3, weight=1)
#         self.j1708_frame.rowconfigure(2, weight=1)
        
#         self.j1708_tree.heading("#0", anchor = 'center', text = "J1708 Messages")
#         self.j1708_tree.column("#0",width=350)

        

#         self.lin_frame = tk.LabelFrame(self.extra_tab, text="LIN Messages")
#         self.lin_frame.grid(row=0,column=1,sticky='NSEW',rowspan=4)


#         self.stream_lin_box =  ttk.Checkbutton(self.lin_frame,
#                                     text="Stream LIN",
#                                     command=self.send_stream_lin)
#         self.stream_lin_box.grid(row=0,column=0,padx=5,sticky=tk.W,columnspan=2)
#         self.stream_lin_box.state(['!alternate']) #Clears Check Box

#         self.suppress_lin_box =  ttk.Checkbutton(self.lin_frame,
#                                     text="Enable LIN on SSS2",
#                                     command=self.send_supress_lin)
#         self.suppress_lin_box.grid(row=2,column=0,padx=5,sticky=tk.W,columnspan=2)
#         self.suppress_lin_box.state(['!alternate']) #Clears Check Box
#         self.suppress_lin_box.state(['selected']) 

#         tk.Button(self.lin_frame,text="Clear Buffer", command=self.clear_lin_buffer).grid(row=1,column=0,pady=5,padx=1,sticky=tk.N+tk.W)
#         tk.Button(self.lin_frame,text="Save Buffer ", command=self.save_lin_buffer).grid(row=1,column=1,pady=5,padx=1,sticky=tk.N+tk.W)
#         tk.Button(self.lin_frame,text="Save As...", command=self.save_lin_buffer_as).grid(row=1,column=2,pady=5,padx=1,sticky=tk.N+tk.W)
    

#         self.lin_tree = ttk.Treeview(self.lin_frame,  height=27)
#         self.lin_tree.grid(row=3,column=0,sticky=tk.S+tk.W,columnspan=4)
#         self.lin_frame.columnconfigure(3, weight=1)
#         self.lin_frame.rowconfigure(2, weight=1)
        
#         self.lin_tree.heading("#0", anchor = 'center', text = "LIN Messages")
#         self.lin_tree.column("#0",width=250)

        

        
#     def send_stream_A21(self):
#         if self.stream_A21_box.instate(['selected']):
#             commandString = "AI,1"
#         else:
#             commandString = "AI,0"
#         self.tx_queue.put_nowait(commandString)    

#       

#     def recall_command_down(self,event=None):
#         self.serial_TX_message.delete(0,tk.END)
#         self.serial_TX_message.insert(0,self.sent_serial_messages[self.sent_serial_messages_index])
#         self.sent_serial_messages_index += 1
#         if self.sent_serial_messages_index == len(self.sent_serial_messages):
#             self.sent_serial_messages_index = 0
            
#     def recall_command_up(self,event=None):
#         self.serial_TX_message.delete(0,tk.END)
#         self.serial_TX_message.insert(0,self.sent_serial_messages[self.sent_serial_messages_index])
#         self.sent_serial_messages_index -= 1
#         if self.sent_serial_messages_index < 0:
#             self.sent_serial_messages_index = len(self.sent_serial_messages)-1
            
#     def save_transcript(self):
#         pass
    
#     def settings_monitor_setup(self):
        
        
#         self.settings_frame = tk.LabelFrame(self.monitor_tab, text="SSS2 Settings")
#         self.settings_frame.grid(row=0,column=0,sticky='EW',rowspan=2)

#         tk.Button(self.settings_frame,text="List SSS2 Settings",
#                     command=self.send_list_settings).grid(row=0,column=0,sticky="W",padx=5,pady=5)
#         #tk.Button(self.settings_frame,text="Save Transcript",
#         #            command=self.save_transcript).grid(row=0,column=1,sticky="W",padx=5,pady=5)
        
#         tk.Label(self.settings_frame,text="Command:").grid(row=0,column=2, sticky="E",pady=5)
#         self.serial_TX_message = ttk.Entry(self.settings_frame,width=55)
#         self.serial_TX_message.grid(row=0,column = 3,sticky="EW")
#         self.serial_TX_message.bind('<Return>',self.send_arbitrary_serial_message)
#         self.serial_TX_message.bind('<Up>',self.recall_command_up)
#         self.serial_TX_message.bind('<Down>',self.recall_command_down)
#         self.sent_serial_messages=[]
#         self.sent_serial_messages_index=0
        
#         self.settings_text = tkst.ScrolledText(self.settings_frame,wrap=tk.NONE,width=130,height=35)
#         self.settings_text.grid(row=1,column=0,sticky="NSEW",columnspan=4)
   
#         self.settings_frame.grid_columnconfigure(3, weight=1)

#         self.analog_frame = tk.LabelFrame(self.monitor_tab, text="Analog Voltage Readings")
#         self.analog_frame.grid(row=0,column=3,sticky='NSEW')
#         self.analog_frame.grid_columnconfigure(3, weight=1)
        
#         self.stream_A21_box =  ttk.Checkbutton(self.analog_frame,
#                                     name='stream_A21',
#                                     text="Stream Voltage Readings",
#                                     command=self.send_stream_A21)
#         self.stream_A21_box.grid(row=0,padx=5,column=0,sticky=tk.W,columnspan=3)
#         self.stream_A21_box.state(['!alternate']) #Clears Check Box
        
        
#         tk.Button(self.analog_frame,text="Clear Buffer", command=self.clear_analog_buffer).grid(row=1,column=0,padx=1,sticky=tk.W)
#         tk.Button(self.analog_frame,text="Save Buffer ", command=self.save_analog_buffer).grid(row=1,column=1,pady=5,padx=1,sticky=tk.W)
#         tk.Button(self.analog_frame,text="Save Buffer As...", command=self.save_analog_buffer_as).grid(row=1,column=2,pady=5,padx=1,sticky=tk.W)

        
        
#         colWidths = [65,65,65,65,65,65]
#         #colNames = ["J24:10","J24:9","J24:8","J18:13","J18:14","J24:7"]
#         colNames = ["J24:10","J24:9","J24:8","J18:13"]
#         colPos = ['center','center','center','center','center','center']
#         self.analog_tree = ttk.Treeview(self.analog_frame, columns=colNames, height=20)
#         self.analog_tree.grid(row=4,column=0,sticky=tk.W,columnspan=4)

#         self.analog_tree.heading("#0", anchor = 'center', text = "Time")
#         self.analog_tree.column("#0",width=65)

#         for c,w,p in zip(colNames,colWidths,colPos):
#             self.analog_tree.column(c, anchor = p, stretch = False, width = w)
#             self.analog_tree.heading(c, anchor = p, text = c)

#         self.clear_analog_buffer()

#         self.calibration_frame = tk.LabelFrame(self.monitor_tab, text="Quadratic Voltage Calibrations")
#         self.calibration_frame.grid(row=1,column=3,sticky='NSEW')
#         col=1
#         for name in colNames:
#             tk.Label(self.calibration_frame,text=name).grid(row=0,column=col)
#             col+=1

#         tk.Label(self.calibration_frame,text="a2").grid(row=1,column=0)
#         tk.Label(self.calibration_frame,text="a1").grid(row=2,column=0)
#         tk.Label(self.calibration_frame,text="a0").grid(row=3,column=0)
            
#         self.calibration_variable=[]
#         self.calibration_entries=[]
#         for i in range(len(self.settings_dict["Analog Calibration"])): #Rows
#             self.calibration_variable.append([])
#             self.calibration_entries.append([])
            
#             for j in range(len(self.settings_dict["Analog Calibration"][i])): #Columns
#                 if j==4:
#                     break
#                 self.calibration_variable[i].append(tk.StringVar(value="{}".format(self.settings_dict["Analog Calibration"][i][j])))
#                 self.calibration_entries[i].append(tk.Entry(self.calibration_frame, width=11,textvariable = self.calibration_variable[i][j]))
#                 self.calibration_entries[i][j].grid(row=i+1, column=j+1)
#                 self.calibration_entries[i][j].bind("<Tab>",self.adjust_calibrations)
#                 self.calibration_entries[i][j].bind("<Return>",self.adjust_calibrations)
              
#     def adjust_calibrations(self,event=None):
#         for i in range(len(self.settings_dict["Analog Calibration"])): #Rows
#             for j in range(len(self.settings_dict["Analog Calibration"][i])): #Columns
#                 try:
#                     self.settings_dict["Analog Calibration"][i][j] = float(self.calibration_variable[i][j].get())
#                     self.calibration_entries[i][j]['bg']='white'
#                 except Exception as e:
#                     logger.debug(e)
#                     self.calibration_entries[i][j]['bg']='red'
#                     self.root.bell()
                    
        
#     def connect_to_serial(self,auto=False):
#         if auto:
#             try:
#                 logger.debug("Automatically connecting to SSS2.")
#                 self.connection_status_string.set("SSS2 connecting automatically.")
#                 with open(self.home_directory+"SSS2comPort.txt","r") as comFile:
#                     comport = comFile.readline().strip()
#                 self.serial = serial.Serial(comport,baudrate=4000000,timeout=1,
#                                         parity=serial.PARITY_ODD,write_timeout=1,
#                                         xonxoff=False, rtscts=False, dsrdtr=False)
#             except Exception as e:
#                 logger.debug(e)
#                 connection_dialog = setup_serial_connections(self)
#                 self.serial = connection_dialog.result
#         else:
#             connection_dialog = setup_serial_connections(self)
#             self.serial = connection_dialog.result
            
#         logger.debug("Clearing TX Queue...", end = '')
#         while not self.tx_queue.empty():
#             dummy = self.tx_queue.get()
#         logger.debug("done.")
        
#         logger.debug(self.serial)
#         if self.serial: 
#             if self.serial is not None:
#                 if self.serial.is_open:
#                     logger.debug("SSS2 connected.")
#                     self.thread = SerialThread(self, self.rx_queue)
#                     self.thread.signal = True
#                     self.thread.daemon = True
#                     self.thread.start()
#                     self.TXthread = TXThread(self,self.tx_queue)
#                     self.TXthread.signal = True
#                     self.TXthread.daemon = True
#                     self.TXthread.start()
                    
#                     #self.thread.join()
#                     logger.debug("Started Serial Thread.")
#                     self.init_tabs()
#                     self.check_serial_connection()
#         else:
#             self.throw_serial_error()

#     def throw_serial_error(self):
#         messagebox.showerror("SSS2 Serial Connection Error",
#                               "The SSS2 serial connection is not present on the selected COM port. Please connect the SSS2 to the correct USB to Serial connection. You may have to restart the program and the SSS2 if the connection continues to fail." )                
#         self.connection_status_string.set('USB to Serial Connection Unavailable. Please install drivers and plug in the SSS2.')
#         self.serial_rx_entry['bg']='red'
#         for tbs in range(1,7):
#             self.tabs.tab(tbs, state="disabled")
#         self.ignition_key_button.state(['!selected'])
#         self.ignition_key_button.state(['disabled'])
#         try:
#             self.thread.signal = False
#         except:
#             pass

        

#     def check_serial_connection(self,event = None):
#         if self.thread.signal:
#             sss2_id = self.settings_dict["SSS2 Product Code"].strip()
#             command_string = "OK,{}".format(sss2_id)
#             self.tx_queue.put_nowait(command_string)
#             self.connection_status_string.set('SSS2 Connected on '+self.serial.port)
#             self.serial_rx_entry['bg']='white'
#             for tbs in range(7):
#                 self.tabs.tab(tbs, state="normal")
#             self.ignition_key_button.state(['!disabled'])
#             #self.ignition_key_button.configure(state = "normal")
            

#         else:
#             self.throw_serial_error()
#             # self.file_OK_received.set(False)
#             # self.wait_variable(self.file_OK_received)       
#             # self.file_OK_received.set(False)
#             self.connect_to_serial()
            

#         self.after(3000,self.check_serial_connection)
        
    
#     def send_arbitrary_serial_message(self,event = None):
#         commandString = self.serial_TX_message.get()
#         self.tx_queue.put_nowait(commandString)
#         self.serial_TX_message.delete(0,tk.END)
#         self.sent_serial_messages.append(commandString)
#         self.sent_serial_messages_index=len(self.sent_serial_messages)-1
        
    
            
#     def send_list_settings(self):
#         commandString = "LS,"
#         self.tx_queue.put_nowait(commandString)
        
#     def write_j1708_log_file(self,data_file_name):
#         with open(data_file_name,'w') as f:
#             f.write("Channel,Unix Timestamp,MID,PID,Data,Checksum,OK (Checksum Valid)\n")
#             for line in self.received_j1708_messages:
#                 f.write(",".join(line)+"\n")
#         logger.debug("Saved {}".format(data_file_name))
#         self.file_status_string.set("Saved log file to "+data_file_name)

#     def write_lin_log_file(self,data_file_name):
#         with open(data_file_name,'w') as f:
#             f.write("Timestamp,ID,B0,B1,B2,B3,Checksum,Checksum\n")
#             for line in self.received_lin_messages:
#                 f.write(",".join(line)+"\n")
#         logger.debug("Saved {}".format(data_file_name))
#         self.file_status_string.set("Saved log file to "+data_file_name)

#     def write_analog_log_file(self,data_file_name,message_list):
#         with open(data_file_name,'w') as f:
#             f.write("Analog Input Voltage Readings.\n")
#             f.write("Units for time are seconds.\n")
#             f.write("Units for Ports are Volts.\n")
#             f.write("Voltage Readings on J24:7 require additional interior pins installed on the Teensy 3.6. See the schematics on Github for more details.\n")
#             #f.write("Time,J24:10,J24:9,J24:8,J18:13,J18:14,J24:7\n")
#             f.write("Time,J24:10,J24:9,J24:8,J18:13\n")
#             for line in message_list:
#                 f.write(",".join(line)+"\n")
#         logger.debug("Saved {}".format(data_file_name))
#         self.file_status_string.set("Saved log file to "+data_file_name)
        
#     def write_can_log_file(self,data_file_name,message_list):    
#         with open(data_file_name,'w') as f:
#             f.write("Channel,Unix Timestamp,CAN ID (Hex),EXT,DLC,B1,B2,B3,B4,B5,B6,B7,B8\n")
#             for line in message_list:
#                 f.write(",".join(line)+"\n")
#         logger.debug("Saved {}".format(data_file_name))
#         self.file_status_string.set("Saved log file to "+data_file_name)

#     def save_j1939_buffer_as(self):
#         types = [('Comma Separated Values', '*.csv')]
#         idir = self.home_directory
#         ifile = "SSS2_J1939_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         title='Save J1939 Log File'
#         data_file_name = filedialog.asksaveasfilename( filetypes=types,
#                                            initialdir=idir,
#                                            initialfile=ifile,
#                                            title=title,
#                                            defaultextension=".csv")
#         self.write_can_log_file(data_file_name,self.received_can0_messages)
#         self.clear_j1939_buffer()
        
#     def save_can2_buffer_as(self):
#         types = [('Comma Separated Values', '*.csv')]
#         idir = self.home_directory
#         ifile = "SSS2_CAN2_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         title='Save CAN2 Log File'
#         data_file_name = filedialog.asksaveasfilename( filetypes=types,
#                                            initialdir=idir,
#                                            initialfile=ifile,
#                                            title=title,
#                                            defaultextension=".csv")
        
#         self.write_can_log_file(data_file_name,self.received_can2_messages)
#         self.clear_can2_buffer()

#     def save_can1_buffer_as(self):
#         types = [('Comma Separated Values', '*.csv')]
#         idir = self.home_directory
#         ifile = "SSS2_CAN1_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         title='Save CAN1 Log File'
#         data_file_name = filedialog.asksaveasfilename( filetypes=types,
#                                            initialdir=idir,
#                                            initialfile=ifile,
#                                            title=title,
#                                            defaultextension=".csv")
        
#         self.write_can_log_file(data_file_name,self.received_can1_messages)
#         self.clear_can1_buffer()
        
#     def save_j1708_buffer_as(self):
#         types = [('Comma Separated Values', '*.csv')]
#         idir = self.home_directory
#         ifile = "SSS2_J1708_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         title='Save J1708 Log File'
#         data_file_name = filedialog.asksaveasfilename( filetypes=types,
#                                            initialdir=idir,
#                                            initialfile=ifile,
#                                            title=title,
#                                            defaultextension=".csv")
        
#         self.write_j1708_log_file(data_file_name)
#         self.clear_j1708_buffer()

#     def save_lin_buffer_as(self):
#         types = [('Comma Separated Values', '*.csv')]
#         idir = self.home_directory
#         ifile = "SSS2_LIN_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         title='Save LIN Log File'
#         data_file_name = filedialog.asksaveasfilename( filetypes=types,
#                                            initialdir=idir,
#                                            initialfile=ifile,
#                                            title=title,
#                                            defaultextension=".csv")
        
#         self.write_lin_log_file(data_file_name)
#         self.clear_lin_buffer()
        
#     def save_analog_buffer_as(self):
#         types = [('Comma Separated Values', '*.csv')]
#         idir = self.home_directory
#         ifile = "SSS2_Analog_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         title='Save Analog Voltage Log File'
#         data_file_name = filedialog.asksaveasfilename( filetypes=types,
#                                            initialdir=idir,
#                                            initialfile=ifile,
#                                            title=title,
#                                            defaultextension=".csv")
        
#         self.write_analog_log_file(data_file_name,self.received_analog_messages)
#         self.clear_analog_buffer()
   
#     def save_j1939_buffer(self):
#         if os.path.exists(self.home_directory):
#             data_file_name=self.home_directory + "SSS2_J1939_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         else:
#             self.save_j1939_buffer_as()
#         self.write_can_log_file(data_file_name,self.received_can0_messages)
#         self.clear_j1939_buffer()
        
#     def save_can1_buffer(self):
#         if os.path.exists(self.home_directory):
#             data_file_name=self.home_directory + "SSS2_CAN1_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         else:
#             self.save_can1_buffer_as()
#         self.write_can_log_file(data_file_name,self.received_can1_messages)
#         self.clear_can1_buffer()
#     def save_can2_buffer(self):
#         if os.path.exists(self.home_directory):
#             data_file_name=self.home_directory + "SSS2_CAN2_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         else:
#             self.save_can2_buffer_as()
#         self.write_can_log_file(data_file_name,self.received_can2_messages)
#         self.clear_can2_buffer()
   
#     def save_j1708_buffer(self):
#         if os.path.exists(self.home_directory):
#             data_file_name=self.home_directory + "SSS2_J1708_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         else:
#             self.save_j1708_buffer_as()
#         self.write_j1708_log_file(data_file_name)
#         logger.debug("Saved {}".format(data_file_name))
#         self.file_status_string.set("Saved log file to "+data_file_name)
#         self.clear_j1708_buffer()

#     def save_lin_buffer(self):
#         if os.path.exists(self.home_directory):
#             data_file_name=self.home_directory + "SSS2_LIN_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         else:
#             self.save_lin_buffer_as()
#         self.write_lin_log_file(data_file_name)
#         logger.debug("Saved {}".format(data_file_name))
#         self.file_status_string.set("Saved log file to "+data_file_name)
#         self.clear_lin_buffer()

#     def save_analog_buffer(self):
#         if os.path.exists(self.home_directory):
#             data_file_name=self.home_directory + "SSS2_Analog_Data_Log_{}.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))
#         else:
#             self.save_analog_buffer_as()
#         self.write_analog_log_file(data_file_name,self.received_analog_messages)
#         logger.debug("Saved {}".format(data_file_name))
#         self.file_status_string.set("Saved log file to "+data_file_name)
#         self.clear_analog_buffer()
        
#     def clear_j1939_buffer(self):
#         self.received_can0_messages=[]
#         self.j1939_prior_messages={}
#         self.j1939_unique_messages={}
#         for tree_item in self.j1939_tree.get_children():
#             self.j1939_tree.delete(tree_item)  
#         self.j1939_tree.tag_configure('dataRow',background='white')
        
#     def clear_can1_buffer(self):
#         self.received_can1_messages=[]
#         self.can1_prior_messages={}
#         self.can1_unique_messages={}
#         for tree_item in self.can1_tree.get_children():
#             self.can1_tree.delete(tree_item)  
#         self.can1_tree.tag_configure('dataRow',background='white')
        
#     def clear_can2_buffer(self):
#         self.received_can2_messages=[]
#         self.can2_prior_messages={}
#         self.can2_unique_messages={}
#         for tree_item in self.can2_tree.get_children():
#             self.can2_tree.delete(tree_item)  
#         self.can2_tree.tag_configure('dataRow',background='white')
    
#     def clear_j1708_buffer(self):
#         self.received_j1708_messages=[]
#         for tree_item in self.j1708_tree.get_children():
#             self.j1708_tree.delete(tree_item)  
#         self.j1708_tree.tag_configure('dataRow',background='white')

#     def clear_lin_buffer(self):
#         self.received_lin_messages=[]
#         for tree_item in self.lin_tree.get_children():
#             self.lin_tree.delete(tree_item)  
#         self.lin_tree.tag_configure('dataRow',background='white')

#     def clear_analog_buffer(self):
#         for tree_item in self.analog_tree.get_children():
#             self.analog_tree.delete(tree_item) 
#         self.analog_tree.tag_configure('dataRow',background='white')
#         self.analog_count = 0
        
#     def process_serial(self):
#         try:
#             limit = int(self.j1939_size_value.get())
#             self.j1939_size['bg']='white'
#         except:
#             limit = 100000
#             self.j1939_size['bg']='red'
        
#         while self.rx_queue.qsize():
#                 self.receivetime = time.time()
#                 new_serial_line = self.rx_queue.get_nowait()
#                 if new_serial_line[0:4]==b'CAN0':
#                     CANdata = new_serial_line.decode('ascii',"ignore").strip().split()
                         
#                     if len(self.received_can0_messages) < limit:
#                         try:
#                             self.received_can0_messages.append(CANdata)
#                             if CANdata[2] in self.j1939_prior_messages:
#                                 self.j1939_prior_messages[CANdata[2]]=self.j1939_unique_messages[CANdata[2]]
#                                 self.j1939_unique_messages[CANdata[2]]={"Timestamp":CANdata[1],"DLC":CANdata[4],"data":CANdata[5:],"count":self.j1939_prior_messages[CANdata[2]]["count"]+1}
#                                 period = float(self.j1939_unique_messages[CANdata[2]]["Timestamp"]) - float(self.j1939_prior_messages[CANdata[2]]["Timestamp"])
#                             else:
#                                 self.j1939_prior_messages[CANdata[2]]={"Timestamp":CANdata[1],"DLC":CANdata[4],"data":CANdata[5:13],"count":1}
#                                 self.j1939_unique_messages[CANdata[2]]={"Timestamp":CANdata[1],"DLC":CANdata[4],"data":CANdata[5:13],"count":1}
                                
#                                 period = None
#                             if self.j1939_tree.exists(CANdata[2]):
#                                 self.j1939_tree.set(CANdata[2],"Period","{:5f}".format(period))
#                                 self.j1939_tree.set(CANdata[2],"DLC",CANdata[4])
#                                 self.j1939_tree.set(CANdata[2],"Count",self.j1939_unique_messages[CANdata[2]]["count"])
#                                 for b in range(8):
#                                     self.j1939_tree.set(CANdata[2],"B{}".format(b),CANdata[5+b])
#                             else: 
#                                 self.j1939_tree.insert("",tk.END,iid=CANdata[2],text = CANdata[2],values=[None,CANdata[4]]+CANdata[5:13]+[1],tags=('dataRow',))
#                             self.j1939_tree.see(CANdata[2])
#                             self.j1939_tree.tag_configure('dataRow',background='white')
#                         except Exception as e:
#                             logger.debug(e)
#                             self.j1939_tree.tag_configure('dataRow',background='orange')
#                     else:
#                         self.j1939_tree.tag_configure('dataRow',background='orange')
                            
#                 elif new_serial_line[0:4]==b'CAN1':
#                     CANdata = new_serial_line.decode('ascii',"ignore").strip().split()
#                     if len(self.received_can1_messages) < limit:
#                         try:
#                             self.received_can1_messages.append(CANdata)
#                             if CANdata[2] in self.can1_prior_messages:
#                                 self.can1_prior_messages[CANdata[2]]=self.can1_unique_messages[CANdata[2]]
#                                 self.can1_unique_messages[CANdata[2]]={"Timestamp":CANdata[1],"DLC":CANdata[4],"data":CANdata[5:],"count":self.can1_prior_messages[CANdata[2]]["count"]+1}
#                                 period = float(self.can1_unique_messages[CANdata[2]]["Timestamp"]) - float(self.can1_prior_messages[CANdata[2]]["Timestamp"])
#                             else:
#                                 self.can1_prior_messages[CANdata[2]]={"Timestamp":CANdata[1],"DLC":CANdata[4],"data":CANdata[5:13],"count":1}
#                                 self.can1_unique_messages[CANdata[2]]={"Timestamp":CANdata[1],"DLC":CANdata[4],"data":CANdata[5:13],"count":1}
                                
#                                 period = None
#                             if self.can1_tree.exists(CANdata[2]):
#                                 self.can1_tree.set(CANdata[2],"Period","{:5f}".format(period))
#                                 self.can1_tree.set(CANdata[2],"DLC",CANdata[4])
#                                 self.can1_tree.set(CANdata[2],"Count",self.can1_unique_messages[CANdata[2]]["count"])
#                                 for b in range(8):
#                                     self.can1_tree.set(CANdata[2],"B{}".format(b),CANdata[5+b])
#                             else: 
#                                 self.can1_tree.insert("",tk.END,iid=CANdata[2],text = CANdata[2],values=[None,CANdata[4]]+CANdata[5:13]+[1],tags=('dataRow',))
#                             self.can1_tree.see(CANdata[2])
#                             self.can1_tree.tag_configure('dataRow',background='white')
#                         except Exception as e:
#                             logger.debug(e)
#                             self.can1_tree.tag_configure('dataRow',background='orange')
#                     else:
#                         self.can1_tree.tag_configure('dataRow',background='orange')
                     
#                 elif new_serial_line[0:4]==b'CAN2':
#                     CANdata = new_serial_line.decode('ascii',"ignore").strip().split()
#                     if len(self.received_can2_messages) < limit:
#                         try:
#                             self.received_can2_messages.append(CANdata)
#                             if CANdata[2] in self.can2_prior_messages:
#                                 self.can2_prior_messages[CANdata[2]]=self.can2_unique_messages[CANdata[2]]
#                                 self.can2_unique_messages[CANdata[2]]={"Timestamp":CANdata[1],"DLC":CANdata[4],"data":CANdata[5:],"count":self.can2_prior_messages[CANdata[2]]["count"]+1}
#                                 period = float(self.can2_unique_messages[CANdata[2]]["Timestamp"]) - float(self.can2_prior_messages[CANdata[2]]["Timestamp"])
#                             else:
#                                 self.can2_prior_messages[CANdata[2]]={"Timestamp":CANdata[1],"DLC":CANdata[4],"data":CANdata[5:13],"count":1}
#                                 self.can2_unique_messages[CANdata[2]]={"Timestamp":CANdata[1],"DLC":CANdata[4],"data":CANdata[5:13],"count":1}
                                
#                                 period = None
#                             if self.can2_tree.exists(CANdata[2]):
#                                 self.can2_tree.set(CANdata[2],"Period","{:5f}".format(period))
#                                 self.can2_tree.set(CANdata[2],"DLC",CANdata[4])
#                                 self.can2_tree.set(CANdata[2],"Count",self.can2_unique_messages[CANdata[2]]["count"])
#                                 for b in range(8):
#                                     self.can2_tree.set(CANdata[2],"B{}".format(b),CANdata[5+b])
#                             else: 
#                                 self.can2_tree.insert("",tk.END,iid=CANdata[2],text = CANdata[2],values=[None,CANdata[4]]+CANdata[5:13]+[1],tags=('dataRow',))
#                             self.can2_tree.see(CANdata[2])
#                             self.can2_tree.tag_configure('dataRow',background='white')
#                         except Exception as e:
#                             logger.debug(e)
#                             self.can2_tree.tag_configure('dataRow',background='orange')
#                     else:
#                         self.can2_tree.tag_configure('dataRow',background='orange')
                     
#                 elif new_serial_line[0:3]==b'LIN':
#                     LINdata = new_serial_line.decode('ascii',"ignore").strip().split(',')
#                     self.received_lin_messages.append(LINdata)
#                     latest = self.lin_tree.insert("",tk.END,text = LINdata[1:])
#                     self.lin_tree.see(latest)
#                 elif new_serial_line[0:5]==b'J1708':
#                     J1708Data = new_serial_line.decode('ascii',"ignore").strip().split()
#                     self.received_j1708_messages.append(J1708Data)
#                     latest = self.j1708_tree.insert("",tk.END,text = J1708Data[2:-1])
#                     self.j1708_tree.see(latest)

#                 elif new_serial_line[0:6]==b'ANALOG':
#                     self.analog_count += 1
#                     if self.analog_count < limit:
#                         analog_data = new_serial_line[7:].decode('ascii',"ignore").strip().split()
#                         #logger.debug(analog_data)
#                         analog_time="{:>0.3f}".format(float(analog_data[0])/1000)
#                         analog_list = []
#                         for i in range(len(self.settings_dict["Analog Calibration"][0])):
#                             if i==4:
#                                 break
#                             analog_data.append(0) #makes sure data streams have values
#                             analog_list.append("{:>0.3f}".format(self.settings_dict["Analog Calibration"][0][i]*float(analog_data[i+1])*float(analog_data[i+1])
#                                                            + self.settings_dict["Analog Calibration"][1][i]*float(analog_data[i+1])
#                                                            + self.settings_dict["Analog Calibration"][2][i]))
#                         latest = self.analog_tree.insert("",tk.END,text = analog_time ,values=analog_list,tags=('dataRow',))
#                         self.analog_tree.see(latest)
#                         self.analog_tree.tag_configure('dataRow',background='white')
#                         self.received_analog_messages.append([analog_time]+analog_list[:len(self.settings_dict["Analog Calibration"][0])])
#                     else:
#                         self.analog_tree.tag_configure('dataRow',background='orange')
                   
#                 elif new_serial_line[:16]==b'OK:Authenticated':
#                     self.file_authenticated = True
#                     self.file_OK_received.set(True)
                    
#                 elif new_serial_line[0:9]==b'OK:Denied':
#                     self.file_authenticated = False
#                     self.file_OK_received.set(True)
                    
#                 elif new_serial_line[0:23]==b'INFO SSS2 Component ID:':
#                     temp_data = str(new_serial_line,'utf-8').split(':')
#                     self.sss_component_id_text.set(temp_data[1].strip())
#                 elif new_serial_line[0:8]==b'FIRMWARE':
#                     temp_data = str(new_serial_line,'utf-8').split()
#                     self.sss_software_id_text.set(temp_data[1].strip())
#                 elif new_serial_line[0:4]==b'ID: ':
#                     temp_data = str(new_serial_line[4:],'utf-8').strip()
#                     if self.sss2_product_code_text.get().strip() is not "UNIVERSAL":
#                         self.sss2_product_code_text.set(temp_data)
#                     self.unique_ID = temp_data
#                     self.sss2_product_code['bg']='white'
#                 elif new_serial_line[0:8]==b'SET 50,1':
#                     self.ignition_key_button.state(['selected'])
#                 elif new_serial_line[0:8]==b'SET 50,0':
#                     self.ignition_key_button.state(['!selected'])
#                 elif new_serial_line[0:7]==b'SET 83,': #PWM3
#                     freq = self.pwm_objects["PWM3"].pwm_frequency_value.get()
#                     self.pwm_objects["PWM4"].pwm_frequency_value.delete(0,tk.END)
#                     self.pwm_objects["PWM4"].pwm_frequency_value.insert(0,freq)
#                     self.pwm_objects["PWM4"].pwm_frequency_slider.set(float(freq))
#                 elif new_serial_line[0:7]==b'SET 84,': #PWM4
#                     freq = self.pwm_objects["PWM4"].pwm_frequency_value.get()
#                     self.pwm_objects["PWM3"].pwm_frequency_value.delete(0,tk.END)
#                     self.pwm_objects["PWM3"].pwm_frequency_value.insert(0,freq)
#                     self.pwm_objects["PWM3"].pwm_frequency_slider.set(float(freq))
#                 elif new_serial_line[0:7]==b'SET 81,': #PWM1
#                     freq = self.pwm_objects["PWM1"].pwm_frequency_value.get()
#                     self.pwm_objects["PWM2"].pwm_frequency_value.delete(0,tk.END)
#                     self.pwm_objects["PWM2"].pwm_frequency_value.insert(0,freq)
#                     self.pwm_objects["PWM2"].pwm_frequency_slider.set(float(freq))
#                 elif new_serial_line[0:7]==b'SET 82,': #PWM2
#                     freq = self.pwm_objects["PWM2"].pwm_frequency_value.get()
#                     self.pwm_objects["PWM1"].pwm_frequency_value.delete(0,tk.END)
#                     self.pwm_objects["PWM1"].pwm_frequency_value.insert(0,freq)
#                     self.pwm_objects["PWM1"].pwm_frequency_slider.set(float(freq))
#                 elif new_serial_line[0:7]==b'SET 85,': #PWM5 and 6
#                     self.pwm_objects["PWM6"].pwm_frequency_slider.configure(state='normal')
#                     self.pwm_objects["PWM6"].pwm_frequency_value.configure(state='normal')
#                     freq = self.pwm_objects["PWM5"].pwm_frequency_value.get()
#                     self.pwm_objects["PWM5"].pwm_frequency_value.delete(0,tk.END)
#                     self.pwm_objects["PWM5"].pwm_frequency_value.insert(0,freq)
#                     self.pwm_objects["PWM5"].pwm_frequency_slider.set(float(freq))
#                     self.pwm_objects["PWM6"].pwm_frequency_value.delete(0,tk.END)
#                     self.pwm_objects["PWM6"].pwm_frequency_value.insert(0,freq)
#                     self.pwm_objects["PWM6"].pwm_frequency_slider.set(float(freq))
#                     self.pwm_objects["PWM6"].pwm_frequency_slider.configure(state='disabled')
#                     self.pwm_objects["PWM6"].pwm_frequency_value.configure(state='disabled')
#                 else:
#                     self.file_OK_received.set(True)
#                 if new_serial_line[0:4]!=b'CAN0' and new_serial_line[0:4]!=b'CAN1' and new_serial_line[0:4]!=b'CAN2' and new_serial_line[0:5]!=b'J1708' and new_serial_line[0:6]!=b'ANALOG' and new_serial_line[0:4]!=b'LIN ' and new_serial_line[0:2]!=b'OK':
#                     self.serial_rx_entry.delete(0,tk.END)
#                     self.serial_rx_entry.insert(0, new_serial_line.decode('ascii',"ignore"))
#                     self.settings_text.insert(tk.END,new_serial_line.decode('ascii',"ignore"))
#                     self.settings_text.see(tk.END)
                
#         self.after(10, self.process_serial)
    
#     def potentiometer_settings(self):
#         """Adjusts the potentiometers and other analog outputs"""

#         self.pot_bank={}
#         row_index=0
#         pot_dict=self.settings_dict["Potentiometers"]
#         for bank_key in sorted(pot_dict.keys()):
#             if bank_key == "Others":
#                 self.pot_bank[bank_key] = pot_bank(self.extra_tab,self.tx_queue,pot_dict,bank_key,row=0,col=2,colspan=1)
#             else:
#                 self.pot_bank[bank_key] = pot_bank(self.settings_tab,self.tx_queue,pot_dict,bank_key,row=row_index,col=0,colspan=4)
#             row_index += 1
 
#         self.settings_tab.grid_columnconfigure(0,weight=1)
#         self.settings_tab.grid_columnconfigure(1,weight=1)
#         self.settings_tab.grid_columnconfigure(2,weight=1)
#         self.settings_tab.grid_columnconfigure(3,weight=1)
               
#         self.twelve2_switch = config_switches(self.settings_tab,self.tx_queue,
#                             self.settings_dict["Switches"],"12V Out 2",row=2,col=1)
#         self.ground2_switch = config_switches(self.settings_tab,self.tx_queue,
#                             self.settings_dict["Switches"],"Ground Out 2",row=3,col=1)

                

#     
      

    
# class pot_bank(QWidget):
#     def __init__(self, parent,tx_queue,pot_dict,key, row = 0, col = 0,colspan=3):
#         self.root=parent
#         self.tx_queue = tx_queue
#         self.pot_dict = pot_dict
#         self.bank_key = key
#         self.col=col
#         self.row=row
#         self.colspan=colspan
#         self.setup_pot_bank()
#     def setup_pot_bank(self):
#         #Setup Bank with a common Switch for Terminal A
#         label=self.pot_dict[self.bank_key]["Label"]
#         self.pot_bank = tk.LabelFrame(self.root,name=label.lower(),text=label)
#         self.pot_bank.grid(row=self.row,column=self.col,columnspan=self.colspan,sticky=tk.W)
#         if self.pot_dict[self.bank_key]["Terminal A Connection"] is not None:
#             self.bank_button =  ttk.Checkbutton(self.pot_bank,
#                                                 text="Terminal A Voltage Enabled",
#                                                 name='terminal_A_voltage_connect',
#                                                 command=self.send_bank_term_A_voltage_command)
#             self.bank_button.grid(row=0,column=0,sticky=tk.W)
#             self.bank_button.state(['!alternate']) #Clears Check Box
#             if self.pot_dict[self.bank_key]["Terminal A Connection"]:
#                 self.bank_button.state(['selected'])
#             self.send_bank_term_A_voltage_command() #Call the command once

#         self.pot_pairs={}
#         col_index=0
#         for key in sorted(self.pot_dict[self.bank_key]["Pairs"].keys()):
#             self.pot_pairs[key] = potentiometer_pair(self.pot_bank,self.tx_queue,
#                            self.pot_dict[self.bank_key]["Pairs"],
#                            pair_id=key,col=col_index,row=1)
#             col_index += 1
        
#     def send_bank_term_A_voltage_command(self):
#         state=self.bank_button.instate(['selected'])
#         setting = self.pot_dict[self.bank_key]["SSS2 Setting"]
#         if setting is not None:
#             if state:
#                 commandString = "{:d},1".format(setting)
#             else:
#                 commandString = "{:d},0".format(setting)
#             self.tx_queue.put_nowait(commandString)

            
# class config_switches(QWidget):
#     def __init__(self, parent,tx_queue,switch_dict,key, row = 0, col = 0):
#         self.root=parent
#         self.tx_queue = tx_queue
#         self.switch_button_dict = switch_dict
#         self.key = key
#         self.col=col
#         self.row=row
#         self.setup_switches()

#     def setup_switches(self):
#         self.switch_button =  ttk.Checkbutton(self.root,
#                                             text=self.switch_button_dict[self.key]["Label"],
#                                             command=self.connect_switches)
#         self.switch_button.grid(row=self.row,column=self.col,sticky=tk.W)
#         self.switch_button.state(['!alternate']) #Clears Check Box
#         if self.switch_button_dict[self.key]["State"]:
#             self.switch_button.state(['selected'])
#         else:
#             self.switch_button.state(['!selected'])
#         self.connect_switches()
            
#     def connect_switches(self):
#         state=self.switch_button.instate(['selected'])
#         #self.switch_button_dict[self.key]["State"]=state
#         SSS2_setting = self.switch_button_dict[self.key]["SSS2 setting"]
#         if state:
#             commandString = "{},1".format(SSS2_setting)
#         else:
#             commandString = "{},0".format(SSS2_setting)
#         return self.tx_queue.put_nowait(commandString)

# class config_radio_switches(QWidget):
#     def __init__(self, parent,tx_queue,switch_dict,key, rowA = 0, colA = 0,
#                  rowB = 0, colB = 1, rowspanA=2, rowspanB=2,
#                  colspanA=1, colspanB=1,):
#         self.root=parent
#         self.tx_queue =tx_queue
#         self.switch_button_dict = switch_dict
#         self.key = key
#         self.colA=colA
#         self.rowA=rowA
#         self.colB=colB
#         self.rowB=rowB
#         self.labelA=self.switch_button_dict[self.key]["Label A"]
#         self.nameA=self.labelA.lower()
#         self.labelB=self.switch_button_dict[self.key]["Label B"]
#         self.nameB=self.labelB.lower()
#         self.setup_switches()

#     def setup_switches(self):
#         button_val = tk.StringVar()
        
#         self.switch_buttonA =  ttk.Radiobutton(self.root,
#                                                text=self.labelA,
#                                                value = "A",
#                                                name=self.nameA,
#                                                command=self.connect_switches,
#                                                variable=button_val)
        
#         self.switch_buttonA.grid(row=self.rowA,column=self.colA,sticky=tk.W,columnspan=2)
#         self.switch_buttonA.state(['!alternate']) #Clears Check Box
#         if self.switch_button_dict[self.key]["State"]:
#             self.switch_buttonA.state(['selected'])
#         else:
#             self.switch_buttonA.state(['!selected'])

#         self.switch_buttonB =  ttk.Radiobutton(self.root,
#                                                text=self.labelB,
#                                                value = "B",
#                                                name=self.nameB,
#                                                command=self.connect_switches,
#                                                variable=button_val)
#         self.switch_buttonB.grid(row=self.rowB,column=self.colB,sticky=tk.W,columnspan=2)
#         self.switch_buttonB.state(['!alternate']) #Clears Check Box
#         if not self.switch_button_dict[self.key]["State"]:
#             self.switch_buttonB.state(['selected'])
#         else:
#             self.switch_buttonB.state(['!selected'])

#         self.connect_switches()
            
#     def connect_switches(self):
#         state=self.switch_buttonA.instate(['selected'])
#         #self.switch_button_dict[self.key]["State"]=state
#         SSS2_setting = self.switch_button_dict[self.key]["SSS2 setting"]
#         if state:
#             commandString = "{},1".format(SSS2_setting)
#         else:
#             commandString = "{},0".format(SSS2_setting)
#         return self.tx_queue.put_nowait(commandString)   

  
# class potentiometer_pair(QWidget):
#     def __init__(self, parent,tx_queue,pair_dict,pair_id, row = 0, col = 0):
#         self.root = parent
#         self.tx_queue = tx_queue
#         self.row=row
#         self.col=col
#         self.key=pair_id
#         self.pair_dict=pair_dict[pair_id]
#         self.setup_pot_pair()

#     def setup_pot_pair(self):
#         self.potentiometer_pair = tk.LabelFrame(self.root, name="pot_pair_"+self.key,
#                                                 text=self.pair_dict["Name"])
#         self.potentiometer_pair.grid(row=self.row,column=self.col)
#         if self.pair_dict["Terminal A Voltage"]:
#             self.terminal_A_setting = tk.StringVar()
            
#             self.twelve_volt_switch = ttk.Radiobutton(self.potentiometer_pair, text="+12V", value="+12V",
#                                                 command=self.send_terminal_A_voltage_command,
#                                                       name='button_12',
#                                                       variable = self.terminal_A_setting)
#             self.twelve_volt_switch.grid(row=0,column = 0,sticky=tk.E)
            
            
#             self.five_volt_switch = ttk.Radiobutton(self.potentiometer_pair, text="+5V", value="+5V",
#                                                 command=self.send_terminal_A_voltage_command,
#                                                     name='button_5',
#                                                     variable = self.terminal_A_setting)
#             self.five_volt_switch.grid(row=0,column = 1,sticky=tk.W)
#             if self.pair_dict["Terminal A Voltage"] == "+5V":
#                 self.five_volt_switch.state(['selected'])
#                 self.terminal_A_setting.set("+5V")
#             else:
#                 self.twelve_volt_switch.state(['selected'])
#                 self.terminal_A_setting.set("+12V")
#             self.send_terminal_A_voltage_command() #run once
#         else:
#             self.twelve_volt_switch = None

#         col_count = 0
#         self.pots={}
#         for key in sorted(self.pair_dict["Pots"].keys()):
#             self.pots[key] = potentiometer(self.potentiometer_pair,self.tx_queue, self.pair_dict["Pots"][key], row=1, col=col_count)
#             col_count+=1

#     def send_terminal_A_voltage_command(self):
        
#         new_setting = self.terminal_A_setting.get()
#         if new_setting == "+5V":
#             commandString = "{},0".format(self.pair_dict["SSS Setting"])
#         else:
#             commandString = "{},1".format(self.pair_dict["SSS Setting"])
#         return self.tx_queue.put_nowait(commandString)

# class potentiometer(QWidget):
#     def __init__(self, parent,tx_queue, pot_dict, row = 2, col = 0):
#         self.root = parent
#         self.tx_queue = tx_queue
#         self.pot_row=row
#         self.pot_col=col
#         self.pot_settings_dict = pot_dict
#         self.pot_number=self.pot_settings_dict["SSS2 Wiper Setting"]
#         self.connector=self.pot_settings_dict["Pin"]
#         self.label = self.pot_settings_dict["Name"]+" ("+self.connector+")"
#         self.name = self.pot_settings_dict["Name"].lower()
#         self.tcon_setting = self.pot_settings_dict["SSS2 TCON Setting"]
#         self.setup_potentometer()
      
#     def setup_potentometer(self):        
#         self.potentiometer_frame = tk.LabelFrame(self.root, name=self.name+'_frame',text=self.label)
#         self.potentiometer_frame.grid(row=self.pot_row,column=self.pot_col,sticky=tk.W,padx=5,pady=5)

        

#         self.terminal_A_connect_button =  ttk.Checkbutton(self.potentiometer_frame,
#                                                           text="Terminal A Connected",
#                                                           name="terminal_A_connect",
#                                                           command=self.set_terminals)
#         self.terminal_A_connect_button.grid(row=1,column=1,columnspan=2,sticky=tk.NW)
#         self.terminal_A_connect_button.state(['!alternate']) #Clears Check Box
#         if self.pot_settings_dict["Term. A Connect"]:
#             self.terminal_A_connect_button.state(['selected']) 
        
#         self.wiper_position_slider = tk.Scale(self.potentiometer_frame,
#                                               from_ = 255, to = 0, digits = 1, resolution = 1,
#                                               orient = tk.VERTICAL, length = 100,
#                                               sliderlength = 10, showvalue = 0, 
#                                               label = None,
#                                               name='wiper_position_slider',
#                                               command = self.set_wiper_voltage)
#         self.wiper_position_slider.grid(row=1,column=0,columnspan=1,rowspan=5,sticky="E")
#         self.wiper_position_slider.set(self.pot_settings_dict["Wiper Position"])
        
        
#         tk.Label(self.potentiometer_frame,text="Wiper Position",name="wiper label").grid(row=2,column=1, sticky="SW",columnspan=2)
#         tk.Label(self.potentiometer_frame,text=self.pot_settings_dict["Resistance"],
#                  name="wiper resistance").grid(row=2,column=2, sticky="NE",columnspan=1)
#         self.wiper_position_value = ttk.Entry(self.potentiometer_frame,width=10,name='wiper_position_value')
#         self.wiper_position_value.grid(row=3,column = 1,sticky="E")
#         self.wiper_position_value.bind('<Return>',self.set_wiper_slider)

#         self.wiper_position_button = ttk.Button(self.potentiometer_frame,text="Set Position",
#                                             command = self.set_wiper_slider,name='wiper_position_button')
#         self.wiper_position_button.grid(row=3,column = 2,sticky="W")


       
#         self.wiper_connect_button =  ttk.Checkbutton(self.potentiometer_frame, text="Wiper Connected",
#                                             command=self.set_terminals,name='wiper_connect_checkbutton')
#         self.wiper_connect_button.grid(row=4,column=1,columnspan=2,sticky=tk.NW)
#         self.wiper_connect_button.state(['!alternate']) #Clears Check Box
#         if self.pot_settings_dict["Wiper Connect"]:
#             self.wiper_connect_button.state(['selected']) #checks the Box
        

#         self.terminal_B_connect_button =  ttk.Checkbutton(self.potentiometer_frame,
#                                                           text="Connected to Ground",
#                                                           name="terminal_B_connect",
#                                                           command=self.set_terminals)
#         self.terminal_B_connect_button.grid(row=5,column=1,columnspan=2,sticky=tk.SW)
#         self.terminal_B_connect_button.state(['!alternate']) #Clears Check Box
#         if self.pot_settings_dict["Term. B Connect"]:
#             self.terminal_B_connect_button.state(['selected']) 
        
#         self.set_terminals()
#         self.set_wiper_voltage()

#         self.ecu_app = ecu_application(self.potentiometer_frame,self.pot_settings_dict,row=6,column=0,columnspan=4)
        
#     def set_wiper_slider(self,event=None):
#         try:
#             self.wiper_position_slider.set(self.wiper_position_value.get())
#             self.wiper_position_value['foreground'] = "black"
#         except:
#             self.root.bell()
#             self.wiper_position_value['foreground'] = "red"

#     def set_wiper_voltage(self,event=None):
#         self.wiper_position_value.delete(0,tk.END)
#         self.wiper_position_value.insert(0,self.wiper_position_slider.get())
#         commandString = "{},{}".format(self.pot_number,self.wiper_position_slider.get())
#         self.tx_queue.put_nowait(commandString)
    
#     def set_terminals(self):
#         self.terminal_A_connect_state = self.terminal_A_connect_button.instate(['selected'])
#         self.terminal_B_connect_state = self.terminal_B_connect_button.instate(['selected'])
#         self.wiper_connect_state = self.wiper_connect_button.instate(['selected'])
#         terminal_setting = self.terminal_B_connect_state + 2*self.wiper_connect_state + 4*self.terminal_A_connect_state
#         commandString = "{},{}".format(self.tcon_setting,terminal_setting)
#         self.tx_queue.put_nowait(commandString)
        

# class DAC7678(QWidget):
#     def __init__(self, parent,tx_queue,sss2_settings, row = 2, col = 0, software_ID = ""):
#         self.root = parent
#         self.tx_queue = tx_queue
#         self.sss_software_id_text = software_ID
#         self.row=row
#         self.col=col
#         self.settings_dict = sss2_settings
#         self.connector=self.settings_dict["Pin"]
#         self.label = self.settings_dict["Name"]+" ("+self.connector+")"
#         self.name = self.label.lower()
#         self.setting_num = self.settings_dict["SSS2 setting"]
#         self.setup_dac_widget()
        
#     def setup_dac_widget(self):
         
#         self.dac_frame = tk.LabelFrame(self.root, name=self.name,text=self.label)
#         self.dac_frame.grid(row=self.row,column=self.col,sticky=tk.W,padx=5,pady=5)
#         self.low = float(self.settings_dict["Lowest Voltage"])
#         self.high = float(self.settings_dict["Highest Voltage"])

#         self.dac_mean_slider = tk.Scale(self.dac_frame,
#                                         from_ = self.low*100,
#                                         to = self.high*100,
#                                         digits = 1, resolution = 1,
#                                         orient = tk.HORIZONTAL, length = 200,
#                                         sliderlength = 10, showvalue = 0, 
#                                         label = "Mean Value",
#                                         name = self.name,
#                                         command = self.set_dac_voltage)
#         self.dac_mean_slider.grid(row=0,column=0,columnspan=1)
#         self.dac_mean_position_value = ttk.Entry(self.dac_frame,width=5)
#         self.dac_mean_position_value.grid(row=0,column = 1,sticky="SE")
#         self.dac_mean_position_value.insert(0,self.dac_mean_slider.get())
#         self.dac_mean_position_value.bind('<Return>',self.set_dac_mean_slider)

#         self.dac_mean_slider.set(self.settings_dict["Average Voltage"]*100)


#         self.wiper_position_button = ttk.Button(self.dac_frame,text="Set Voltage",
#                                                 width=15,
#                                                 command = self.set_dac_mean_slider)
#         self.wiper_position_button.grid(row=0,column = 2,sticky="SW",columnspan=1)

#         self.range_frame = tk.Frame(self.dac_frame)
#         self.range_frame.grid(row=1,column=0,columnspan=3)
#         self.range_frame.grid_columnconfigure(1,weight=2)
#         tk.Label(self.range_frame,text="Low: {} V".format(self.low)).grid(row=0,column=0, sticky="E",columnspan=1)
#         tk.Label(self.range_frame,text="High: {} V".format(self.high)).grid(row=0,column=2,sticky="E",columnspan=1)

#         self.set_dac_voltage()
        
#         self.ecu_app = ecu_application(self.dac_frame,self.settings_dict,row=1,column=0,columnspan=3)
   
   
#     def set_dac_voltage(self,event=None):
            
#         self.dac_mean_position_value.delete(0,tk.END)
#         self.dac_mean_position_value.insert(0,self.dac_mean_slider.get()/100)
#         x=float(self.dac_mean_position_value.get())
#         if self.setting_num == 49:
#             if 'REV03' in self.sss_software_id_text.get():
#                 dac_raw_setting = int(4.2646*x - 16.788) ##Special for Rev3
#             else:
#                 dac_raw_setting = int(19.985*x - 37.522) ##Special for Rev5
#             if dac_raw_setting < 0:
#                dac_raw_setting = 0 
#         else:
#             slope = 4095/(self.high-self.low)
#             dac_raw_setting = int(slope*(x - self.low))
#         commandString = "{},{:d}".format(self.setting_num,dac_raw_setting)
#         self.tx_queue.put_nowait(commandString)
        
    
#     def set_dac_mean_slider(self,event=None):
#         entry_value = self.dac_mean_position_value.get()
#         self.dac_mean_position_value['foreground'] = "black"
#         try:
#             self.dac_mean_slider.set(float(entry_value)*100)
#         except Exception as e:
#             logger.debug(e)
#             self.root.bell()
#             self.dac_mean_position_value['foreground'] = "red"


# class pwm_out(QWidget):
#     def __init__(self, parent,tx_queue,sss2_settings, row = 2, col = 0):
#         self.root = parent
#         self.tx_queue = tx_queue
#         self.row=row
#         self.col=col
#         self.settings_dict = sss2_settings
#         self.number=self.settings_dict["Port"]
#         self.connector=self.settings_dict["Pin"]
#         self.label = self.settings_dict["Name"]+" ("+self.connector+")"
#         self.name = self.label.lower()
#         self.setting_num = self.settings_dict["SSS2 setting"]
#         self.freq_setting_num = self.settings_dict["SSS2 freq setting"]
#         self.setup_pwm_widget()
        
#     def setup_pwm_widget(self):
         
#         self.pwm_frame = tk.LabelFrame(self.root, name=self.name,text=self.label)
#         self.pwm_frame.grid(row=self.row,column=self.col,sticky=tk.W,padx=5,pady=5)
        
#         self.pwm_duty_cycle_slider = tk.Scale(self.pwm_frame,
#                                         from_ = 0,
#                                         to = 100,
#                                         digits = 1, resolution = 0.1,
#                                         orient = tk.HORIZONTAL, length = 90,
#                                         sliderlength = 10, showvalue = 0, 
#                                         label = "Duty Cycle (%)",
#                                         name = self.name+'_duty_cycle',
#                                         command = self.set_pwm_duty_cycle)
#         self.pwm_duty_cycle_slider.grid(row=0,column=0)
#         self.pwm_duty_cycle_value = ttk.Entry(self.pwm_frame,width=5)
#         self.pwm_duty_cycle_value.grid(row=0,column = 1,sticky="SE")
#         self.pwm_duty_cycle_slider.set(self.settings_dict["Duty Cycle"])
#         self.pwm_duty_cycle_value.insert(0,self.pwm_duty_cycle_slider.get())
#         self.pwm_duty_cycle_value.bind('<Return>',self.set_pwm_duty_cycle_slider)
#         self.pwm_duty_cycle_value.icursor(tk.END)
#         self.pwm_duty_cycle_value.focus_set()
#         self.set_pwm_duty_cycle_slider()
        
#         self.wiper_position_button = ttk.Button(self.pwm_frame,text="Set Duty Cycle",
#                                                 width=14,
#                                             command = self.set_pwm_duty_cycle_slider)
#         self.wiper_position_button.grid(row=0,column = 2,sticky="SW",columnspan=1)


#         self.pwm_frequency_slider = tk.Scale(self.pwm_frame,
#                                         from_ = self.settings_dict["Lowest Frequency"],
#                                         to = self.settings_dict["Highest Frequency"],
#                                         digits = 1,
#                                         resolution = 0.1,#(self.settings_dict["Highest Frequency"] -
#                                                       #self.settings_dict["Lowest Frequency"])/200,
#                                         orient = tk.HORIZONTAL, length = 90,
#                                         sliderlength = 14, showvalue = 0, 
#                                         label = "Frequency (Hz)",
#                                         name = self.name+'_frequency',
#                                         command = self.set_pwm_frequency)
#         self.pwm_frequency_slider.grid(row=1,column=0)
#         self.pwm_frequency_value = ttk.Entry(self.pwm_frame,width=5)
#         self.pwm_frequency_value.grid(row=1,column = 1,sticky="SE")
        
#         self.pwm_frequency_slider.set(self.settings_dict["Frequency"])
#         self.pwm_frequency_value.insert(0,self.pwm_frequency_slider.get())
#         self.pwm_frequency_value.bind('<Return>',self.set_pwm_frequency_slider)
#         self.set_pwm_frequency_slider()
        

#         self.frequency_button = ttk.Button(self.pwm_frame,text="Set Frequency",
#                                                 width=15,
#                                             command = self.set_pwm_frequency_slider)
#         self.frequency_button.grid(row=1,column = 2,sticky="SW",columnspan=1)

#         self.set_pwm_frequency()
#         self.set_pwm_duty_cycle()

#         self.ecu_app = ecu_application(self.pwm_frame,self.settings_dict,row=2,column=0,columnspan=3)
   
#     def set_pwm_frequency(self,event=None):
#         self.pwm_frequency_value.delete(0,tk.END)
#         self.pwm_frequency_value.insert(0,self.pwm_frequency_slider.get())
        
#         slope = 1
#         pwm_raw_setting = int(slope*(float(self.pwm_frequency_value.get())))
#         commandString = "{},{}".format(self.freq_setting_num,pwm_raw_setting)
#         self.tx_queue.put_nowait(commandString)
        

#     def set_pwm_duty_cycle(self,event=None):
             
#         self.pwm_duty_cycle_value.delete(0,tk.END)
#         self.pwm_duty_cycle_value.insert(0,self.pwm_duty_cycle_slider.get())
        
#         slope = 4096/100
#         pwm_raw_setting = int(slope*(float(self.pwm_duty_cycle_value.get())))
#         commandString = "{},{}".format(self.setting_num,pwm_raw_setting)
#         self.tx_queue.put_nowait(commandString)
        

#     def set_pwm_frequency_slider(self,event=None):
#         entry_value = self.pwm_frequency_value.get()
#         self.pwm_frequency_value['foreground'] = "black"
#         try:
#             self.pwm_frequency_slider.set(float(entry_value))
#             self.set_pwm_frequency()
#         except Exception as e:
#             logger.debug(e)
#             self.root.bell()
#             self.pwm_frequency_value['foreground'] = "red"
    
#     def set_pwm_duty_cycle_slider(self,event=None):
#         entry_value = self.pwm_duty_cycle_value.get()
#         self.pwm_duty_cycle_value['foreground'] = "black"
#         try:
#             self.pwm_duty_cycle_slider.set(float(entry_value))
#             self.set_pwm_duty_cycle()
#         except Exception as e:
#             logger.debug(e)
#             self.root.bell()
#             self.pwm_duty_cycle_value['foreground'] = "red"
            
# class ecu_application(QWidget):
#     def __init__(self, parent, ecu_settings, row = 2, column = 0,columnspan=3,rowspan=1):
#         self.root = parent
#         self.row=row
#         self.col=column
#         self.rowspan=rowspan
#         self.colspan=columnspan
#         self.settings_dict = ecu_settings
#         self.setup_ecu_application()
        
#     def setup_ecu_application(self):

#         colors=[" ","PPL/WHT","BRN/WHT","YEL/BLK","PNK/BLK","BLUE","GRN/BLK","ORN/BLK","YEL/RED","RED/WHT",
#                 "RED/BLK","BLU/WHT","TAN/BLK","BROWN","BLK/WHT","GRN/WHT","TAN/RED","PURPLE","PINK","TAN",
#                 "ORANGE","GREEN","YELLOW","RED","BLACK","RED/GRN","YEL/GRN"]

        
#         self.ecu_frame = tk.LabelFrame(self.root,name='ecu_frame',text="ECU Application")
#         self.ecu_frame.grid(row=self.row,column=self.col,columnspan=self.colspan,
#                             rowspan=self.rowspan,sticky=tk.E+tk.W)
#         self.ecu_frame.grid_columnconfigure(1,weight=2)
#         self.ecu_frame.grid_columnconfigure(3,weight=2)
        
#         tk.Label(self.ecu_frame,text="Pin").grid(row=0,column=0, sticky=tk.W)
#         self.ecu_pins = ttk.Entry(self.ecu_frame,width=9,name="ecu pins")
#         self.ecu_pins.insert(0,self.settings_dict["ECU Pins"])
#         self.ecu_pins.grid(row=0,column=1,sticky=tk.W)

#         #tk.Label(self.ecu_frame,text="Wire").grid(row=0,column=2, sticky=tk.W)
#         self.ecu_color = ttk.Combobox(self.ecu_frame,name="color",values=sorted(colors),width=9)
#         self.ecu_color.insert(0,self.settings_dict["Wire Color"])
#         self.ecu_color.grid(row=0,column=3,sticky=tk.E)
        
#         self.ecu_app = tk.Entry(self.ecu_frame,name="ecu application")
#         self.ecu_app.insert(tk.END,self.settings_dict["Application"])
#         self.ecu_app.grid(row=1,column=0,columnspan=4,sticky=tk.E+tk.W)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    execute = SSS2Interface()
    sys.exit(app.exec_())
    
