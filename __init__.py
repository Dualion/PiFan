#!/usr/bin/env python

"""
To start the daemon, we should run the next command:
python microfanPi.py start

To stop the daemon, we should run the next command:
python microfanPi.py stop

To restart the daemon, we should run the next command:
python microfanPi.py restart
"""

import sys, time, os
import RPi.GPIO as GPIO
from daemon import Daemon

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
    def fan_off(self):
        GPIO.output(FAN_PIN, GPIO.LOW)

if __name__ == "__main__":
    daemon = MyFan('/var/run/microfanPi.pid')
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