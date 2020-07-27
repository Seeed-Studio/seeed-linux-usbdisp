import usb.core
import usb.util
import struct
import time
import random

from PIL import Image

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
# dev1.set_interface_altsetting(interface = 3, alternate_setting = 0)
# dev2.set_interface_altsetting(interface = 3, alternate_setting = 0)
# dev3.set_interface_altsetting(interface = 3, alternate_setting = 0)
# dev4.set_interface_altsetting(interface = 3, alternate_setting = 0)

displayEndpointAddr = 0x04

########################## fill screen ##############################
def fillScreen(color):
	# fillScreen_color = random.randint(0, 65535)
	# fillScreen_color = 0xF800 # red
	# fillScreen_color = 0xFFFF # white
	fillScreen_color = color
	fillScreen_header = 0x81
	fillScreen_index = "<BH"
	fillScreen_index_end = "<B"
	fillScreen_data = [fillScreen_header, fillScreen_color]

	fillScreen_package = struct.pack(fillScreen_index, *fillScreen_data)
	fillScreen_package_end = struct.pack(fillScreen_index_end, fillScreen_header)

	fillScreen_cnt = dev1.write(displayEndpointAddr, fillScreen_package)
	dev1.write(displayEndpointAddr, fillScreen_package_end)
	# time.sleep(1)
	fillScreen_cnt = dev2.write(displayEndpointAddr, fillScreen_package)
	dev2.write(displayEndpointAddr, fillScreen_package_end)
	# time.sleep(1)
	fillScreen_cnt = dev3.write(displayEndpointAddr, fillScreen_package)
	dev3.write(displayEndpointAddr, fillScreen_package_end)
	# time.sleep(1)
	fillScreen_cnt = dev4.write(displayEndpointAddr, fillScreen_package)
	dev4.write(displayEndpointAddr, fillScreen_package_end)

	print("fillScreen. Send %d byte(s) data." %fillScreen_cnt) # 3 bytes
	print("Write------->successful!\n")

	time.sleep(0.5)
######################################################################

########################## rect ######################################
def rect(left, top, right, bottom, color, operation):
	rect_left = left
	rect_right = right
	# rect_printOneTime = 0
	rect_header = 0x83
	rect_top = top
	rect_bottom = bottom
	# rect_color = random.randint(0, 65535)
	rect_color = color
	rect_operation = operation
	rect_index = "<BHHHHHB"
	rect_index_end = "<B"
	rect_data = [rect_header, rect_left, rect_top, rect_right, rect_bottom, rect_color, rect_operation]

	rect_package = struct.pack(rect_index, *rect_data)
	rect_package_end = struct.pack(rect_index_end, rect_header)

	rect_cnt = dev1.write(displayEndpointAddr, rect_package)
	dev1.write(displayEndpointAddr, rect_package_end)
	rect_cnt = dev2.write(displayEndpointAddr, rect_package)
	dev2.write(displayEndpointAddr, rect_package_end)
	rect_cnt = dev3.write(displayEndpointAddr, rect_package)
	dev3.write(displayEndpointAddr, rect_package_end)
	rect_cnt = dev4.write(displayEndpointAddr, rect_package)
	dev4.write(displayEndpointAddr, rect_package_end)

	# rect_left = rect_left + 10
	# rect_right = rect_right + 10
	# if(rect_left==350):
	# 	rect_left = 0
	# 	rect_right = 100

	# time.sleep(0.5)

	# if(rect_printOneTime==0):
	# 	rect_printOneTime = 1
	print("rect. Send %d byte(s) data." %rect_cnt) # 12 bytes
	print("Write------->successful!\n")
######################################################################

############################# copyArea ###############################
def copyArea(sx, sy, dx, dy, width, height):
	# copyArea_printOneTime = 0
	copyArea_header = 0x84
	copyArea_sx = sx
	copyArea_sy = sy
	copyArea_dx = dx
	copyArea_dy = dy
	copyArea_width = width
	copyArea_height = height
	copyArea_index = "<BHHHHHH"
	copyArea_index_end = "<B"
	copyArea_data = [copyArea_header, copyArea_sx, copyArea_sy, copyArea_dx, copyArea_dy, copyArea_width, copyArea_height]

	copyArea_package = struct.pack(copyArea_index, *copyArea_data)
	copyArea_package_end = struct.pack(copyArea_index_end, copyArea_header)

	copyArea_cnt = dev1.write(displayEndpointAddr, copyArea_package)
	dev1.write(displayEndpointAddr, copyArea_package_end)
	copyArea_cnt = dev2.write(displayEndpointAddr, copyArea_package)
	dev2.write(displayEndpointAddr, copyArea_package_end)
	copyArea_cnt = dev3.write(displayEndpointAddr, copyArea_package)
	dev3.write(displayEndpointAddr, copyArea_package_end)
	copyArea_cnt = dev4.write(displayEndpointAddr, copyArea_package)
	dev4.write(displayEndpointAddr, copyArea_package_end)

	# time.sleep(0.3)

	# if(copyArea_printOneTime==0):
	# 	copyArea_printOneTime = 1
	print("copyArea. Send %d byte(s) data." %copyArea_cnt) # 13 bytes
	print("Write------->successful!\n")
######################################################################

