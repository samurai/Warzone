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
			return id
		if not timestamp:
			timestamp = time.time()
		sql = "INSERT INTO asset (ip, found) VALUES ('%s', %d) RETURNING id" % ( ip, timestamp )
		print sql
		self.cur.execute(sql)
		self.conn.commit()
		data = self.cur.fetchone()
		return data[0]


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