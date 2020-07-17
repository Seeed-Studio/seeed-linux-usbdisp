# Seeed Linux USB Display

Driver for Linux USB Display Project

You can use it for multi-screen expansion display and multi-screen clone display.


## WIKI
Get more detail about Seeed Linux USB Display from: 
[WIKI](https://wiki.seeedstudio.com/Wio-Terminal-HMI)


## Get Started
Take Raspberry Pi as an example.
1. Update the raspberry pi kernel headers and kernels.
```
$ sudo apt-get -y --force-yes install raspberrypi-kernel-headers raspberrypi-kernel
```
2. Download the display driver to your local path using git tool.
```
$ cd Your_Local_Path/
$ git clone https://github.com/Seeed-Studio/seeed-linux-usbdisp.git
```
3. Go to the linux-driver path.
```
$ cd Your_Local_Path/seeed-linux-usbdisp/drivers/linux-driver/
```
4. Make and build the driver.
```
$ make && sudo make install
```
5. Restart raspberry pi.
```
$ sudo reboot
```
6. Go to /seeed-linux-usbdisp/drivers/linux-driver/xserver_conf/, And there are five xorg.config sample files in this folder. Please copy one of the files according to your own needs to /usr/share/X11/xorg.conf.d/ (You can also modify the xorg.config file by yourself)
```
$ cd Your_Local_Path/seeed-linux-usbdisp/drivers/linux-driver/xserver_conf/
$ sudo cp The_File_You_Need /usr/share/X11/xorg.conf.d/
```
7. Restart the X11 Server.
```
$ sudo service lightdm restart
```



## Contributing

Contributing to this software is warmly welcomed. You can do this basically by<br>
[forking](https://help.github.com/articles/fork-a-repo), committing modifications and then [pulling requests](https://help.github.com/articles/using-pull-requests) (follow the links above<br>
for operating guide). Adding change log and your contact into file header is encouraged.<br>
Thanks for your contribution.

Seeed Studio is an open hardware facilitation company based in Shenzhen, China. <br>
Benefiting from local manufacture power and convenient global logistic system, <br>
we integrate resources to serve new era of innovation. Seeed also works with <br>
global distributors and partners to push open hardware movement.<br>
