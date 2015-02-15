#!/usr/bin/env python

"""
To start the daemon, we should run the next command:
python microfanPi.py start

To stop the daemon, we should run the next command:
python microfanPi.py stop

To restart the daemon, we should run the next command:
python microfanPi.py restart
"""

import sys
import time
import os
import RPi.GPIO as GPIO
from daemon import Daemon
import ConfigParser

config = ConfigParser.SafeConfigParser()
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

config.read('pifan.conf')
fan_pin = int(config.get('Fan', 'fan_pin'))
fan_on = float(config.get('Fan', 'fan_on'))
fan_off = float(config.get('Fan', 'fan_off'))
check_temp_interval = int(config.get('Fan', 'check_temp_interval'))
temp_file = str(config.get('Fan', 'temp_file'))

GPIO.setup(fan_pin, GPIO.OUT)


class PiFan(Daemon):
    def run(self):
        self.turn_fan_off()
        sys.stderr.write("In Run")
        sys.stdout.flush()
        sys.stderr.flush()

        while True:
            f_sensor = os.popen(temp_file)
            temp = float(f_sensor.read()) * 0.001
            f_sensor.close()

            if temp <= fan_off:
                # Stop fan, it's cold!!
                GPIO.output(fan_pin, GPIO.LOW)
            if temp >= fan_on:
                # We have warmed up enough, turn the fan on
                GPIO.output(fan_pin, GPIO.HIGH)

            time.sleep(check_temp_interval)

    # Function to set all drives off
    @classmethod
    def turn_fan_off(cls):
        GPIO.output(fan_pin, GPIO.LOW)