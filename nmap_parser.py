#!/usr/bin/python

import xmltodict
import os
import util
import config

process_dir = config.DIRECTORY

for file in os.listdir(process_dir):
	if "txt" in file:
		file = process_dir + os.sep + file
		print file
		data = xmltodict.parse(open(file,"r"))['nmaprun']
		util.recursePrint(data)