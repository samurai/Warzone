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
scan_type = "_".join(file.split("_")[0:2])
timestamp = file.split("_")[2]
print timestamp
print scan_type
timestamp = time.mktime(time.strptime(timestamp,"%Y%m%d%H%M"))
print file
data = xmltodict.parse(open(file,"r"))['nmaprun']

util.recursePrint(data)
