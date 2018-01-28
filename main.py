#!/usr/bin/env python
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import time
import configparser
from datetime import datetime, date
from PIL import Image, ImageDraw, ImageFont


#Wiring config
motor_pin = 4
button_pin = 24
#OLED screen
RST = 13
DC = 11
SPI_PORT = 0
SPI_DEVICE = 0

#Config/Prefs Config
configFilePath = 'resources/config.ini'
config = configparser.ConfigParser()
config.read(configFilePath)
prefsDateTimeFormat = '%b %d, %Y %I:%M%p';
prefs = config['prefs']

#Software config
version = "1.0"
spin_duration = 0.3 #seconds

#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(motor_pin, GPIO.OUT)
servo = GPIO.PWM(motor_pin, 50) #50hz frequency

#OLED screen setup
#disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, sclk=10, din=9, cs=12)
# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# text drawing setup
largeFontSize = 16
largeFont = ImageFont.truetype('resources/neoletters.ttf', largeFontSize)
smallFontSize = 16
smallFont = ImageFont.truetype('resources/Nintendo-DS-BIOS.ttf', smallFontSize)

#Functions
def savePref(thePref, theValue):
    prefs[thePref] = theValue
    print('SAVING')
    print(thePref)
    print(theValue)
    with open(configFilePath, 'w') as configfile:
        config.write(configfile)

lastTimePrefStr = prefs.get('lastFedTime')
print(lastTimePrefStr)
lastTime = datetime.strptime(lastTimePrefStr, prefsDateTimeFormat)
isSpinning = False

def feed():
    global lastTime
    global isSpinning
    try:
        displayFeeding()
        lastTime = datetime.now()
        savePref('lastFedTime', lastTime.strftime(prefsDateTimeFormat))
        
        isSpinning = True
        servo.start(0)
    
        #rotate clockwise
        servo.ChangeDutyCycle(2.5)
        time.sleep(spin_duration)
        
        #Pause for delay
        servo.ChangeDutyCycle(0)
        time.sleep(spin_duration)
        
        #rotate counter-clockwise 
        servo.ChangeDutyCycle(12)
        time.sleep(spin_duration)
        
        #stop
        servo.ChangeDutyCycle(0)
        #servo.stop()
        #GPIO.cleanup()
        isSpinning = False
        
        #update display
        clearBelowTitle()
        displayLastTime()
    except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()
        isSpinning = False
        
def clearScreen():
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width, height), outline=0, fill=0)
    
def clearBelowTitle():
    draw.rectangle((0, largeFontSize, width, height), outline=0, fill=0)
    
def displayTitle():
    clearScreen()
    draw.rectangle((0, 0, width, largeFontSize), outline=0, fill=255)
    draw.text((2, 2), "CAT FEEDER " + version, font=largeFont, fill=0)
    disp.image(image)
    disp.display()

def displayFeeding():
    clearBelowTitle()
    top = largeFontSize + 15
    draw.text((10, top), "Feeding Now!", font=largeFont, fill=255)
    disp.image(image)
    disp.display()
    
def displayLastTime():
    top = largeFontSize + 10
    #https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    lastFedDisplay = lastTime.strftime("%a, %b %d    %I:%M %p")
    
    draw.text((0, top), "Last Fed:", font=largeFont, fill=255)
    draw.text((10, top + largeFontSize), lastFedDisplay, font=smallFont, fill=255)
    disp.image(image)
    disp.display()
    
#Show the title
displayTitle()
displayLastTime()

#Listen for button presses
while True:
    input_state = GPIO.input(button_pin)
    if input_state == False and isSpinning == False:
        #print('Button Pressed')
        feed()
        
    time.sleep(0.1) #break up the loop a bit to we don't use 100% CPU all the time