########################## bitblt ####################################
def bitblt(x, y, image_path,  operation):
	# image_path = "./img_20_30.png"
	# image_path = "./img_30_40.jpg"
	# image_path = "./img_160_240.png"
	# image_path = "./img_320_240.png"
	# image = Image.open(image_path)
	image = Image.open(image_path)
	image = image.convert("RGB")
	image_data = []
	bitblt_width = image.width
	bitblt_height = image.height
	# bitblt_printOneTime = 0

	# print(type(image))
	# print(image)
	# print(image_data)

	# convert (R, G, B) -----> RGB565 (0xRGB)
	for y_ in range(bitblt_height):
		for x_ in range(bitblt_width):
			pixel = image.getpixel((x_, y_))
			# pixel = (pixel[0] + pixel[1] + pixel[2]) / 3
			R = ((pixel[0] >> 3) << 11) & 0xF800
			G = ((pixel[1] >> 2) << 5)  & 0x07E0
			B = ( pixel[2] >> 3)        & 0x001F
			RGB565_data = R | G | B
			image_data.append(RGB565_data)

	bitblt_start_header = 0x82
	bitblt_subpackage_header = 0x02
	bitblt_x = x
	bitblt_y = y

	image_size = bitblt_width * bitblt_height
	integer_part = (int)(image_size / 31)
	remainder_part = ((image_size) - (integer_part * 31))

	# while(True):
	bitblt_width = image.width
	bitblt_height = image.height
	bitblt_operation = operation
	bitblt_index_for_parameter = "<BHHHHB"
	bitblt_index_for_image = "<BHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"  # 1+31x2 = 63 bytes

	# bitblt_index_for_image_end = "<BHHHHHHHHHHH"  # 1+11x2 = 23 bytes
	bitblt_index_for_image_end = "<B"
	for i in range(remainder_part):
		bitblt_index_for_image_end = bitblt_index_for_image_end + 'H'

	# if(bitblt_printOneTime==0):
	print(bitblt_index_for_image_end)

	bitblt_index_end = "<B"

	bitblt_parameterData = [bitblt_start_header, bitblt_x, bitblt_y, bitblt_width, bitblt_height, bitblt_operation]
	# bitblt_subImageData = [bitblt_subpackage_header, subImageData]
	bitblt_subImageData_end = [bitblt_subpackage_header, *image_data[integer_part*31 : image_size]]

	bitblt_parameterPackage    = struct.pack(bitblt_index_for_parameter, *bitblt_parameterData)
	# bitblt_subImageDataPackage = struct.pack(bitblt_index_for_image, *bitblt_subImageData)
	bitblt_subImageDataPackage_end = struct.pack(bitblt_index_for_image_end, *bitblt_subImageData_end)
	bitblt_package_end         = struct.pack(bitblt_index_end, bitblt_start_header)

	dev1.write(displayEndpointAddr, bitblt_parameterPackage)
	dev2.write(displayEndpointAddr, bitblt_parameterPackage)
	dev3.write(displayEndpointAddr, bitblt_parameterPackage)
	dev4.write(displayEndpointAddr, bitblt_parameterPackage)

	# if(bitblt_printOneTime==0):
	print((int)(image_size / 31))
	print("integer_part:",integer_part)
	print("remainder_part:",remainder_part)


	for i in range(integer_part):
		bitblt_subImageData = [bitblt_subpackage_header, *image_data[i*31 : 31+i*31]]
		bitblt_subImageDataPackage = struct.pack(bitblt_index_for_image, *bitblt_subImageData)
		
		bitblt_cnt = dev1.write(displayEndpointAddr, bitblt_subImageDataPackage)
		bitblt_cnt = dev2.write(displayEndpointAddr, bitblt_subImageDataPackage)
		bitblt_cnt = dev3.write(displayEndpointAddr, bitblt_subImageDataPackage)
		bitblt_cnt = dev4.write(displayEndpointAddr, bitblt_subImageDataPackage)

	dev1.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
	dev1.write(displayEndpointAddr, bitblt_package_end)
	dev2.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
	dev2.write(displayEndpointAddr, bitblt_package_end)
	dev3.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
	dev3.write(displayEndpointAddr, bitblt_package_end)
	dev4.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
	dev4.write(displayEndpointAddr, bitblt_package_end)

	# time.sleep(0.4)

	# bitblt_x = bitblt_x + 20
	# if(bitblt_x == 320):
	# 	bitblt_x = 0
	# 	bitblt_y = bitblt_y + 30
	# 	if(bitblt_y > 210):
	# 		bitblt_y = 0


	# if(bitblt_printOneTime==0):
		# bitblt_printOneTime = 1
	print("bitblt. Send %d byte(s) data." %bitblt_cnt) # 63 bytes
	print("Write------->successful!\n")
######################################################################

########################### main() ###################################
def main():
	# print("test fillScreen function.")
	# # while(True):
	# fillScreen(random.randint(0, 65535))
	# # time.sleep(1)

	# print("test rect function.")
	# rect_left = 0
	# rect_right = 100
	# rect_top = 0
	# rect_bottom = 100
	# while (True):
	# 	rect(rect_left, rect_top, rect_right, rect_bottom, random.randint(0, 65535), 0)
	
	# 	rect_left = rect_left + 10
	# 	rect_right = rect_right + 10
	# 	if(rect_left==350):
	# 		rect_left = 0
	# 		rect_right = 100
	# 	time.sleep(1)

	# print("test copyArea function.")
	# while (True):
	# 	copyArea(random.randint(0, 320), random.randint(0, 240), random.randint(0, 320), random.randint(0, 240), 100, 100)
	# 	time.sleep(1)

	print("test bitblt function.")
	path = "./img_20_30.png"
	bitblt_x = 0
	bitblt_y = 0
	while(True):
		bitblt(x=bitblt_x, y=bitblt_y, image_path=path,  operation=0)
		bitblt_x = bitblt_x + 20
		if(bitblt_x > 320):
			bitblt_x = 0
			bitblt_y = bitblt_y + 30
			if(bitblt_y > 210):
				bitblt_y = 0
				fillScreen(0xffff)
		# time.sleep(0.3)

if __name__ == '__main__':
	main()
######################################################################