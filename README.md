Alfred Status Scripts for Servers
---------------------------------

A gluon compatible status script for alfred in python.

## Dependencies

 * lsb_release
 * ethtool
 * alfred binary in PATH
 * python3
 * python3-netifaces
 * py-cpuinfo

## Setup

Add _announce.sh_ to your cronjobs, and let it run every minute, e.g.
```
PATH=/opt/alfred/:/bin:/usr/bin:/sbin:$PATH /opt/alfred-announce/announce.sh
```
