#!/usr/bin/env python3

import json
import argparse
import codecs
import os
import socket
import subprocess
import re
import netifaces as netif

# Force encoding to UTF-8
import locale                                  # Ensures that subsequent open()s
locale.getpreferredencoding = lambda _=None: 'UTF-8'  # are UTF-8 encoded.

import sys
#sys.stdin = open('/dev/stdin', 'r')
#sys.stdout = open('/dev/stdout', 'w')
#sys.stderr = open('/dev/stderr', 'w')

# Utility functions for the announce.d files
def toUTF8(line):
  return line.decode("utf-8")

def call(cmdnargs):
  output = subprocess.check_output(cmdnargs)
  lines = output.splitlines()
  lines = [toUTF8(line) for line in lines]
  return lines

# Local used functions
def setValue(node,path,value):
  ''' Sets a value inside a complex data dictionary.
      The path Array must have at least one element.
  '''
  key = path[0]
  if len(path) == 1:
    node[key] = value;
  elif key in node:
    setValue(node[key],path[1:],value)
  else:
    node[path[0]] = {}
    setValue(node[key],path[1:],value)

def gateway(batadv_dev):
  output = subprocess.check_output(["batctl","-m",batadv_dev,"gwl","-n"])
  output_utf8 = output.decode("utf-8")
  lines = output_utf8.splitlines()
  gw = None

  for line in lines:
    gw_line = re.match(r"^=> +([0-9a-f:]+) ", line)
    if gw_line:
      gw = gw_line.group(1)

  return gw

def clients(batadv_dev):
  output = subprocess.check_output(["batctl","-m",batadv_dev,"tl","-n"])
  output_utf8 = output.decode("utf-8")
  lines = output_utf8.splitlines()

  count = 0

  for line in lines:
    client_line = re.match(r"^\s\*\s[0-9a-f:]+\s+-\d\s\[[W\.]+\]", line)
    if client_line:
      count += 1

  return count

def addresses(bridge_dev):
  ip_addrs = netif.ifaddresses(bridge_dev)
  ip_list = []

  for ip6 in netif.ifaddresses(bridge_dev)[netif.AF_INET6]:
    raw6 = ip6['addr'].split('%')
    ip_list.append(raw6[0])

  for ip4 in netif.ifaddresses(bridge_dev)[netif.AF_INET]:
    raw4 = ip4['addr'].split('%')
    ip_list.append(raw4[0])

  return ip_list

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--directory', action='store',
                  help='structure directory',required=True)

parser.add_argument('-b', '--batman', action='store',
                  help='batman-adv device',default='bat0')

parser.add_argument('-i', '--interface', action='store',
                  help='freifunk bridge',default='br0')

args = parser.parse_args()

options = vars(args)

directory = options['directory']
batadv_dev = options['batman']
bridge_dev = options['interface']

data = {}

for dirname, dirnames, filenames in os.walk(directory):
  for filename in filenames:
    if filename[0] != '.':
      relPath = os.path.relpath(dirname + os.sep + filename,directory);
      fh = open(dirname + os.sep + filename,'r', errors='replace')
      source = fh.read()
      fh.close()
      value = eval(source)
      setValue(data,relPath.rsplit(os.sep),value)
print(json.dumps(data))
