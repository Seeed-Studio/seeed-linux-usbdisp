'''
 * simple-test.py
 * Seeed Linux USB Display demo in python
 *
 * A demo for Wio Terminal to single-screen display in python.
 *
 * Copyright (c) 2020 seeed technology co., ltd.
 * Author      : weihong.cai (weihong.cai@seeed.cc)
 * Create Time : July 2020
 * Change Log  :
 *
 * The MIT License (MIT)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
 * and to permit persons to whom the Software istm furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions
 * of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
 * THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS INcommInterface
 * THE SOFTWARE.
 *
 * Get started:
 *     1. Download the pyusb library use pip3:
 *         $ pip3 install pyusb
 *     2. Go to the python-demo path:
 *         $ cd ~/seeed-linux-usbdisp/drivers/python-demo/
 *     3. Run demo:
 *         $ sudo python3 simple-test.py
'''

import usb.core
import usb.util
import struct
import time
import random

from PIL import Image

#------Please choose one of them according to the WioTerminal Demo--------#
# NullFunctional_Demo_for_WioTerminal
displayEndpointAddr = 0x04

# USBDisplayAndMouseControl_Demo_for_WioTerminal
# displayEndpointAddr = 0x05
#-------------------------------------------------------------------------#

# find our device
devices = list(usb.core.find(find_all=True, idVendor=0x2886, idProduct=0x802D))
dev1 = devices[0]

if dev1 is None:
	raise ValueError('Device not found')

# print device serial_number
print(dev1.serial_number)

# set interface altsetting
# dev1.set_interface_altsetting(interface = 3, alternate_setting = 0)

########################## fill screen ###################################################
'''
brief: Fill the whole screen with color

color: A 16 bit color represent in B5G6R5 format
dev1_on: Select dev1 to work
'''
def fillScreen(color, dev1_on):
	# fillScreen_color = random.randint(0, 65535)
	# fillScreen_color = 0xF800 # red
	# fillScreen_color = 0xFFFF # white
	# fillScreen_printOneTime = 0
	fillScreen_color = color
	fillScreen_header = 0x81
	fillScreen_index = "<BH"
	fillScreen_index_end = "<B"
	fillScreen_data = [fillScreen_header, fillScreen_color]

	fillScreen_package = struct.pack(fillScreen_index, *fillScreen_data)
	fillScreen_package_end = struct.pack(fillScreen_index_end, fillScreen_header)

	if(dev1_on):
		fillScreen_cnt = dev1.write(displayEndpointAddr, fillScreen_package)
		dev1.write(displayEndpointAddr, fillScreen_package_end)
	time.sleep(1)

	# if(fillScreen_printOneTime==0)
	# 	fillScreen_printOneTime=1
	print("fillScreen. Send %d byte(s) data." %fillScreen_cnt) # 3 bytes
	print("Write------->successful!\n")

	time.sleep(1)
##########################################################################################

############################### rect #####################################################
'''
brief    : Fill a rectangle of the display with a solid color

left     : The left boundry of the rectangle
top      : The top boundry of the rectangle
right    : The right boundry of the rectangle
bottom   : The bottom boundry of the rectangle
color    : A 16 bit color represent in B5G6R5 format
operation: The pixel bit operation will be done when filling the rectangle
dev1_on  : Select dev1 to work
'''
def rect(left, top, right, bottom, color, operation, dev1_on):
	rect_header = 0x83
	rect_left = left
	rect_top = top
	rect_right = right
	rect_bottom = bottom
	# rect_printOneTime = 0
	# rect_color = random.randint(0, 65535)
	rect_color = color
	rect_operation = operation
	rect_index = "<BHHHHHB"
	rect_index_end = "<B"
	rect_data = [rect_header, rect_left, rect_top, rect_right, rect_bottom, rect_color, rect_operation]

	rect_package = struct.pack(rect_index, *rect_data)
	rect_package_end = struct.pack(rect_index_end, rect_header)

	if(dev1_on):
		rect_cnt = dev1.write(displayEndpointAddr, rect_package)
		dev1.write(displayEndpointAddr, rect_package_end)

	print("rect. Send %d byte(s) data." %rect_cnt) # 12 bytes
	print("Write------->successful!\n")
