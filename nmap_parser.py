#!/usr/bin/python

import xmltodict
import os
import util
import config
import assets
import time
import collections


ass = assets.assets(config.DBNAME, config.DBUSER, config.DBPASS)

process_dirs = config.DIRECTORIES

all = ass.getAllAssets()
all_assets = {}
for item in all:
	print "%s - %s" % (time.ctime(item[2]), item[1] )
	all_assets[item[1]] = int(item[0])
old = all_assets.keys()


for process_dir in process_dirs:
	for file in os.listdir(process_dir):
		if "txt" in file:
			parts = file.split("-")
			scan_type = parts[0]
			timestamp = parts[1]
			timestamp = time.mktime(time.strptime(timestamp,"%Y%m%d%H%M"))
			extra_info = parts[2].split(".")[0]
			file = process_dir + os.sep + file
			print file
			print "%s - %s - %s" % ( scan_type, timestamp, extra_info)	

			found_assets = []
			data = xmltodict.parse(open(file,"r"))['nmaprun']
			for host in data['host']:
				ip = host['address']['@addr']
				asset_id = ass.addAsset(host['address']['@addr'], timestamp)
				if asset_id not in all_assets:
					all_assets[ip] = asset_id
				print asset_id
				found_assets.append(host['address']['@addr'])
				if 'port' in host['ports']:
					for port in host['ports']['port']:
						if type(port) == type(collections.OrderedDict()):
							proto = 'unknown'
							if '@protocol' in port:
								proto = port['@protocol']
							if 'service' in port:
								if '@product' in port['service']:
									name = port['service']['@product']
								else:
									name = port['service']['@name']
								version = ''
								if '@version' in port['service']:
									version = port['service']['@version']
							else:
								name = 'unknown'
								version = 'unknown'
							ass.addAssetPort(asset_id, int(port['@portid']), proto, name + ";" + version, timestamp, scan_type)
		
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
	if row[1] not in old:
		print "This is a new host!"
	status = ass.getStatus(row[0])
	big_status = 0
	if len(status) > 10:
			status = status[:10]
	big_status = 1
	for stat in status:
		print "\t%s - %s - %s" % ( time.ctime(stat[2]), stat[1], stat[3] )
	if big_status:
		print "\t results were truncated to the most recent 10 items"
	ports = ass.getAssetPorts(row[0])
	for port in ports:
		print "\t%s - %s (%s by %s)" % ( port, ports[port]['service'], time.ctime(ports[port]['history'][0][0]), ports[port]['history'][0][1] )
