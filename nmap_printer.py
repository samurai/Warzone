#!/usr/bin/python

import xmltodict
import os
import util
import config
import assets
import time
import collections
import sys


file = sys.argv[1]
print file
scan_type = file.split("-")[0]
timestamp = file.split("-")[1]
print timestamp
print scan_type
print timestamp
timestamp = time.mktime(time.strptime(timestamp,"%Y%m%d%H%M"))
print file
data = xmltodict.parse(open(file,"r"))['nmaprun']

util.recursePrint(data)
