#!/usr/bin/python

import xmltodict
import os
import util
import config
import assets
import time



ass = assets.assets(config.DBNAME, config.DBUSER, config.DBPASS)

process_dir = config.DIRECTORY

all = ass.getAllAssets()
all_assets = {}
for item in all:
	print "%s - %s" % (time.ctime(item[2]), item[1] )
	all_assets[item[1]] = int(item[0])



for file in os.listdir(process_dir):
	if "txt" in file:
		found_assets = []
		scan_type = "_".join(file.split("_")[0:2])
		timestamp = file.split("_")[2]
#		print timestamp
		timestamp = time.mktime(time.strptime(timestamp,"%Y%m%d%H%M"))
#		print timestamp
		file = process_dir + os.sep + file
		print file
		data = xmltodict.parse(open(file,"r"))['nmaprun']


#		host = data['host'][0]
		for host in data['host']:
			ass.addAsset(host['address']['@addr'], timestamp)
			found_assets.append(host['address']['@addr'])
#		print host['address']['@addr']		

		not_found = all_assets.keys()
		for found in found_assets:
			ass.updateStatus(all_assets[found],timestamp,scan_type, 'up')
			if found in not_found:
				not_found.remove(found)
		for nf in not_found:
			ass.updateStatus(all_assets[nf],timestamp, scan_type,'down')




all = ass.getAllAssets()
for row in all:
	print "%s - first detected %s" % ( row[1], time.ctime(row[2]) )
	status = ass.getStatus(row[0])
	big_status = 0
	if len(status) > 10:
		status = status[:10]
		big_status = 1
	for stat in status:
		print "\t%s - %s - %s" % ( time.ctime(stat[2]), stat[1], stat[3] )
	if big_status:
		print "\t results were truncated to the most recent 10 items"
exit()

if 0:
	if 0:

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
