# Raspberry Pi Controlled Cat Feeder

This is a very much work-in-progress side project for myself for the year 2018.  This is my first attempt at physical computing. The goal here is to be able to dispense cat food into a dish at automated intervals, or manually by pressing a button.

### Hardware
Currently, this is a mess of wires on my desk, but below is a list of all hardware used right now
 - [Raspberry Pi Zero W](https://www.adafruit.com/product/3400)
 - [Adafruit 128x64 OLED screen](https://www.adafruit.com/product/938)
 - [FeeTech FS5103R Continuous Rotation Servo](https://www.adafruit.com/product/154)
 - [Zevro KCH-06127 Compact Dry Food Dispenser](https://www.amazon.com/gp/product/B009Q8PZMK/)

### Requirements & Setup
 - Rasbpian 
 - Python & related libraries: run `sudo apt-get install build-essential python-pip python-dev python-smbus git`
 - `RPi.GPIO` library: run `sudo apt-get install python-rpi.gpio python3-rpi.gpio`
 - `Adafruit_GPIO` library: Follow instructions on https://github.com/adafruit/Adafruit_Python_GPIO
 - `Adafruit_Python_SSD1306` library: clone this repo `https://github.com/adafruit/Adafruit_Python_SSD1306` and run `python3 setup.py`

### TODO Items
 - Fix OLED screen to have a faster refresh rate. Awaiting answer on [this thread](https://forums.adafruit.com/viewtopic.php?f=8&t=130166).
 - Trigger remotely via IFTTT action
 - Trigger remotely via Amazon Echo
 - Display on screen if last feeding was timed or local manual, or remote manual
 - Send webhook when triggered (time and trigger type)
 - Run on schedule
 - Start script on boot
