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

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# FAN
fan_pin = 11    # Set GPIO pin the fan are connected to
fan_on = 31   # Set Temperature the fan put on
fan_off = 30  # Set Temperature the fan put off
check_temp_interval = 10  # Set interval the fan verify temperature (in sec)

# Temperature
temp_file = 'cat /sys/class/thermal/thermal_zone0/temp'

# Set the fan pin as output pins
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

if __name__ == "__main__":
    daemon = PiFan('/var/run/microfanPi.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "Usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)