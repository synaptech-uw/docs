import serial  					#Used to read in data from the UART 
from serial import Serial
import pyautogui 				# Used to map keyboard to python

serialPort = serial.Serial(port = "COM6", baudrate=9600, bytesize=8, timeout=None, stopbits=serial.STOPBITS_ONE, xonxoff = True) # These input values made sure we were connected with the rright device
serialString = serialPort.readline() 			# Read the complete value each time

pyautogui.PAUSE = 0.01						# Make sure there is no delay between consecutive values when the autogui library is used
jumpFlag = 0.0								# Flag to make sure that jump command is only sent once and then sent again only after relaxing the muscle 

while(1):

    # Wait until there is data waiting in the serial buffer
    #if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline().decode('ascii')										# Decode the bytes data into string, so that I can print the values
        convString = "" + serialString[4] + serialString[5] + serialString[6] + serialString[7]		# Used this technique to convert the data into processable form of float
        print(float(convString))

        if(float(convString) > 1.0): # 3.11 is highest
        	if jumpFlag == 0.0:				# If muscle was relaxed before 
        		pyautogui.press("space")
        		print("Above threshold")
        		jumpFlag = 1.0				# Set threshold to prevent multiple jumps
        else: 
        #	pyautogui.press("m")
        	jumpFlag = 0.0