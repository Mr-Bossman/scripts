## Making 32u4_bulk
##### A bulk storage USB device from the Atmega32u4

I wanted to have the ability to write data to a cheep lcd i bought but all of my MCU weren't fast enough to do this. I wanted a way to display pictures and video but UART wasnt fast enought so i decided to use USB. i went online to see if some one had done it before, they did using VUSB. there was also an example i found for using usb without VUSB but wasnt for mass storege. There was also a simple explanation of how SCSI over usb worked. I used all of these to create my device, although i could have used VUSB from the start i didnt want to becuse i wanted to learn how the protocalls worked. I endded up havind two functions that would be caled to read and write data to the storage device, but in reality we can only write to the LCD, and becuse i had already made code to controll the LCD it was very easy to combine them.


I finaly could display binary data on the display. Unfortunatly i couldnt display images yet becuse i want wrinting the data in the rufht format. So i used my favorite image library (OpenCV) to make a program to convert video/ image to RGB565 and write it to my fake block device.

Finaly i coulde display images. i added a batery so that i coulde carry i around and then i fealt like this project had come to a close.

