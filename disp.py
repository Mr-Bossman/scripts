from time import sleep
import cv2
#dsk = open(r"\\.\physicaldrive1",'rb+')
class hardwareD:
	def __init__(self,drive):
		self.dsk = open(drive,'rb+') # open drive that is memory map of the display and buzzer
		self.drive = drive # save path

	def writedisp(self,arr):
		if len(arr)%512: # if not multiple of 512(sector size) round up to nearest
			arr += [0]*(512 - len(arr)%512)
		self.dsk.seek(0) # seek to begining of display
		self.dsk.write(bytearray(arr)) # write display
		self.dsk.close() # sync io reads
		self.dsk = open(self.drive,'rb+') # sync io reads and open

	def writeaudio(self,pwm,freq):
		if freq: # if not zero so no divition by zero, zero is off
			freq = int((16000000/1024)/freq) # divide base speed by wanted speed to get div factor
		pwm = int(freq*pwm) # calculate pwm duty cycle
		arr = [pwm,freq] # make an array out of the values
		if len(arr)%512: # if not multiple of 512(sector size) round up to nearest
			arr += [0]*(512 - len(arr)%512)
		self.dsk.seek(2*160*128) # seek to end of display
		self.dsk.write(bytearray(arr)) #write to buzzer
		self.dsk.close() # sync io reads
		self.dsk = open(self.drive,'rb+') # sync io reads and open

	def readtemp(self):
		self.dsk.seek(2*160*128)  # seek to end of display
		ret = int.from_bytes(self.dsk.read(512)[:2],'little')/16 # read temp value in little endian int16. temp is multiplied by 16 so divide it
		self.dsk.close() # sync io reads
		self.dsk = open(self.drive,'rb+') # sync io reads and open
		#read will queue next read of temp and send over last read each read takes 1.5s because of the temp sensor
		return ret

disp = hardwareD("/dev/sde") # open drive for me its /dev/sde on windows its `r"\\.\physicaldrive"+ number` 
# `wmic diskdrive list` will list drive number in windows. if the drive number is a real drive it will be erased be VERY carefull
cap = cv2.VideoCapture('/home/jesse/Videos/chung.mp4') # open image for testing
if (cap.isOpened()== False): # it didnt open
	print("Error opening video stream or file")

while(cap.isOpened()):
	ret, img = cap.read() # read image data
	if ret == True: # if end of video

		img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) # rotate image lcd is rotated idk why
		img = cv2.resize(img,(128,160),interpolation = cv2.INTER_LANCZOS4) # scale image to lcd size using LANCZOS4
		img = cv2.cvtColor(img,cv2.COLOR_BGR2BGR565) # convert to bgr565 color space the color space the lcd uses
		arr=[]
		for i in range(160):
			for j in range(128):
				arr+= [img[i,j][1],img[i,j][0]] # because idk python well we expand the 3d array to 1d and swap the bytes.
		disp.writedisp(arr) # write the binary data to the display
		disp.writeaudio(0.50,0) # turn off audio
	else:
		break

cap.release()
cv2.destroyAllWindows()

print(disp.readtemp()) # read temp
sleep(1) # wait for recalc
