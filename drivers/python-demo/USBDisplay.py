import usb.core
import usb.util
import struct
import time
import random

# find our device
devices = list(usb.core.find(find_all=True, idVendor=0x2886, idProduct=0x802D))
dev1 = devices[0]
dev2 = devices[1]
dev3 = devices[2]
dev4 = devices[3]
if dev1 is None:
	raise ValueError('Device not found')
if dev2 is None:
	raise ValueError('Device not found')
if dev3 is None:
	raise ValueError('Device not found')
if dev4 is None:
	raise ValueError('Device not found')

# print device serial_number
print(dev1.serial_number)
print(dev2.serial_number)
print(dev3.serial_number)
print(dev4.serial_number)

# set interface altsetting
dev1.set_interface_altsetting(interface = 3, alternate_setting = 0)
dev2.set_interface_altsetting(interface = 3, alternate_setting = 0)
dev3.set_interface_altsetting(interface = 3, alternate_setting = 0)
dev4.set_interface_altsetting(interface = 3, alternate_setting = 0)

########################## fill screen ##############################
while(True):
	color = random.randint(0, 65535)
	package = struct.pack("<BH", 0x81, color)
	end = struct.pack("<B", 0x81)

	cnt1 = dev1.write(0x04, package)
	dev1.write(0x04, end)
	cnt2 = dev2.write(0x04, package)
	dev2.write(0x04, end)
	cnt3 = dev3.write(0x04, package)
	dev3.write(0x04, end)
	cnt4 = dev4.write(0x04, package)
	dev4.write(0x04, end)
	
	time.sleep(1)
	
	print("Send %d byte(s) data." %cnt1)
	print("Send %d byte(s) data." %cnt2)
	print("Send %d byte(s) data." %cnt3)
	print("Send %d byte(s) data." %cnt4)
	print("Write------->successful!\n")
####################################################################