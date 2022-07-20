from msvcrt import kbhit
import pywinusb.hid as hid
import usb.core
import usb.util
import struct
#import crc16
import traceback
import time
from time import sleep

import usb.backend.libusb1
backend = usb.backend.libusb1.get_backend(find_library=lambda x: "libusb0.dll")
print("Backend: ",backend)



# must have libusb-win32 installed.
# use Zdiag

USB_HID_OUTPUT_ENDPOINT_ADDRESS = 0x02
USB_HID_INPUT_ENDPOINT_ADDRESS = 0x81
USB_HID_LENGTH = 64
USB_HID_TIMEOUT = 0  # 0 = Blocking


def sample_handler(data):
    print("Raw data: {0}".format(data))

def crc16_ccitt(crc, data):
    msb = (crc & 0xFF00) >> 8
    lsb = crc & 0xFF
    for c in data:
        x = c ^ msb
        x ^= (x >> 4)
        msb = (lsb ^ (x >> 3) ^ (x << 4)) & 255
        lsb = (x ^ (x << 5)) & 255
    return bytes([lsb, msb])



def raw_test():

	filter = hid.HidDeviceFilter(vendor_id=0x16c0, product_id=0x0486)
	hid_device = filter.get_devices()
	device = hid_device[0]
	if device is None:
		raise ValueError('Device not found')
	# device.open()
	print(hid_device)

	try:
		device.open()

		#set custom raw data handler
		device.set_raw_data_handler(sample_handler)


		print(
			"\nWaiting for data...\nPress any (system keyboard) key to stop...")
		while device.is_plugged():
			#just keep the device opened to receive events
			sleep(1)
			
			# print(report)
			# print(report[0])
			data = b'\x63,1,32,2,33,3,34,4,42,17,42,50,1'
			padded_data = data + bytes([0 for i in range(62 - len(data))])
			crc = crc16_ccitt(0xFFFF, bytes(padded_data))
			print(crc)
			data_to_send = bytes(padded_data) + crc
			print(data_to_send)
			# buffer = [0xFF]*64
			# buffer[0] = 0xAB

			# print(buffer)
			# out_report = device.find_output_reports()
			# out_report[0].set_raw_data(buffer)
			# out_report[0].send()
			for report in device.find_output_reports():
				if target_usage in report:
					# found out target!
					report[target_usage] = 1 # yes, changing values is that easy
					# at this point you could change different usages at a time...
					# and finally send the prepared output report
					report.send()
					# now toggle back the signal
					report[target_usage] = 0
					report.send()
					print("\nUsage clicked!\n")
					return

			
		return
		
	finally:
		device.close()



# if __name__ == '__main__':
#     raw_test()
# find our device
# sss = usb.core.find()
for device in usb.core.find(find_all=True, idVendor=0x16c0, idProduct=0x0486):
	sss = device
	
# was the usb instance found?
if sss is None:
    raise ValueError('Device not found')
print(sss)
sss.set_configuration()
# get an endpoint instance
cfg = sss.get_active_configuration()
sss_interface = cfg[(0,0)]


data = b'\x10,1,32,2,33,3,34,4,42,17,42,50,1' 
padded_data = data + bytes([0 for i in range(62 - len(data))])
crc = crc16_ccitt(0xFFFF, bytes(padded_data))
print(crc)
data_to_send = bytes(padded_data) + crc
print(data_to_send)
print(len(data_to_send))
sss.write(USB_HID_OUTPUT_ENDPOINT_ADDRESS, data_to_send, USB_HID_TIMEOUT)
while(1):
	# read method returns an array of bytes 
	# see (https://docs.python.org/3/library/array.html)
	time.sleep(0.1)
	try:
		data_stream = bytes(sss.read(USB_HID_INPUT_ENDPOINT_ADDRESS, 
								 USB_HID_LENGTH, 
								 300))
		data_stream_crc = data_stream[62:64]
		calculated_crc = crc16_ccitt(0xFFFF, data_stream[0:62])
		print(data_stream)
		#print(calculated_crc)
		# assert data_stream_crc == calculated_crc
		
	except usb.core.USBError:
		time.sleep(0.002)
	except:
		print(traceback.format_exc())

 # The data payload can be any sequence type that can be used 
 # as a parameter for the array __init__ method. 
data = b'\x10,50,0,b1, ,B0' 
padded_data = data + bytes([0 for i in range(62 - len(data))])
crc = crc16_ccitt(0xFFFF, bytes(padded_data))
print(crc)
data_to_send = bytes(padded_data) + crc
print(data_to_send)
print(len(data_to_send))
sss.write(USB_HID_OUTPUT_ENDPOINT_ADDRESS, data_to_send, USB_HID_TIMEOUT)
usb.util.release_interface(sss,sss_interface)
