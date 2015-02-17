#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from datetime import datetime
import os
import RPi.GPIO as GPIO
from daemon import Daemon
import ConfigParser

config = ConfigParser.SafeConfigParser()

config.read('/etc/pifan/pifan.conf')
fan_pin = int(config.get('Fan', 'fan_pin'))
fan_on = float(config.get('Fan', 'fan_on'))
fan_off = float(config.get('Fan', 'fan_off'))
check_temp_interval = int(config.get('Fan', 'check_temp_interval'))
temp_file = str(config.get('Fan', 'temp_file'))

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
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
            if temp <= fan_off and GPIO.input(fan_pin) == GPIO.HIGH:
                # Stop fan, it's cold!!
                GPIO.output(fan_pin, GPIO.LOW)
                self.pifan_log(str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ": Apagando ventilador, temepratura=" + str(temp) + "ºC")
            if temp >= fan_on and GPIO.input(fan_pin) == GPIO.LOW:
                # We have warmed up enough, turn the fan on
                GPIO.output(fan_pin, GPIO.HIGH)
                self.pifan_log(str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ": Encendiendo ventilador, temepratura=" + str(temp) + "ºC")

            time.sleep(check_temp_interval)

    @classmethod
    def pifan_log(cls, log_string):
        sys.stdout.write("%s\n" % log_string) # write it to console --> so in the log file in /var/log/pifan/pifan.log
        sys.stdout.flush()

    # Function to set all drives off
    @classmethod
    def turn_fan_off(cls):
        GPIO.output(fan_pin, GPIO.LOW)