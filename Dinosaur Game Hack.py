'''
AUTHOR 	- GAGAN sgagankumar@gmail.com
GITHUB 	- @sgagankumar
VERSION - 1.0
DATE 	- 24/4/2020
'''

# Importing Modules
import win32gui
import pyautogui
import mouse
import keyboard
import time
import itertools
import threading
import sys
import webbrowser
import socket


# GLOBAL VARIABLES
WebPage = "www.google.com"				# Webpage URL
done = False							# Animation flag variable
dinx = 0								# dinosaur x element
diny = 0								# dinosaur y element
color = 0								# color variable


# Function: Gets Pixel RGB Value
def get_pixel_colour(i_x, i_y):
	i_desktop_window_id = win32gui.GetDesktopWindow()
	i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
	long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
	i_colour = int(long_colour)
	win32gui.ReleaseDC(i_desktop_window_id,i_desktop_window_dc)
	r,g,b = (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)
	grayscale = (r+g+b)/3
	return int(grayscale)


# Function: Loading Animation
def animate():
	for c in itertools.cycle(['|', '/', '-', '\\']):
		if done:
			break
		sys.stdout.write('\rworking...  '+ c)
		sys.stdout.flush()
		time.sleep(0.1)
t = threading.Thread(target=animate)


# Function: Check Network Connection
def is_not_connected(hostname):
	try:
		# resolve the host name and return if a DNS is listening
		host = socket.gethostbyname(hostname)
		# connect to the host and return if the host is reachable
		s = socket.create_connection((host, 80), 2)
		s.close()
		print("Network: ON")
		return False
	except:
		pass
	print("Network: OFF")
	return True


# Function: to change control
def changeWindow(timeSec):
	time.sleep(timeSec)
	keyboard.press("alt")
	time.sleep(0.2)
	keyboard.press("tab")
	time.sleep(0.2)
	keyboard.release("alt")
	time.sleep(0.2)
	keyboard.release("tab")
	time.sleep(0.2)


# Function: to fetch mouse position
def getPositions():
	while not (mouse.is_pressed(button='left')):
		time.sleep(0.2)
	x, y = pyautogui.position()
	return (x, y)


# Function: to Check for light or dark theme
def fetchTheme(x, y):
	color = get_pixel_colour(x, y)
	thres = 128
	if color > thres:
		return 1		# Return Light
	else:
		return 0		# Return Dark


# Funtion: to filter and locate eye
def getEye(dinx, diny, theme):
	dino =list()
	dinorow = list()
	offset = 20
	thres = 128
	bit=0
	# Collect the pixel values
	for y in range(diny-offset, diny+offset):
		for x in range(dinx-offset, dinx+offset):
			color = get_pixel_colour(x, y)
			if theme == 1:
				color = 255 - color
			if color > thres:
				bit=1
			else:
				bit=0
			dinorow.append(bit)
		dino.append(dinorow)
		dinorow = list()
	# print(dino)

	# Searching for eye
	for i in range(len(dino)-3):
		for j in range(len(dino[0])-3):
			if(dino[i][j]==1):
				if(dino[i+1][j+1]==0 and dino[i+2][j+2]==0 and dino[i+3][j+3]==1 and dino[i+2][j+3]==1):
					return dinx-offset+j, diny-offset+i
	return -1, -1


# Function: to detect obstacles
def detectObstacle(x, yu, yd, theme):
	for y in range(yu,yd+1,5):
		color = get_pixel_colour(x,y)
		if theme == 1:
			color = 255 - color2
		if color > 128:
			return True
	return False


# Function: AutoPlay Game
def autoPlay(eyex, eyey):
	xPos=eyex+95
	yUprPos=eyey-10
	yDwnPos=eyey+25
	eyex-=100
	eyey-=100
	theme=0
	count=0
	time.sleep(4)
	keyboard.press('space')
	keyboard.release('space')
	while(True):
		theme = fetchTheme(eyex, eyey)
		if detectObstacle(xPos, yUprPos, yDwnPos, theme):
			keyboard.press('space')
			keyboard.release('space')
			print("\r Theme:",theme,"\tDetected:",count,end='')
			count+=1
	print("out")


# Function: Main
def main():
	global done
	
	# Check for internet and opening browser
	print("PROGRAM RUNNING...\n")
	time.sleep(2)
	if is_not_connected(WebPage):
		time.sleep(1)
		print("Action: Browser Opening")
		webbrowser.open(WebPage)
		changeWindow(3)
	else:
		print("\nWARNING : Disconnect the Device from Internet.")
		exit()
	time.sleep(3)

	# Position the dinosaur and Fetch Theme
	print("\nClick on the dinosaur head!")
	clickx, clicky = getPositions()
	time.sleep(1)
	print("Clicked position : ",clickx,",",clicky,sep="")
	theme = fetchTheme(clickx-100,clicky-100)
	time.sleep(1)
	print("Browser Theme :",end="")
	if theme == 1:
		print("Light Mode")
	else:
		print("Dark Mode")
	time.sleep(1)

	# ERROR Fail to recognise Dino Location
	t = threading.Thread(target=animate)
	t.start()		#start loading animation
	eyex, eyey = getEye(clickx, clicky, theme)
	done = True		#end loading animation
	while(eyex==-1):
		print("\r\nWARNING : Failed to Recognise Dino...")
		exit()
	print("\rDino position : ",eyex,":",eyey)

	# Auto Play Game
	print("\nDino indentified! Starting AutoPlay")
	autoPlay(eyex, eyey)


main()