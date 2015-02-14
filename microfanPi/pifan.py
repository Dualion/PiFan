__author__ = 'lluis'

import sys
import os
import time
from daemon import Daemon
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class PiFan(Daemon):
    def __init__(self, pidfile, fan_pin, fan_on, fan_off, check_temp_interval, temp_file):
        # FAN
        self.fan_pin = fan_pin  # Set GPIO pin the fan are connected to
        self.fan_on = fan_on  # Set Temperature the fan put on
        self.fan_off = fan_off  # Set Temperature the fan put off
        self.check_temp_interval = check_temp_interval  # Set interval the fan verify temperature (in sec)
        # Temperature
        self.temp_file = temp_file
        Daemon.__init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')

    def run(self, fan_pin, fan_on, fan_off, check_temp_interval, temp_file):
        # Set the fan pin as output pins
        GPIO.setup(fan_pin, GPIO.OUT)
        self.fan_off(fan_pin)
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
    def fan_off(cls, fan_pin):
        GPIO.output(fan_pin, GPIO.LOW)