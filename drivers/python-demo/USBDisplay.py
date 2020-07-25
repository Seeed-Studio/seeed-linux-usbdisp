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

displayEndpointAddr = 0x04

########################## fill screen ##############################
# fillScreen_color = random.randint(0, 65535)
# fillScreen_color = 0xFFFF
# fillScreen_header = 0x81
# fillScreen_index = "<BH"
# fillScreen_end_index = "<B"
# fillScreen_data = [fillScreen_header, fillScreen_color]

# fillScreen_package = struct.pack(fillScreen_index, *fillScreen_data)
# fillScreen_end_package = struct.pack(fillScreen_end_index, fillScreen_header)

# fillScreen_cnt = dev1.write(displayEndpointAddr, fillScreen_package)
# dev1.write(displayEndpointAddr, fillScreen_end_package)
# fillScreen_cnt = dev2.write(displayEndpointAddr, fillScreen_package)
# dev2.write(displayEndpointAddr, fillScreen_end_package)
# fillScreen_cnt = dev3.write(displayEndpointAddr, fillScreen_package)
# dev3.write(displayEndpointAddr, fillScreen_end_package)
# fillScreen_cnt = dev4.write(displayEndpointAddr, fillScreen_package)
# dev4.write(displayEndpointAddr, fillScreen_end_package)

# print("fillScreen. Send %d byte(s) data." %fillScreen_cnt)
# print("Write------->successful!\n")
######################################################################

########################## rect ######################################
# left = 0
# right = 100
# printOneTime = 0
# while(True):
# 	rect_header = 0x83
# 	top = 0
# 	bottom = 100
# 	rect_color = random.randint(0, 65535)
# 	operation = 0
# 	rect_index = "<BHHHHHB"
# 	rect_end_index = "<B"
# 	rect_data = [rect_header, left, top, right, bottom, rect_color, operation]
	
# 	rect_package = struct.pack(rect_index, *rect_data)
# 	rect_end_package = struct.pack(rect_end_index, rect_header)
	
# 	rect_cnt = dev1.write(displayEndpointAddr, rect_package)
# 	dev1.write(displayEndpointAddr, rect_end_package)
# 	rect_cnt = dev2.write(displayEndpointAddr, rect_package)
# 	dev2.write(displayEndpointAddr, rect_end_package)
# 	rect_cnt = dev3.write(displayEndpointAddr, rect_package)
# 	dev3.write(displayEndpointAddr, rect_end_package)
# 	rect_cnt = dev4.write(displayEndpointAddr, rect_package)
# 	dev4.write(displayEndpointAddr, rect_end_package)
# 	time.sleep(0.05)
	
# 	left = left + 10
# 	right = right + 10
# 	if(left==350):
# 		left = 0
# 		right = 100
	
# 	if(printOneTime==0):
# 		printOneTime = 1
# 		print("rect. Send %d byte(s) data." %rect_cnt)
# 		print("Write------->successful!\n")
######################################################################

############################# copyArea ###############################
# copyArea_header = 0x84
# sx = random.randint(0, 320)
# sy = random.randint(0, 240)
# dx = random.randint(0, 320)
# dy = random.randint(0, 240)
# width = 100
# height = 100
# copyArea_index = "<BHHHHHH"
# copyArea_end_index = "<B"
# copyArea_data = [copyArea_header, sx, sy, dx, dy, width, height]

# copyArea_package = struct.pack(copyArea_index, *copyArea_data)
# copyArea_end_package = struct.pack(copyArea_end_index, copyArea_header)

# copyArea_cnt = dev1.write(displayEndpointAddr, copyArea_package)
# dev1.write(displayEndpointAddr, copyArea_end_package)
# copyArea_cnt = dev2.write(displayEndpointAddr, copyArea_package)
# dev2.write(displayEndpointAddr, copyArea_end_package)
# copyArea_cnt = dev3.write(displayEndpointAddr, copyArea_package)
# dev3.write(displayEndpointAddr, copyArea_end_package)
# copyArea_cnt = dev4.write(displayEndpointAddr, copyArea_package)
# dev4.write(displayEndpointAddr, copyArea_end_package)

