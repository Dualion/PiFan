#!/usr/bin/env python

import sys, time, os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#FAN
FAN_PIN = 4     # Set GPIO pin the fan are connected to
FAN_ON = 24.0	# Set Temperature the fan put on
FAN_OFF = 22.0	# Set Temperature the fan put off
FAN_ITVAL = 5	# Set interval the fan verify temperature (in sec)

#Temperature
TEMP_FILE = 'cat /sys/class/thermal/thermal_zone0/temp'

# Set the fan pin as output pins
GPIO.setup(FAN_PIN, GPIO.OUT)

if __name__ == "__main__":
	GPIO.output(FAN_PIN, GPIO.LOW)

	while True:
		fSensor = os.popen(TEMP_FILE)
		temp = float(fSensor.read()) * 0.001
		fSensor.close()

		if temp <= FAN_OFF:
			# Stop fan, it's cold!!
			GPIO.output(FAN_PIN, GPIO.LOW)
			print "OFF"
		if temp >= FAN_ON:
			# We have warmed up enough, turn the fan on
			GPIO.output(FAN_PIN, GPIO.HIGH)
			print "ON"
			
		print str(temp)
		
		time.sleep(FAN_ITVAL)
