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
import pifan
import ConfigParser

config = ConfigParser.SafeConfigParser()


def fan():
    config.read('pifan.conf')
    fan_pin = config.get('Fan', 'fan_pin')
    fan_on = config.get('Fan', 'fan_on')
    fan_off = config.get('Fan', 'fan_off')
    check_temp_interval = config.get('Fan', 'check_temp_interval')
    temp_file = config.get('Fan', 'temp_file')
    daemon = pifan.PiFan('/var/run/microfanPi.pid', fan_pin, fan_on, fan_off, check_temp_interval, temp_file)
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

if __name__ == '__main__':
    fan()