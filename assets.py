#!/usr/bin/python

import psycopg2
import config
import IPy
import time

class assets:

	def __init__(self, db, user, password):
		self.dbname = db
		self.dbuser = user
		self.dbpass = password
		try:
			self.conn = psycopg2.connect("dbname='%s' user='%s' host='localhost' password='%s'" %(self.dbname, self.dbuser, self.dbpass))
			self.cur = self.conn.cursor()
		except:
			print "Failed to connect to database"
			exit()


	def isValidIP(self, ip):
		try:
			IPy.IP(ip)
			return True
		except:
			print "IP address %s is not valid" % ( ip ) 
			return False
		


	def assetExists(self, ip):
		if not self.isValidIP(ip):
			return 0
		sql = "SELECT * FROM asset WHERE ip = '%s'" % ( ip )
		self.cur.execute(sql)
		data = self.cur.fetchall()
		return data


	def addAsset(self, ip, timestamp = 0):
		if not self.isValidIP(ip):
			return 0
		id = self.assetExists(ip)
		if id:
			return int(id[0][0])
		if not timestamp:
			timestamp = time.time()
		sql = "INSERT INTO asset (ip, found) VALUES ('%s', %d) RETURNING id" % ( ip, timestamp )
		print sql
		self.cur.execute(sql)
		self.conn.commit()
		data = self.cur.fetchone()
		return int(data[0])


	def getAllAssets(self):
		sql = "SELECT * FROM asset ORDER BY id DESC"
		self.cur.execute(sql)
		data = self.cur.fetchall()
		return data


	def updateStatus(self, asset_id, timestamp, scan_type, status):
		sql = "SELECT count(*) FROM status WHERE asset_id=%d AND detection_type='%s' and detected=%d and status='%s'" % ( asset_id, scan_type, timestamp, status)
		self.cur.execute(sql)
		data = self.cur.fetchone()
		if data[0] == 0:
			sql = "INSERT INTO status (asset_id, detection_type, detected, status) VALUES (%d, '%s', %d, '%s')" % ( asset_id, scan_type, timestamp, status)
			self.cur.execute(sql)
			self.conn.commit()

	def getStatus(self, asset_id):
		sql = "SELECT * FROM status WHERE asset_id=%d ORDER BY detected DESC" % ( asset_id )
		self.cur.execute(sql)
		data = self.cur.fetchall()
		return data


	def addAssetPort(self, asset_id, port, port_type, service, timestamp, scan_type):
		sql = "SELECT count(*) FROM ports WHERE asset_id=%d AND port=%d AND type='%s' AND detected=%d AND detection_type='%s'" % ( asset_id, port, port_type, timestamp, scan_type )
		self.cur.execute(sql)
		data = self.cur.fetchone()
		if data[0] == 0:
			sql = "INSERT INTO ports ( asset_id, port, type, detected, detection_type, service) VALUES (%d, %d, '%s', %d, '%s', '%s')"
			self.cur.execute(sql % (asset_id, port, port_type, timestamp, scan_type, service))
			self.conn.commit()

	def getAssetPorts(self, asset_id):
		sql = "SELECT port, type, detected, detection_type, service FROM ports where asset_id=%d ORDER BY detected DESC" % ( asset_id )
		self.cur.execute(sql)
		data = self.cur.fetchall()
		ports = {}
		for row in data:
			port = row[1]+"/"+str(row[0])
			if port not in ports:
				ports[port] = {'history':[]}
			ports[port]['history'].append((row[2],row[3]))
			ports[port]['service'] = row[4]
		return ports