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

print("dev1:", dev1.serial_number)

# # was it found?
# if dev is None:
#     raise ValueError('Device not found')
if dev1 is None:
    raise ValueError('Device not found')


############################ bitblt ######################################################
'''
brief     : Draw image to the display

x         : The x coordinate where the image will be painted
y         : The y coordinate where the image will be painted
image_path: The path of image
operation : The pixel bit operation will be done between the original pixel and the pixel from the image
dev1_on/dev2_on/dev3_on/dev4_on: Select which device to work
'''
def bitblt(x, y, image_path,  operation, dev1_on):
	# image_path = "./img_20_30.png"
	# image = Image.open(image_path)
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
	# time.sleep(0.4)

	print("bitblt. Send %d byte(s) data." %bitblt_cnt) # 63 bytes
	print("Write------->successful!\n")
##########################################################################################

########################### main() #######################################################
def main():
	image_path = "./image.jpg"
	bitblt(x=0, y=0, image_path=image_path, operation=0, dev1_on=True)

if __name__ == '__main__':
	main()