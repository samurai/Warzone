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


		host = data['host'][0]
		print host['address']['@addr']		
		for port in host['ports']['port']:
#			print port
			if '@product' in port['service']:
				name = port['service']['@product']
			else:
				name = port['service']['@name']
			version = ''
			if '@version' in port['service']:
				version = port['service']['@version']
			print "\t%s - %s - %s" % (port['@portid'] , name, version) #, port['service']['@product'], port['service']['@version'])

		util.recursePrint(data['host'][0])
