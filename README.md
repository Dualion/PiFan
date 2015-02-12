# MicroFan-Pi
Daemon that control microfan for **Raspberry Pi**.

# Install
```
python setup.py install
```

# Uninstall
```
pip uninstall microfanPi
```

To **start** the daemon, we should run the next command:
```
microfanPi start
```

To **stop** the daemon, we should run the next command:
```
microfanPi stop
```

To **restart** the daemon, we should run the next command:
```
microfanPi restart
```

To start microfanPi automatically on Boot:
```
$ cp ./script/microfanPi /etc/init.d/microfanPi
$ chmod a+rx /etc/init.d/microfanPi
$ insserv microfanPi
```
