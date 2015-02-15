# PiFan
Daemon that control fan for **Raspberry Pi**.

# Install
```
sudo python setup.py install
```

# Uninstall
```
sudo pip uninstall pifan
```

To **start** the daemon, we should run the next command:
```
sudo pifan start
```

To **stop** the daemon, we should run the next command:
```
sudo pifan stop
```

To **restart** the daemon, we should run the next command:
```
sudo pifan restart
```

To start pifan automatically on Boot:
```
$ cp ./script/pifan /etc/init.d/pifan
$ chmod a+rx /etc/init.d/pifan
$ insserv pifan
```