##########################################################################################

############################# copyArea ###################################################
'''
brief : Copy a part of the existing image of the screen to another position of the display

sx    : Source x coordinate
sy    : Source y coordinate
dx    : Destination x coordinate
dy    : Destination y coordinate
width : Width of the copying area
height: Height of the copying area
dev1_on: Select dev1 to work
'''
def copyArea(sx, sy, dx, dy, width, height, dev1_on):
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

	if(dev1_on):
		copyArea_cnt = dev1.write(displayEndpointAddr, copyArea_package)
		dev1.write(displayEndpointAddr, copyArea_package_end)

	time.sleep(0.3)

	# if(copyArea_printOneTime==0):
	# 	copyArea_printOneTime = 1
	print("copyArea. Send %d byte(s) data." %copyArea_cnt) # 13 bytes
	print("Write------->successful!\n")
##########################################################################################

############################ bitblt ######################################################
'''
brief     : Draw image to the display

x         : The x coordinate where the image will be painted
y         : The y coordinate where the image will be painted
image_path: The path of image
operation : The pixel bit operation will be done between the original pixel and the pixel from the image
dev1_on   : Select dev1 to work
'''
def bitblt(x, y, image_path,  operation, dev1_on):

	image = Image.open(image_path)
	image = image.convert("RGB")
	image_data = []
	bitblt_width = image.width
	bitblt_height = image.height


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

	if(dev1_on):
		dev1.write(displayEndpointAddr, bitblt_parameterPackage)

	# if(bitblt_printOneTime==0):
	print((int)(image_size / 31))
	print("integer_part:",integer_part)
	print("remainder_part:",remainder_part)

	for i in range(integer_part):
		bitblt_subImageData = [bitblt_subpackage_header, *image_data[i*31 : 31+i*31]]
		bitblt_subImageDataPackage = struct.pack(bitblt_index_for_image, *bitblt_subImageData)
		
		if(dev1_on):
			bitblt_cnt = dev1.write(displayEndpointAddr, bitblt_subImageDataPackage)

	if(dev1_on):
		dev1.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
		dev1.write(displayEndpointAddr, bitblt_package_end)

	time.sleep(0.4)

	print("bitblt. Send %d byte(s) data." %bitblt_cnt) # 63 bytes
	print("Write------->successful!\n")
##########################################################################################


########################### main() #######################################################
def main():
	print("test fillScreen function.")
	for _ in range(1,10,1):
		fillScreen(color=random.randint(0, 65535), dev1_on=True)

	fillScreen(color=0xffff, dev1_on=True)
	rect_left = 0
	rect_top = 0
	rect_right = 100
	rect_bottom = 100
	for _ in range(1,10,1):
		rect(left=rect_left, top=rect_top, right=rect_right, bottom=rect_bottom, \
			color=random.randint(0, 65535), operation=0, \
			dev1_on=True)
		rect_left = rect_left + 10
		rect_right = rect_right + 10
		if(rect_left==350):
			rect_left = 0
			rect_right = 100
		time.sleep(1)

	print("test copyArea function.")
	for _ in range(1,10,1):
		copyArea(sx=random.randint(0, 320), sy=random.randint(0, 240), \
				dx=random.randint(0, 320), dy=random.randint(0, 240), \
				width=100, height=100, \
				dev1_on=True)
		time.sleep(1)

	print("test bitblt function.")
	fillScreen(color=0xffff, dev1_on=True)
	path = "./image/img_20_30.png"
	bitblt_x = 0
	bitblt_y = 0
	while(True):
		bitblt(x=bitblt_x, y=bitblt_y, image_path=path, operation=0, dev1_on=True)
		bitblt_x = bitblt_x + 20
		if(bitblt_x > 320):
			bitblt_x = 0
			bitblt_y = bitblt_y + 30
			if(bitblt_y > 210):
				bitblt_y = 0
				fillScreen(color=0xffff, dev1_on=True)
		time.sleep(0.3)

if __name__ == '__main__':
    main()