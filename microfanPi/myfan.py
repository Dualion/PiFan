__author__ = 'lluis'

import sys
import os
import time
from daemon import Daemon
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# FAN
FAN_PIN = 11    # Set GPIO pin the fan are connected to
FAN_ON = 35   # Set Temperature the fan put on
FAN_OFF = 30  # Set Temperature the fan put off
FAN_ITVAL = 10  # Set interval the fan verify temperature (in sec)

# Temperature
TEMP_FILE = 'cat /sys/class/thermal/thermal_zone0/temp'

# Set the fan pin as output pins
GPIO.setup(FAN_PIN, GPIO.OUT)


class MyFan(Daemon):
    def run(self):
        self.fan_off()
        sys.stderr.write("In Run")
        sys.stdout.flush()
        sys.stderr.flush()

        while True:
            f_sensor = os.popen(TEMP_FILE)
            temp = float(f_sensor.read()) * 0.001
            f_sensor.close()

            if temp <= FAN_OFF:
                # Stop fan, it's cold!!
                GPIO.output(FAN_PIN, GPIO.LOW)
            if temp >= FAN_ON:
                # We have warmed up enough, turn the fan on
                GPIO.output(FAN_PIN, GPIO.HIGH)

            time.sleep(FAN_ITVAL)

    # Function to set all drives off
    @classmethod
    def fan_off(cls):
        GPIO.output(FAN_PIN, GPIO.LOW)
