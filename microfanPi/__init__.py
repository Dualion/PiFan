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
import myfan


def fan():
    daemon = myfan.MyFan('/var/run/microfanPi.pid')
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