# print("copyArea. Send %d byte(s) data." %copyArea_cnt)
# print("Write------->successful!\n")
######################################################################

########################## bitblt ####################################
image = Image.open("./img_20_30.png")
image = image.convert("RGB")
image_data = []
width = image.width
height = image.height
for y in range(height):
	for x in range(width):
		pixel = image.getpixel((x, y))
		#pixel = (pixel[0] + pixel[1] + pixel[2]) / 3
		R = ((pixel[0] >> 3) << 11) & 0xF800
		G = ((pixel[1] >> 2) << 5)  & 0x07E0
		B = ( pixel[2] >> 3)        & 0x001F
		RGB565_data = R | G | B
		image_data.append(RGB565_data)
# print(type(image))
# print(image)
# print(image_data)

bitblt_start_header = 0x82
bitblt_subpackage_header = 0x02
x = 0
y = 0
while(True):
	width = image.width
	height = image.height
	operation = 0
	bitblt_index_for_parameter = "<BHHHHB"
	bitblt_index_for_image = "<BHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"  # 1+31x2 = 63bytes
	bitblt_index_for_image_end = "<BHHHHHHHHHHH"  # 1+11x2 = 63bytes
	bitblt_index_end = "<B"
	
	bitblt_parameterData = [bitblt_start_header, x, y, width, height, operation]
	# bitblt_subImageData = [bitblt_subpackage_header, subImageData]
	bitblt_subImageData_end = [bitblt_subpackage_header, *image_data[589:600]]
	
	bitblt_parameterPackage    = struct.pack(bitblt_index_for_parameter, *bitblt_parameterData)
	# bitblt_subImageDataPackage = struct.pack(bitblt_index_for_image, *bitblt_subImageData)
	bitblt_subImageDataPackage_end = struct.pack(bitblt_index_for_image_end, *bitblt_subImageData_end)
	bitblt_end_package         = struct.pack(bitblt_index_end, bitblt_start_header)
	
	dev1.write(displayEndpointAddr, bitblt_parameterPackage)
	dev2.write(displayEndpointAddr, bitblt_parameterPackage)
	dev3.write(displayEndpointAddr, bitblt_parameterPackage)
	dev4.write(displayEndpointAddr, bitblt_parameterPackage)
	for i in range(19):
		bitblt_subImageData = [bitblt_subpackage_header, *image_data[i*31 : 31+i*31]]
		bitblt_subImageDataPackage = struct.pack(bitblt_index_for_image, *bitblt_subImageData)
		cnt = dev1.write(displayEndpointAddr, bitblt_subImageDataPackage)
		dev2.write(displayEndpointAddr, bitblt_subImageDataPackage)
		dev3.write(displayEndpointAddr, bitblt_subImageDataPackage)
		dev4.write(displayEndpointAddr, bitblt_subImageDataPackage)
	dev1.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
	dev1.write(displayEndpointAddr, bitblt_end_package)
	dev2.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
	dev2.write(displayEndpointAddr, bitblt_end_package)
	dev3.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
	dev3.write(displayEndpointAddr, bitblt_end_package)
	dev4.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
	dev4.write(displayEndpointAddr, bitblt_end_package)
	
	time.sleep(0.2)
	
	x = x + 20
	if(x==320):
		x = 0
		y = y+30
		if(y>210):
			y=0

# fillScreen_cnt = dev1.write(displayEndpointAddr, fillScreen_package)
# dev1.write(displayEndpointAddr, fillScreen_end_package)
# fillScreen_cnt = dev2.write(displayEndpointAddr, fillScreen_package)
# dev2.write(displayEndpointAddr, fillScreen_end_package)
# fillScreen_cnt = dev3.write(displayEndpointAddr, fillScreen_package)
# dev3.write(displayEndpointAddr, fillScreen_end_package)
# fillScreen_cnt = dev4.write(displayEndpointAddr, fillScreen_package)
# dev4.write(displayEndpointAddr, fillScreen_end_package)

print("fillScreen. Send %d byte(s) data." %cnt)
print("Write------->successful!\n")

######################################################################