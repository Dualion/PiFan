#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pwd
import grp
import signal


class Daemon:
    """
    A generic daemon class.
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null', user=None, group=None):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.user = user
        self.group = group

    def openstreams(self):
        """
        Open the standard file descriptors stdin, stdout and stderr as specified
        in the constructor.
        """
        if self.stdout != "/dev/null" and not os.path.exists(os.path.dirname(self.stdout)):
            os.mkdir(os.path.dirname(self.stdout))
        if self.stderr != "/dev/null" and not os.path.exists(os.path.dirname(self.stderr)):
            os.mkdir(os.path.dirname(self.stderr))
        if self.stdin != "/dev/null" and not os.path.exists(os.path.dirname(self.stdin)):
            os.mkdir(os.path.dirname(self.stdin))
        si = open(self.stdin, "r")
        so = open(self.stdout, "a+")
        se = open(self.stderr, "a+", 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
    def handlesighup(self, signum, frame):
        self.openstreams()

    def handlesigterm(self, signum, frame):
        if self.pidfile is not None:
            try:
                os.remove(self.pidfile)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                pass
        sys.exit(0)

    def switchuser(self, user, group):
        if group is not None:
            if isinstance(group, basestring):
                group = grp.getgrnam(group).gr_gid
            os.setegid(group)
        if user is not None:
            if isinstance(user, basestring):
                user = pwd.getpwnam(user).pw_uid
            os.seteuid(user)
            if "HOME" in os.environ:
                os.environ["HOME"] = pwd.getpwuid(user).pw_dir
    
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        """
        
        # Finish up with the current stdout/stderr
        sys.stdout.flush()
        sys.stderr.flush()
        
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        
        # Now I am a daemon!
    
        # Switch user
        self.switchuser(self.user, self.group)

        # Redirect standard file descriptors
        self.openstreams()

        # Write pid file
        if self.pidfile is not None:
            open(self.pidfile, "wb").write(str(os.getpid()))

        # Reopen file descriptions on SIGHUP
        signal.signal(signal.SIGHUP, self.handlesighup)

        # Remove pid file and exit on SIGTERM
        signal.signal(signal.SIGTERM, self.handlesigterm)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        sys.stderr.write("To Run\n")
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        if self.pidfile is None:
            sys.exit("no pidfile specified")
        try:
            pidfile = open(self.pidfile, "rb")
        except IOError, exc:
            sys.exit("can't open pidfile %s: %s" % (self.pidfile, str(exc)))
        data = pidfile.read()
        try:
            pid = int(data)
        except ValueError:
            sys.exit("mangled pidfile %s: %r" % (self.pidfile, data))
        os.kill(pid, signal.SIGTERM)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """